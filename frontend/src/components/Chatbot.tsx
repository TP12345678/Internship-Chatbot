"use client";

import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { MessageCircle, X } from "lucide-react";
import { Input } from "./ui/input";
import ChatMessageBubble, {
	type Message,
} from "@/components/ChatMessageBubble"; // Adjust path if needed

const STORAGE_KEY = "chatbot_user_details";
const EXPIRY_DAYS = 3;
const apiUrl = import.meta.env.FLASK_BACKEND_URL || "http://127.0.0.1:5000";
export default function Chatbot() {
	const [isOpen, setIsOpen] = useState(false);
	const [value, setValue] = useState("");
	const [isLoading, setIsLoading] = useState(false);

	// State for user verification
	const [isVerified, setIsVerified] = useState(false);
	const [userName, setUserName] = useState("");
	const [userEmail, setUserEmail] = useState("");

	const [chatMessages, setChatMessages] = useState<Message[]>([]);
	const messagesEndRef = useRef<HTMLDivElement | null>(null);

	useEffect(() => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [chatMessages, isLoading]);

	// Function to initialize the chat *after* verification
	const startChat = () => {
		setChatMessages([
			{
				id: 1,
				from: "bot",
				type: "initial",
				text: `Hi ${userName}, I’m IDC Bot – your digital guide to IDC Technologies.\n\nHow can I help you today?`,
				suggestions: [
					"What are IDC’s capabilities & service areas?",
					"Show me industry-specific solutions.",
					"Tell me about client success stories.",
					"How can I request a proposal?",
				],
			},
		]);
	};

	const sendMessage = async (messageText: string) => {
		if (!messageText.trim()) return;

		const userMessage: Message = {
			id: Date.now(),
			text: messageText,
			from: "user",
		};

		setChatMessages(prev => [...prev, userMessage]);
		setIsLoading(true);

		try {
			const response = await fetch("/ask", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				// Include user details in the request body
				body: JSON.stringify({
					query: messageText,
					email: userEmail ,
				}),
			});
			const data = await response.json();
			const botMessage: Message = {
				id: Date.now() + 1,
				text: data.response || "Sorry, I didn’t understand that.",
				from: "bot",
			};
			setChatMessages(prev => [...prev, botMessage]);
		} catch (error) {
			console.error("Error fetching response:", error);
			const errorMessage: Message = {
				id: Date.now() + 2,
				text: "An error occurred while fetching the response.",
				from: "bot",
			};
			setChatMessages(prev => [...prev, errorMessage]);
		} finally {
			setIsLoading(false);
		}
	};

	const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		sendMessage(value);
		setValue("");
	};

	const handleSuggestionClick = (suggestion: string) => {
		sendMessage(suggestion);
	};

	// Handler for the verification form
	const handleVerificationSubmit = async (
		e: React.FormEvent<HTMLFormElement>
	) => {
		e.preventDefault();
		if (userName.trim() && userEmail.trim()) {
			try {
				await fetch(`${apiUrl}/register`, {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ name: userName, email: userEmail }),
				});
				console.log("User details successfully sent to backend.");
			} catch (error) {
				console.error("Failed to register user on the backend:", error);
				// We proceed even if the backend call fails, so the user can still chat.
			}

			const now = new Date();
			const expiryTime = now.getTime() + EXPIRY_DAYS * 24 * 60 * 60 * 1000;

			const item = {
				name: userName,
				email: userEmail,
				expiry: expiryTime,
			};
			try {
				localStorage.setItem(STORAGE_KEY, JSON.stringify(item));
				setIsVerified(true);
				startChat();
			} catch (error) {
				console.error("Could not write to localStorage:", error);
				// Fallback for private browsing mode, etc.
				setIsVerified(true);
				startChat();
			}
		}
	};

	useEffect(() => {
		if (isOpen) {
			try {
				const itemStr = localStorage.getItem(STORAGE_KEY);
				if (!itemStr) {
					return; // No stored data
				}

				const item = JSON.parse(itemStr);
				const now = new Date();

				// Compare the expiry time with the current time
				if (now.getTime() > item.expiry) {
					// If the item is expired, remove it from storage and do nothing
					localStorage.removeItem(STORAGE_KEY);
				} else {
					// If the item is not expired, set the state and verify the user
					setUserName(item.name);
					setUserEmail(item.email);
					setIsVerified(true);
				}
			} catch (error) {
				console.error("Could not access localStorage:", error);
			}
		}
	}, [isOpen]);

	useEffect(() => {
		if (isVerified && userName) {
			startChat();
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [isVerified, userName]);

	return (
		<>
			<Button
				onClick={() => setIsOpen(!isOpen)}
				className="fixed bottom-4 right-4 z-50 bg-gradient-to-tr from-blue-600 to-purple-500  hover:scale-105 rounded-full size-12 flex items-center justify-center shadow-2xl transition-transform duration-200 ease-in-out"
				aria-label="Open chat"
			>
				<MessageCircle className="w-7 h-7 text-white drop-shadow-lg" />
			</Button>

			{isOpen && (
				<div className="fixed bottom-24 right-6 w-[360px] h-[520px] z-50">
					<div
						className="flex flex-col h-full rounded-lg border-none shadow-2xl overflow-hidden backdrop-blur-lg bg-white/80"
						style={{ border: "none", boxShadow: "0 16px 48px 0 #4f51d550" }}
					>
						<div className="flex items-center justify-between px-5 py-3 bg-gradient-to-tr from-blue-600/50 to-purple-500/50 backdrop-blur-sm border-b border-white/20">
							<span className="font-semibold text-gray-800 text-lg">
								Ask IDC
							</span>
							<button
								onClick={() => setIsOpen(false)}
								aria-label="Close chat"
								className="cursor-pointer"
							>
								<X className="w-5 h-5 text-gray-700" />
							</button>
						</div>

						{/* --- CONDITIONAL UI: Verification Form or Chat --- */}
						{isVerified ? (
							<>
								{/* Chat Area */}
								<div className="flex-1 overflow-y-auto p-5 text-sm space-y-4">
									{chatMessages.map(msg => (
										<ChatMessageBubble
											key={msg.id}
											message={msg}
											onSuggestionClick={handleSuggestionClick}
										/>
									))}
									{isLoading && (
										<div className="flex items-center gap-1 text-xs text-purple-600 pl-12 pt-2">
											<span className="animate-bounce w-2 h-2 bg-purple-300 rounded-full"></span>
											<span className="animate-bounce w-2 h-2 bg-purple-300 rounded-full [animation-delay:0.15s]"></span>
											<span className="animate-bounce w-2 h-2 bg-purple-300 rounded-full [animation-delay:0.3s]"></span>
										</div>
									)}
									<div ref={messagesEndRef}></div>
								</div>

								{/* Chat Input Form */}
								<form
									onSubmit={handleSubmit}
									className="p-3 border-t border-blue-800/50 flex gap-2"
								>
									<Input
										value={value}
										onChange={e => setValue(e.target.value)}
										type="text"
										placeholder="Type a message..."
										className="flex-1 bg-blue-800/30 border-none placeholder:text-white text-white px-4 py-2 rounded-sm text-sm outline-none focus:ring-2 focus:ring-blue-400"
									/>
									<Button
										size="sm"
										type="submit"
										disabled={isLoading}
										className="bg-blue-500  text-white hover:bg-purple-600 px-4 rounded-sm h-full shadow"
									>
										Send
									</Button>
								</form>
							</>
						) : (
							<>
								{/* Verification Form */}
								<div className="flex-1 flex flex-col justify-center p-6 text-gray-800">
									<h2 className="text-xl font-bold mb-2 text-center">
										Welcome!
									</h2>
									<p className="text-sm mb-6 text-center text-gray-800/80">
										Please enter your details to start chatting with IDC bot.
									</p>
									<form
										onSubmit={handleVerificationSubmit}
										className="flex flex-col gap-4"
									>
										<div className="flex flex-col gap-2">
											<label className="text-sm text-gray-800" htmlFor="name">
												Name
											</label>
											<Input
												id="name"
												type="text"
												placeholder="John Doe"
												value={userName}
												onChange={e => setUserName(e.target.value)}
												required
												className="border-blue-700 placeholder:text-gray-600 text-gray-800 rounded-sm focus:ring-2 focus:ring-white"
											/>
										</div>
										<div className="flex flex-col gap-2">
											<label className="text-sm text-gray-800" htmlFor="email">
												Email
											</label>
											<Input
												id="email"
												type="email"
												placeholder="john.doe@example.com"
												value={userEmail}
												onChange={e => setUserEmail(e.target.value)}
												required
												className="border-blue-700 placeholder:text-gray-600 text-gray-800 rounded-sm focus:ring-2 focus:ring-white"
											/>
										</div>
										<Button
											type="submit"
											className="bg-blue-800 text-white font-bold hover:bg-blue-700 cursor-pointer mt-2 rounded-sm py-2"
										>
											Start Chat
										</Button>
									</form>
								</div>
							</>
						)}
					</div>
				</div>
			)}
		</>
	);
}
