import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AgentSettings, AgentType } from "@/types";

interface AgentSettingsStore extends AgentSettings {
  setModel: (model: string) => void;
  setTemperature: (temp: number) => void;
  setMaxTokens: (maxTokens: number) => void;
  setAgentType: (agentType: AgentType) => void;
}

export const useAgentSettingsStore = create<AgentSettingsStore>()(
  persist(
    (set) => ({
      model: "gemini-3-pro-preview",
      temperature: 0.7,
      maxTokens: 2048,
      agentType: "city-info",

      setModel: (model) => set({ model }),
      setTemperature: (temperature) => set({ temperature }),
      setMaxTokens: (maxTokens) => set({ maxTokens }),
      setAgentType: (agentType) => set({ agentType }),
    }),
    {
      name: "agent-settings-storage",
    }
  )
);