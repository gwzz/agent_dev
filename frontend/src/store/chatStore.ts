import { create } from "zustand";
import { persist } from "zustand/middleware";
import { Message, Conversation, AgentSettings } from "@/types";
import { apiService } from "@/lib/api";
import { useAgentSettingsStore } from "./agentSettingsStore";

interface ChatStore {
  messages: Message[];
  isStreaming: boolean;
  currentConversationId: string | null;
  conversations: Conversation[];
  sendMessage: (content: string) => Promise<void>;
  appendToken: (token: string) => void;
  setCurrentConversation: (id: string) => void;
  createNewConversation: () => void;
  deleteConversation: (id: string) => void;
  updateConversationTitle: (id: string, title: string) => void;
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      messages: [],
      isStreaming: false,
      currentConversationId: null,
      conversations: [],

      sendMessage: async (content: string) => {
        const newMessage: Message = {
          id: Date.now().toString(),
          content,
          role: "user",
          timestamp: new Date(),
        };

        set((state) => ({
          messages: [...state.messages, newMessage],
          isStreaming: true,
        }));

        try {
          // Call the backend API with the selected agent type
          const { agentType } = useAgentSettingsStore.getState();
          const response = await apiService.sendMessage(content, agentType);

          if (response.status === "success") {
            const assistantMessage: Message = {
              id: (Date.now() + 1).toString(),
              content: response.result.content,
              role: "assistant",
              timestamp: new Date(),
            };

            set((state) => ({
              messages: [...state.messages, assistantMessage],
              isStreaming: false,
            }));
          } else {
            const errorMessage: Message = {
              id: (Date.now() + 1).toString(),
              content: "Sorry, there was an error processing your request. Please try again.",
              role: "assistant",
              timestamp: new Date(),
            };

            set((state) => ({
              messages: [...state.messages, errorMessage],
              isStreaming: false,
            }));
          }
        } catch (error) {
          console.error("Error sending message to backend:", error);

          const errorMessage: Message = {
            id: (Date.now() + 1).toString(),
            content: "Sorry, there was an error connecting to the backend. Please make sure the server is running.",
            role: "assistant",
            timestamp: new Date(),
          };

          set((state) => ({
            messages: [...state.messages, errorMessage],
            isStreaming: false,
          }));
        }
      },

      appendToken: (token: string) => {
        set((state) => {
          if (state.messages.length === 0) return state;

          const lastMessage = state.messages[state.messages.length - 1];
          if (lastMessage.role === "assistant") {
            const updatedMessages = [...state.messages];
            const lastIdx = updatedMessages.length - 1;
            updatedMessages[lastIdx] = {
              ...lastMessage,
              content: lastMessage.content + token,
            };
            return { messages: updatedMessages };
          }

          // If the last message is not from assistant, add a new assistant message
          const newAssistantMessage: Message = {
            id: Date.now().toString(),
            content: token,
            role: "assistant",
            timestamp: new Date(),
          };

          return { messages: [...state.messages, newAssistantMessage] };
        });
      },

      setCurrentConversation: (id: string) => {
        const conversation = get().conversations.find(c => c.id === id);
        if (conversation) {
          set({
            currentConversationId: id,
            messages: conversation.messages,
          });
        }
      },

      createNewConversation: () => {
        const newId = Date.now().toString();
        const newConversation: Conversation = {
          id: newId,
          title: `Conversation ${get().conversations.length + 1}`,
          createdAt: new Date(),
          updatedAt: new Date(),
          messages: [],
        };

        set((state) => ({
          currentConversationId: newId,
          conversations: [...state.conversations, newConversation],
          messages: [],
        }));
      },

      deleteConversation: (id: string) => {
        set((state) => ({
          conversations: state.conversations.filter(c => c.id !== id),
          currentConversationId: state.currentConversationId === id ? null : state.currentConversationId,
          messages: state.currentConversationId === id ? [] : state.messages,
        }));
      },

      updateConversationTitle: (id: string, title: string) => {
        set((state) => ({
          conversations: state.conversations.map(c =>
            c.id === id ? { ...c, title, updatedAt: new Date() } : c
          ),
        }));
      },
    }),
    {
      name: "chat-storage",
    }
  )
);