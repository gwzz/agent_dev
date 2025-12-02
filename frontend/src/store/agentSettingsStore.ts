import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AgentSettings } from "@/types";

interface AgentSettingsStore extends AgentSettings {
  setModel: (model: string) => void;
  setTemperature: (temp: number) => void;
  setMaxTokens: (maxTokens: number) => void;
}

export const useAgentSettingsStore = create<AgentSettingsStore>()(
  persist(
    (set) => ({
      model: "gemini-3-pro-preview",
      temperature: 0.7,
      maxTokens: 2048,
      
      setModel: (model) => set({ model }),
      setTemperature: (temperature) => set({ temperature }),
      setMaxTokens: (maxTokens) => set({ maxTokens }),
    }),
    {
      name: "agent-settings-storage",
    }
  )
);