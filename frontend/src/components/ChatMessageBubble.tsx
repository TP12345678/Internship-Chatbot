// components/ChatMessageBubble.tsx

import React from "react";
import { cn } from "@/lib/utils";

export type Message = {
  id: string | number;
  text: string;
  from: "user" | "bot";
};

interface ChatMessageBubbleProps {
  message: Message;
}

const ChatMessageBubble: React.FC<ChatMessageBubbleProps> = ({ message }) => {
  const isUser = message.from === "user";

  return (
    <div
      className={cn(
        "flex w-full mb-2",
        isUser ? "justify-end" : "justify-start",
      )}
    >
      <div
        className={cn(
          "max-w-xs px-4 py-2 rounded-lg text-sm",
          isUser
            ? "bg-green-600 text-white rounded-br-none"
            : "bg-gray-100 text-gray-800 rounded-bl-none",
        )}
      >
        {message.text}
      </div>
    </div>
  );
};

export default ChatMessageBubble;
