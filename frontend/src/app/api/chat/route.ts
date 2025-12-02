import { NextRequest } from "next/server";
import { Message } from "@/types";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { message, conversationId } = body;

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // In a real implementation, this would connect to your Python agents
    // For now, return a mock response based on the input message
    const mockResponse = generateMockResponse(message);

    const responseMessage: Message = {
      id: Date.now().toString(),
      content: mockResponse,
      role: "assistant",
      timestamp: new Date(),
    };

    return new Response(JSON.stringify(responseMessage), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("Error in chat API:", error);
    return new Response(
      JSON.stringify({ error: "Failed to process message" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}

function generateMockResponse(userMessage: string): string {
  const lowerMessage = userMessage.toLowerCase();
  
  if (lowerMessage.includes("bitcoin") || lowerMessage.includes("crypto")) {
    // In a real implementation, this would call your crypto agent
    return "Based on current market data, Bitcoin is trading at approximately $87,000 with a market cap of around $1.7 trillion. The 24-hour trading volume is about $45 billion.";
  } else if (lowerMessage.includes("weather") || lowerMessage.includes("temperature")) {
    // In a real implementation, this would call your city info agent
    return "I can help with weather information. Please specify which city you'd like weather information for. For example, 'What's the weather in London?'";
  } else if (lowerMessage.includes("time") || lowerMessage.includes("date")) {
    // In a real implementation, this would call your city info agent
    return `The current time is ${new Date().toLocaleTimeString()} and the date is ${new Date().toLocaleDateString()}. If you need time for a specific city, please specify which city.`;
  } else if (lowerMessage.includes("population")) {
    // In a real implementation, this would call your city info agent
    return "I can help with population information. Please specify which city you'd like population information for. For example, 'What's the population of Shanghai?'";
  } else {
    return `I received your message: "${userMessage}". In a real implementation, this would be processed by an AI agent that can interact with your Python backend services. The agent has access to tools for cryptocurrency prices, city information (weather, time, population, coordinates), and more.`;
  }
}