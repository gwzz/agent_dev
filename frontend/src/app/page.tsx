"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { 
  Menu, 
  Settings, 
  MessageSquare 
} from "lucide-react";
import { useUIStore } from "@/store/uiStore";
import { ChatMessageList } from "@/components/chat/ChatMessageList";
import { ChatInput } from "@/components/chat/ChatInput";
import { Sidebar } from "@/components/chat/Sidebar";
import { HistoryDrawer } from "@/components/chat/HistoryDrawer";
import { useChatStore } from "@/store/chatStore";

export default function HomePage() {
  const { setSidebarOpen, setHistoryOpen } = useUIStore();
  const { messages, isStreaming } = useChatStore();

  React.useEffect(() => {
    // Initialize a new conversation if none exists
    if (useChatStore.getState().currentConversationId === null) {
      useChatStore.getState().createNewConversation();
    }
  }, []);

  return (
    <div className="flex flex-col h-screen bg-background">
      <header className="border-b py-2 px-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button 
            variant="ghost" 
            size="icon"
            onClick={() => setHistoryOpen(true)}
            className="md:hidden"
          >
            <MessageSquare className="h-5 w-5" />
          </Button>
          <h1 className="text-xl font-bold">Agent Chat</h1>
        </div>
        
        <div className="flex items-center gap-2">
          <Button 
            variant="ghost" 
            size="icon"
            onClick={() => setHistoryOpen(true)}
            className="hidden md:flex"
          >
            <MessageSquare className="h-5 w-5" />
          </Button>
          
          <Button 
            variant="ghost" 
            size="icon"
            onClick={() => setSidebarOpen(true)}
          >
            <Settings className="h-5 w-5" />
          </Button>
        </div>
      </header>
      
      <div className="flex flex-1 overflow-hidden">
        <HistoryDrawer />
        <Sidebar />
        
        <main className="flex-1 flex flex-col">
          <ChatMessageList 
            messages={messages} 
            isStreaming={isStreaming} 
          />
          <ChatInput />
        </main>
      </div>
    </div>
  );
}