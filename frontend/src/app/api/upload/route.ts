import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  try {
    // In a real implementation, this would handle file uploads
    // For now, return a mock response
    const formData = await req.formData();
    const file = formData.get('file') as File | null;
    
    if (!file) {
      return new Response(
        JSON.stringify({ error: "No file provided" }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return new Response(
      JSON.stringify({ 
        success: true, 
        fileName: file.name,
        size: file.size,
        type: file.type,
        message: `File ${file.name} uploaded successfully`
      }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("Error in upload API:", error);
    return new Response(
      JSON.stringify({ error: "Failed to upload file" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}