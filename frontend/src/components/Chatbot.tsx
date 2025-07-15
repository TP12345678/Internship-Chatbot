"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { MessageCircle, X } from "lucide-react";
import { Input } from "./ui/input";
import ChatMessageBubble, {
  type Message,
} from "@/components/ChatMessageBubble";

const messages: Message[] = [
  { id: 1, text: "Hello!", from: "bot" },
  { id: 2, text: "Hi there!", from: "user" },
  { id: 3, text: "How can I assist you today?", from: "bot" },
];
export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Chat Toggle Button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 right-4 z-50 bg-green-600 hover:bg-green-700 rounded-full w-14 h-14 flex items-center justify-center shadow-lg"
      >
        <MessageCircle className="w-6 h-6 text-white" />
      </Button>

      {/* Floating Chat Panel */}
      {isOpen && (
        <div className="fixed bottom-20 right-4 w-[320px] h-[450px] bg-white shadow-xl border rounded-lg flex flex-col z-40 overflow-hidden animate-in fade-in slide-in-from-bottom-5">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-2 border-b bg-muted">
            <span className="font-semibold">Chat</span>
            <button onClick={() => setIsOpen(false)}>
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Chat Body */}
          <div className="flex-1 overflow-y-auto p-4 text-sm text-muted-foreground space-y-2">
            {messages.map((msg) => (
              <ChatMessageBubble key={msg.id} message={msg} />
            ))}
          </div>

          {/* Chat Input */}
          <div className="p-2 border-t bg-background flex gap-2">
            <Input
              type="text"
              placeholder="Type a message..."
              className="flex-1 border px-3 py-2 rounded text-sm outline-none"
            />
            <Button size="sm">Send</Button>
          </div>
        </div>
      )}
    </>
  );
}
