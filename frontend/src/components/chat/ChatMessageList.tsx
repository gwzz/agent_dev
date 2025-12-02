import React, { useEffect, useRef } from "react";
import { Message } from "@/types";
import { ChatMessage } from "@/components/chat/ChatMessage";
import { TypingIndicator } from "@/components/chat/TypingIndicator";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

interface ChatMessageListProps {
  messages: Message[];
  isStreaming: boolean;
}

const ChatMessageList: React.FC<ChatMessageListProps> = ({ 
  messages, 
  isStreaming 
}) => {
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages, isStreaming]);

  return (
    <ScrollArea className="flex-1 p-4">
      <div className="flex flex-col">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <p>Send a message to start the conversation</p>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}
        
        {isStreaming && <TypingIndicator />}
      </div>
      <ScrollBar orientation="vertical" />
    </ScrollArea>
  );
};

export { ChatMessageList };