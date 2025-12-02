import React from "react";
import { 
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { 
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Slider } from "@/components/ui/slider";
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useUIStore } from "@/store/uiStore";
import { useAgentSettingsStore } from "@/store/agentSettingsStore";
import { useChatStore } from "@/store/chatStore";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

const Sidebar = () => {
  const { sidebarOpen, setSidebarOpen } = useUIStore();
  const { 
    model, 
    temperature, 
    maxTokens, 
    setModel, 
    setTemperature, 
    setMaxTokens 
  } = useAgentSettingsStore();
  const { createNewConversation } = useChatStore();
  const { setTheme, theme } = useTheme();

  const handleClearChat = () => {
    createNewConversation();
    setSidebarOpen(false);
  };

  return (
    <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
      <SheetContent side="left" className="w-[350px] sm:w-[400px]">
        <SheetHeader>
          <SheetTitle>Agent Settings</SheetTitle>
        </SheetHeader>
        
        <div className="flex flex-col gap-6 py-4 overflow-y-auto">
          <Card>
            <CardHeader>
              <CardTitle>Agent Information</CardTitle>
              <CardDescription>
                Configure your AI agent preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="model">Model</Label>
                <Select value={model} onValueChange={setModel}>
                  <SelectTrigger id="model">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="gemini-3-pro-preview">Gemini Pro</SelectItem>
                    <SelectItem value="gpt-4">GPT-4</SelectItem>
                    <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                    <SelectItem value="claude-3-opus">Claude 3 Opus</SelectItem>
                    <SelectItem value="claude-3-sonnet">Claude 3 Sonnet</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label>Temperature: {temperature.toFixed(1)}</Label>
                <Slider
                  id="temperature"
                  min={0}
                  max={1}
                  step={0.1}
                  value={[temperature]}
                  onValueChange={([value]) => setTemperature(value)}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Precise</span>
                  <span>Balanced</span>
                  <span>Creative</span>
                </div>
              </div>
              
              <div className="space-y-2">
                <Label>Max Tokens: {maxTokens}</Label>
                <Slider
                  id="maxTokens"
                  min={128}
                  max={8192}
                  step={128}
                  value={[maxTokens]}
                  onValueChange={([value]) => setMaxTokens(value)}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Short</span>
                  <span>Medium</span>
                  <span>Long</span>
                </div>
              </div>
              
              <Separator />
              
              <div className="space-y-2">
                <Label>Theme</Label>
                <div className="flex items-center gap-3">
                  <Button
                    variant={theme === "light" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setTheme("light")}
                    className="flex items-center gap-2"
                  >
                    <Sun className="h-4 w-4" />
                    Light
                  </Button>
                  <Button
                    variant={theme === "dark" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setTheme("dark")}
                    className="flex items-center gap-2"
                  >
                    <Moon className="h-4 w-4" />
                    Dark
                  </Button>
                  <Button
                    variant={theme === "system" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setTheme("system")}
                    className="flex items-center gap-2"
                  >
                    System
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>About Agent</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                This is an AI assistant that can help you with various tasks. 
                It can access real-time information and use tools to perform 
                complex operations.
              </p>
            </CardContent>
          </Card>
          
          <div className="pt-4">
            <Button 
              onClick={handleClearChat}
              variant="destructive"
              className="w-full"
            >
              Clear Chat History
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
};

export { Sidebar };