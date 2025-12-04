import React from "react";
import { Message } from "@/types";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { ToolActionCard } from "@/components/chat/ToolActionCard";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { User, Bot } from "lucide-react";

const syntaxTheme = vscDarkPlus as any;

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === "user";
  const timestamp = message.timestamp instanceof Date
    ? message.timestamp
    : new Date(message.timestamp);
  const renderedTime = Number.isNaN(timestamp.getTime())
    ? "--:--"
    : timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  return (
    <div className={cn(
      "flex gap-3 mb-6 last:mb-0 py-2",
      isUser ? "flex-row-reverse" : "flex-row"
    )}>
      <div className={cn(
        "w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-full",
        isUser
          ? "order-2 bg-primary text-primary-foreground"
          : "order-1 bg-secondary text-secondary-foreground"
      )}>
        {isUser ? (
          <User className="h-4 w-4" />
        ) : (
          <Bot className="h-4 w-4" />
        )}
      </div>

      <div className={cn(
        "flex-1 flex flex-col max-w-[85%]",
        isUser ? "items-end order-1" : "items-start order-2"
      )}>
        <div className={cn(
          "px-4 py-3 rounded-2xl shadow-sm",
          isUser
            ? "bg-primary text-primary-foreground rounded-br-md"
            : "bg-card text-foreground rounded-bl-md border"
        )}>
          {message.toolActions && message.toolActions.length > 0 && (
            <div className="space-y-3 mb-2">
              {message.toolActions.map((toolAction) => (
                <ToolActionCard key={toolAction.id} toolAction={toolAction} />
              ))}
            </div>
          )}

          <div className="prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({node, className, children, ...props}) {
                  const match = /language-(\w+)/.exec(className || '')
                  return match ? (
                    <SyntaxHighlighter
                      style={syntaxTheme}
                      language={match[1]}
                      PreTag="div"
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  )
                }
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
        <div className="text-xs text-muted-foreground mt-1 px-1 ml-2">
          {renderedTime}
        </div>
      </div>
    </div>
  );
};

export { ChatMessage };