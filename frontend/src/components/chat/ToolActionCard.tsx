import React from "react";
import { ToolAction } from "@/types";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

interface ToolActionCardProps {
  toolAction: ToolAction;
}

const ToolActionCard: React.FC<ToolActionCardProps> = ({ toolAction }) => {
  const getStatusColor = () => {
    switch (toolAction.status) {
      case "completed":
        return "text-green-500";
      case "error":
        return "text-red-500";
      case "running":
        return "text-blue-500";
      default:
        return "text-gray-500";
    }
  };

  const getStatusText = () => {
    switch (toolAction.status) {
      case "pending":
        return "Pending";
      case "running":
        return "Running";
      case "completed":
        return "Completed";
      case "error":
        return "Error";
      default:
        return "Unknown";
    }
  };

  return (
    <Card className={cn(
      "w-full overflow-hidden",
      toolAction.status === "error" && "border-red-500/50"
    )}>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium">{toolAction.name}</CardTitle>
          <span className={`text-xs font-medium ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </div>
        <CardDescription className="text-xs">
          Executing tool action
        </CardDescription>
      </CardHeader>
      <CardContent className="pb-3">
        {toolAction.status === "running" && toolAction.progress !== undefined && (
          <div className="mb-2">
            <Progress value={toolAction.progress} className="h-1.5" />
          </div>
        )}
        
        {toolAction.result && (
          <div className="text-xs p-2 bg-muted rounded-md mt-2 max-h-32 overflow-y-auto">
            <pre className="whitespace-pre-wrap break-words">
              {typeof toolAction.result === 'string' 
                ? toolAction.result 
                : JSON.stringify(toolAction.result, null, 2)}
            </pre>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export { ToolActionCard };