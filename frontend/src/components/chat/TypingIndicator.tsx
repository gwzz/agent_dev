import React from "react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-3 mb-6">
      <Avatar className="w-8 h-8 flex-shrink-0">
        <AvatarFallback>A</AvatarFallback>
      </Avatar>
      <div className="max-w-[85%] flex flex-col">
        <div className="px-4 py-3 rounded-2xl bg-muted text-foreground rounded-bl-md">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-100"></div>
            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-200"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export { TypingIndicator };