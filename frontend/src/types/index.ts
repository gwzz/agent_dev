export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
  toolActions?: ToolAction[];
}

export interface ToolAction {
  id: string;
  name: string;
  status: "pending" | "running" | "completed" | "error";
  result?: any;
  progress?: number;
}

export interface Conversation {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
  messages: Message[];
}

export type AgentType = "city-info" | "crypto" | "law";

export interface AgentSettings {
  model: string;
  temperature: number;
  maxTokens: number;
  agentType: AgentType;
}