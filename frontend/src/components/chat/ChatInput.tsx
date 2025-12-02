import React, { useState, useRef, KeyboardEvent } from "react";
import { useChatStore } from "@/store/chatStore";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { 
  Paperclip, 
  Mic, 
  Send 
} from "lucide-react";
import { cn } from "@/lib/utils";

const ChatInput: React.FC = () => {
  const [inputValue, setInputValue] = useState("");
  const textareaRef = useRef<HTMLTextArea>(null);
  const { sendMessage, isStreaming } = useChatStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isStreaming) {
      await sendMessage(inputValue);
      setInputValue("");
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any); // Type assertion since FormEvent and KeyboardEvent are compatible here
    }
  };

  // Auto-resize textarea as user types
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const textarea = e.target;
    textarea.style.height = "auto";
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + "px";
    setInputValue(textarea.value);
  };

  return (
    <form onSubmit={handleSubmit} className="border-t p-4 bg-background">
      <div className="flex items-end gap-2">
        <div className="flex-1 relative">
          <Textarea
            ref={textareaRef}
            value={inputValue}
            onInput={handleInput}
            onKeyDown={handleKeyDown}
            placeholder="Type your message here..."
            className="min-h-[60px] max-h-[200px] py-3 pr-10 resize-none overflow-hidden"
            disabled={isStreaming}
          />
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="absolute bottom-2 right-2 h-8 w-8"
            disabled={isStreaming}
          >
            <Mic className="h-4 w-4" />
            <span className="sr-only">Voice input</span>
          </Button>
        </div>
        <Button 
          type="submit" 
          size="icon" 
          className="h-10 w-10 flex-shrink-0"
          disabled={isStreaming || !inputValue.trim()}
        >
          {isStreaming ? (
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"></div>
          ) : (
            <Send className="h-4 w-4" />
          )}
          <span className="sr-only">Send</span>
        </Button>
      </div>
      <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
        <div className="flex items-center gap-2">
          <Button type="button" variant="ghost" size="sm" className="h-6 p-2 text-xs" disabled>
            <Paperclip className="h-3 w-3 mr-1" />
            Attach
          </Button>
          <span>Shift+Enter for new line</span>
        </div>
        <div>
          {isStreaming ? "Processing..." : "Ready"}
        </div>
      </div>
    </form>
  );
};

export { ChatInput };