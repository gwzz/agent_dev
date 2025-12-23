import { Message, AgentType } from "@/types";

interface QueryRequest {
  query: string;
}

interface ApiResponse {
  status: string;
  result: {
    content: string;
    usage?: {
      prompt_tokens: number;
      completion_tokens: number;
      total_tokens: number;
    };
  };
}

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

/**
 * Service to communicate with the backend AI agents
 */
class ApiService {
  /**
   * Send a message to the city info agent
   */
  async sendToCityInfoAgent(query: string): Promise<ApiResponse> {
    try {
      const response = await fetch(`${BACKEND_URL}/city-info`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error calling city info agent:", error);
      throw error;
    }
  }

  /**
   * Send a message to the crypto agent
   */
  async sendToCryptoAgent(query: string): Promise<ApiResponse> {
    try {
      const response = await fetch(`${BACKEND_URL}/crypto`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error calling crypto agent:", error);
      throw error;
    }
  }

  /**
   * Send a message to the law agent
   */
  async sendToLawAgent(query: string): Promise<ApiResponse> {
    try {
      const response = await fetch(`${BACKEND_URL}/law`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error calling law agent:", error);
      throw error;
    }
  }

  /**
   * Generic method to send a message to the selected agent type
   */
  async sendMessage(query: string, agentType: AgentType = "city-info"): Promise<ApiResponse> {
    switch (agentType) {
      case "city-info":
        return this.sendToCityInfoAgent(query);
      case "crypto":
        return this.sendToCryptoAgent(query);
      case "law":
        return this.sendToLawAgent(query);
      default:
        return this.sendToCityInfoAgent(query);
    }
  }
}

export const apiService = new ApiService();