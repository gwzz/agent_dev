import React from "react";
import { Message } from "@/types";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { ToolActionCard } from "@/components/chat/ToolActionCard";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/cjs/styles/prism";

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === "user";
  
  // Install react-markdown and remark-gfm if not already installed
  // npm install react-markdown remark-gfm
  // Install react-syntax-highlighter if not already installed
  // npm install react-syntax-highlighter
  
  return (
    <div className={cn(
      "flex gap-3 mb-6 last:mb-0",
      isUser ? "flex-row-reverse" : "flex-row"
    )}>
      <Avatar className={cn(
        "w-8 h-8 flex-shrink-0",
        isUser ? "order-2" : "order-1"
      )}>
        <AvatarImage 
          src={isUser ? "/user-avatar.png" : "/agent-avatar.png"} 
          alt={isUser ? "User" : "Agent"} 
        />
        <AvatarFallback>{isUser ? "U" : "A"}</AvatarFallback>
      </Avatar>
      
      <div className={cn(
        "max-w-[85%] flex flex-col",
        isUser ? "items-end order-1" : "items-start order-2"
      )}>
        <div className={cn(
          "px-4 py-3 rounded-2xl",
          isUser 
            ? "bg-primary text-primary-foreground rounded-br-md" 
            : "bg-muted text-foreground rounded-bl-md"
        )}>
          {message.toolActions && message.toolActions.length > 0 && (
            <div className="space-y-3 mb-2">
              {message.toolActions.map((toolAction) => (
                <ToolActionCard key={toolAction.id} toolAction={toolAction} />
              ))}
            </div>
          )}
          
          <ReactMarkdown 
            className="prose prose-sm dark:prose-invert max-w-none"
            remarkPlugins={[remarkGfm]}
            components={{
              code({node, className, children, ...props}) {
                const match = /language-(\w+)/.exec(className || '');
                return match ? (
                  <SyntaxHighlighter
                    style={vscDarkPlus}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              }
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        <div className="text-xs text-muted-foreground mt-1 px-1">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

export { ChatMessage };