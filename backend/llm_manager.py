import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

class LLMManager:
    """Manages interactions with the Gemini LLM and conversation memory."""
    def __init__(self):
        if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
            print("Error: Gemini API Key is not set in config.py. Please update it.")
            self.model = None
            self.memory = None
        else:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)
                print(f"Loaded main Gemini model: {GEMINI_MODEL_NAME}")

                self.memory = ConversationBufferMemory(
                    return_messages=True
                )
                print("ConversationBufferMemory initialized.")

            except Exception as e:
                print(f"Error configuring Gemini API or loading models: {e}")
                self.model = None
                self.memory = None

    def generate_response(self, query, context):
        """
        Generates a summarized, friendly, and polite response using Gemini
        based on the query and retrieved context, incorporating conversation history.
        Includes checks for specific redirections.
        """
        if not self.model or not self.memory:
            return "I cannot generate a response because the Gemini model or memory is not properly initialized."

        lower_query = query.lower()

        # --- Handle specific redirections (e.g., self-referential, Case Studies, Contact Info, Pillars) ---

        # Self-referential questions about the chatbot itself
        self_referential_phrases = [
            "who are your clients", "what are your clients",
            "who are your customers", "what are your customers",
            "who are you", "what is your purpose", "what do you do",
            "tell me about yourself", "how can i contact you"
        ]
        for phrase in self_referential_phrases:
            if phrase in lower_query:
                response_text = "I am a chatbot designed to provide information about IDC. If you're looking for information about IDC's clients or how to contact IDC, please ask a question specifically about IDC, for example: 'Who are IDC's clients?' or 'How can I contact IDC?'"
                self.memory.save_context({"input": query}, {"output": response_text})
                return response_text

        # Redirection for Case Studies (if specific details aren't found via RAG)
        case_study_phrases = [
            "case studies", "case study", "examples of work", "projects worked on"
        ]
        # NOTE: This block is kept if you want a *general* redirection for "case studies"
        # even if specific ones (like Etihad, Markolines) are handled by RAG.
        # If you want ALL case study queries to go through RAG, remove this block.
        # For now, it's kept as a general fallback if RAG doesn't find a strong match.
        if "case study" in lower_query or "case studies" in lower_query:
             # Check if the context is very sparse or non-specific to a case study
             # This is a heuristic; a more advanced check would involve semantic similarity
             # For now, if the query is general "case study" and RAG doesn't return specific case study content,
             # this fallback might still trigger.
             # If you want to force RAG for ALL case studies, remove this 'if' block.
            if not any(cs_keyword in c.lower() for c in context for cs_keyword in ["case study |", "opportunity", "solution", "business outcomes"]):
                response_text = "I don't have enough detailed information to list specific case studies, but you can usually find our comprehensive case studies on IDC's official website under the 'Case Studies' or 'Our Work' section. For example: [https://www.idctechnologies.com/case-studies](https://www.idctechnologies.com/case-studies) (Please replace with your actual URL if different)."
                self.memory.save_context({"input": query}, {"output": response_text})
                return response_text


        # Hardcoded response for Contact Information
        contact_phrases = [
            "how can i contact idc", "how to contact idc", "how do i contact idc",
            "idc contact", "contact information for idc", "idc phone number",
            "idc email", "idc address"
        ]
        for phrase in contact_phrases:
            if phrase in lower_query:
                response_text = "To contact IDC, you can email info@idctechnologies.com or visit their contact us page on the official website. They'll be happy to assist you!"
                self.memory.save_context({"input": query}, {"output": response_text})
                return response_text

        # NEW: Hardcoded response for "Pillars of IDC"
        pillars_phrases = [
            "pillars of idc", "6 pillars of idc", "idc pillars", "idc offering stack"
        ]
        for phrase in pillars_phrases:
            if phrase in lower_query:
                response_text = "IDC's pillars refer to the company's offering stack, which includes: Digital Disruption, Application Modernization, Platform Enablement, Smart Services, Cyber Security, and Operations Support. These represent the core areas of their digital and technology services."
                self.memory.save_context({"input": query}, {"output": response_text})
                return response_text
        
        # --- End of specific query handling ---

        # Load conversation history from memory
        chat_history_messages = self.memory.load_memory_variables({})["history"]

        # Format chat history for Gemini's generate_content 'contents' payload
        gemini_chat_history = []
        for msg in chat_history_messages:
            if isinstance(msg, HumanMessage):
                gemini_chat_history.append({"role": "user", "parts": [{"text": msg.content}]})
            elif isinstance(msg, AIMessage):
                gemini_chat_history.append({"role": "model", "parts": [{"text": msg.content}]})

        # Construct the full 'contents' payload for Gemini
        system_instruction = (
            "You are a helpful, friendly, and polite assistant for a company chatbot. "
            "Your main goal is to provide comprehensive and summarized answers based *only* on the provided context. "
            "Aim for a response length of at least 75 words if the context allows for it, elaborating on details found. "
            "When presenting lists (e.g., industries, clients, case studies), strive for consistency in formatting and content if the context provides a clear list. "
            "If the answer is not in the context, please politely state that you don't have enough information. "
            "Do not invent information. Please provide a friendly and polite summary of the relevant information."
        )
        
        contents_payload = [{"role": "user", "parts": [{"text": system_instruction}]}]
        
        # Add formatted chat history
        contents_payload.extend(gemini_chat_history)
        
        # Add the current RAG context and query as the latest user turn
        current_user_prompt = f"Context:\n" + "\n---\n".join(context) + f"\n\nQuestion: {query}\nAnswer (friendly, polite, and summarized, aiming for 75+ words and consistent list formatting):"
        contents_payload.append({"role": "user", "parts": [{"text": current_user_prompt}]})

        bot_response = ""

        try:
            print("Sending request to Gemini model (with memory and RAG context)...")
            response = self.model.generate_content(contents_payload)
            print("Response received from Gemini.")

            if response.candidates:
                if response.candidates[0].content.parts:
                    bot_response = response.candidates[0].content.parts[0].text
            else:
                bot_response = "I apologize, but I couldn't find a clear answer in the provided information."
        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            bot_response = "I'm sorry, an error occurred while trying to generate a response. Please try again later."
        
        self.memory.save_context({"input": query}, {"output": bot_response})
        
        return bot_response
