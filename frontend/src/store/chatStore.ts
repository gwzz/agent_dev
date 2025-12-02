import { create } from "zustand";
import { persist } from "zustand/middleware";
import { Message, Conversation, AgentSettings } from "@/types";

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

        // In a real app, this would connect to your backend
        // For now, we'll simulate a response
        setTimeout(() => {
          const assistantMessage: Message = {
            id: (Date.now() + 1).toString(),
            content: `This is a simulated response to: "${content}". In a real implementation, this would connect to your Python agents.`,
            role: "assistant",
            timestamp: new Date(),
          };

          set((state) => ({
            messages: [...state.messages, assistantMessage],
            isStreaming: false,
          }));
        }, 1000);
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