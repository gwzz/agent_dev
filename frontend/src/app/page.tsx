"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import {
  Menu,
  Settings,
  MessageSquare
} from "lucide-react";
import { Globe, Bitcoin, Scale } from "lucide-react";
import { useUIStore } from "@/store/uiStore";
import { ChatMessageList } from "@/components/chat/ChatMessageList";
import { ChatInput } from "@/components/chat/ChatInput";
import { Sidebar } from "@/components/chat/Sidebar";
import { HistoryDrawer } from "@/components/chat/HistoryDrawer";
import { useChatStore } from "@/store/chatStore";
import { useAgentSettingsStore } from "@/store/agentSettingsStore";
import { AgentType } from "@/types";

export default function HomePage() {
  const { setSidebarOpen, setHistoryOpen } = useUIStore();
  const { messages, isStreaming } = useChatStore();
  const { agentType } = useAgentSettingsStore();

  React.useEffect(() => {
    // Initialize a new conversation if none exists
    if (useChatStore.getState().currentConversationId === null) {
      useChatStore.getState().createNewConversation();
    }
  }, []);

  // Get agent type display info
  const getAgentInfo = (type: AgentType) => {
    switch (type) {
      case "city-info":
        return { icon: <Globe className="h-4 w-4" />, label: "City Info", color: "text-blue-500" };
      case "crypto":
        return { icon: <Bitcoin className="h-4 w-4" />, label: "Crypto", color: "text-orange-500" };
      case "law":
        return { icon: <Scale className="h-4 w-4" />, label: "Legal", color: "text-purple-500" };
      default:
        return { icon: <Globe className="h-4 w-4" />, label: "Agent", color: "text-blue-500" };
    }
  };

  const agentInfo = getAgentInfo(agentType);

  return (
    <div className="flex flex-col h-screen bg-background">
      <header className="border-b py-3 px-4 flex items-center justify-between bg-card">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setHistoryOpen(true)}
            className="md:hidden"
          >
            <MessageSquare className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-lg md:text-xl font-bold">Agent Chat</h1>
            <div className="flex items-center gap-2 text-sm">
              <span className={`inline-flex items-center gap-1 ${agentInfo.color}`}>
                {agentInfo.icon}
                <span className="font-medium">{agentInfo.label} Agent</span>
              </span>
            </div>
          </div>
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

        <main className="flex-1 flex flex-col bg-muted/5">
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