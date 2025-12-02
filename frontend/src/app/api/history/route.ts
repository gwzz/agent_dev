import { NextRequest } from "next/server";
import { Conversation } from "@/types";

// Mock data for demonstration
let mockConversations: Conversation[] = [
  {
    id: "1",
    title: "Bitcoin Price Inquiry",
    createdAt: new Date(Date.now() - 86400000), // 1 day ago
    updatedAt: new Date(Date.now() - 3600000), // 1 hour ago
    messages: [
      {
        id: "1-1",
        content: "What is the current price of Bitcoin?",
        role: "user",
        timestamp: new Date(Date.now() - 3600000),
      },
      {
        id: "1-2",
        content: "Based on current market data, Bitcoin is trading at approximately $87,000.",
        role: "assistant",
        timestamp: new Date(Date.now() - 3590000),
      }
    ]
  },
  {
    id: "2",
    title: "Weather in London",
    createdAt: new Date(Date.now() - 172800000), // 2 days ago
    updatedAt: new Date(Date.now() - 1200000), // 20 minutes ago
    messages: [
      {
        id: "2-1",
        content: "What's the weather in London?",
        role: "user",
        timestamp: new Date(Date.now() - 1200000),
      },
      {
        id: "2-2",
        content: "The current weather in London is partly cloudy with a temperature of 18°C.",
        role: "assistant",
        timestamp: new Date(Date.now() - 1190000),
      }
    ]
  }
];

export async function GET(req: NextRequest) {
  try {
    // In a real implementation, this would fetch from a database
    // For now, return mock data
    return new Response(JSON.stringify(mockConversations), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    console.error("Error in history API:", error);
    return new Response(
      JSON.stringify({ error: "Failed to fetch history" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}

export async function DELETE(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const id = searchParams.get('id');
    
    if (!id) {
      return new Response(
        JSON.stringify({ error: "Conversation ID is required" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // In a real implementation, this would delete from a database
    // For now, remove from mock data
    mockConversations = mockConversations.filter(conv => conv.id !== id);
    
    return new Response(
      JSON.stringify({ success: true, message: "Conversation deleted" }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("Error in delete history API:", error);
    return new Response(
      JSON.stringify({ error: "Failed to delete conversation" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}