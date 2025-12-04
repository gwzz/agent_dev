import React, { useState, useRef, KeyboardEvent } from "react";
import { useChatStore } from "@/store/chatStore";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Paperclip,
  Mic,
  Send,
  Sparkles
} from "lucide-react";
import { cn } from "@/lib/utils";

const ChatInput: React.FC = () => {
  const [inputValue, setInputValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
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
    <form onSubmit={handleSubmit} className="border-t bg-card p-4 shadow-sm">
      <div className="flex items-end gap-2">
        <div className="flex-1 relative">
          <Textarea
            ref={textareaRef}
            value={inputValue}
            onInput={handleInput}
            onKeyDown={handleKeyDown}
            placeholder="Message your agent..."
            className="min-h-[60px] max-h-[200px] py-3 pr-12 resize-none overflow-hidden border-0 bg-muted/50 focus-visible:ring-2 focus-visible:ring-primary/30 rounded-xl px-4"
            disabled={isStreaming}
          />
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="absolute bottom-2 right-2 h-8 w-8 text-muted-foreground hover:text-foreground"
            disabled={isStreaming}
          >
            <Mic className="h-4 w-4" />
            <span className="sr-only">Voice input</span>
          </Button>
        </div>
        <Button
          type="submit"
          size="icon"
          className="h-12 w-12 flex-shrink-0 rounded-xl bg-primary hover:bg-primary/90 shadow-md"
          disabled={isStreaming || !inputValue.trim()}
        >
          {isStreaming ? (
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
          ) : (
            <Send className="h-4 w-4" />
          )}
          <span className="sr-only">Send</span>
        </Button>
      </div>
      <div className="flex items-center justify-between mt-3 text-xs text-muted-foreground">
        <div className="flex items-center gap-2">
          <Button type="button" variant="ghost" size="sm" className="h-6 p-2 text-xs text-muted-foreground hover:text-foreground">
            <Paperclip className="h-3 w-3 mr-1" />
            Attach
          </Button>
          <span className="hidden sm:inline">Shift+Enter for new line</span>
          <span className="flex items-center gap-1 ml-2">
            <Sparkles className="h-3 w-3 text-purple-500" />
            <span className="text-xs text-purple-600 dark:text-purple-400">AI powered</span>
          </span>
        </div>
        <div className={cn("text-xs", isStreaming ? "text-orange-600 dark:text-orange-400" : "")}>
          {isStreaming ? (
            <span className="flex items-center gap-1">
              <div className="h-2 w-2 bg-orange-500 rounded-full animate-pulse"></div>
              Thinking...
            </span>
          ) : (
            <span className="text-muted-foreground">Ready</span>
          )}
        </div>
      </div>
    </form>
  );
};

export { ChatInput };