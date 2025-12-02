import React, { useState } from "react";
import { 
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { 
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { 
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { 
  MoreHorizontal,
  MessageSquarePlus,
  Trash,
  Edit3
} from "lucide-react";
import { useUIStore } from "@/store/uiStore";
import { useChatStore } from "@/store/chatStore";
import { Conversation } from "@/types";

const HistoryDrawer = () => {
  const { historyOpen, setHistoryOpen } = useUIStore();
  const { 
    conversations, 
    setCurrentConversation, 
    deleteConversation, 
    updateConversationTitle 
  } = useChatStore();
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [editingConversationId, setEditingConversationId] = useState<string | null>(null);
  const [tempTitle, setTempTitle] = useState("");

  const handleEditTitle = (conversation: Conversation) => {
    setEditingConversationId(conversation.id);
    setTempTitle(conversation.title);
    setEditDialogOpen(true);
  };

  const handleSaveTitle = () => {
    if (editingConversationId) {
      updateConversationTitle(editingConversationId, tempTitle);
      setEditDialogOpen(false);
      setEditingConversationId(null);
      setTempTitle("");
    }
  };

  const handleDelete = () => {
    if (editingConversationId) {
      deleteConversation(editingConversationId);
      setDeleteDialogOpen(false);
      setEditingConversationId(null);
    }
  };

  return (
    <>
      <Sheet open={historyOpen} onOpenChange={setHistoryOpen}>
        <SheetContent side="left" className="w-[300px] sm:w-[350px]">
          <SheetHeader>
            <SheetTitle>Chat History</SheetTitle>
          </SheetHeader>
          
          <div className="flex flex-col gap-3 py-4">
            <Button 
              onClick={() => {
                useChatStore.getState().createNewConversation();
                setHistoryOpen(false);
              }}
              variant="outline"
              className="w-full justify-start"
            >
              <MessageSquarePlus className="h-4 w-4 mr-2" />
              New Chat
            </Button>
            
            <div className="mt-2">
              <h3 className="text-sm font-medium mb-2 px-1">Recent Chats</h3>
              
              {conversations.length === 0 ? (
                <p className="text-sm text-muted-foreground px-1">
                  No chat history yet
                </p>
              ) : (
                <div className="space-y-1">
                  {conversations
                    .sort((a, b) => 
                      new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
                    )
                    .map((conversation) => (
                      <div 
                        key={conversation.id}
                        className="flex items-center justify-between p-2 hover:bg-accent rounded-md group"
                      >
                        <Button
                          variant="ghost"
                          className="flex-1 justify-start text-left h-auto py-2 px-2"
                          onClick={() => {
                            setCurrentConversation(conversation.id);
                            setHistoryOpen(false);
                          }}
                        >
                          <span className="truncate text-sm">
                            {conversation.title}
                          </span>
                        </Button>
                        
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button 
                              variant="ghost" 
                              size="icon"
                              className="h-8 w-8 opacity-0 group-hover:opacity-100"
                            >
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem 
                              onClick={() => handleEditTitle(conversation)}
                            >
                              <Edit3 className="h-4 w-4 mr-2" />
                              Rename
                            </DropdownMenuItem>
                            <DropdownMenuItem 
                              onClick={() => {
                                setEditingConversationId(conversation.id);
                                setDeleteDialogOpen(true);
                              }}
                              className="text-red-600"
                            >
                              <Trash className="h-4 w-4 mr-2" />
                              Delete
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    ))}
                </div>
              )}
            </div>
          </div>
        </SheetContent>
      </Sheet>
      
      {/* Edit Title Dialog */}
      <AlertDialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Rename Conversation</AlertDialogTitle>
            <input
              type="text"
              value={tempTitle}
              onChange={(e) => setTempTitle(e.target.value)}
              className="w-full p-2 border rounded-md"
              placeholder="Enter new title"
              autoFocus
            />
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => setEditingConversationId(null)}>
              Cancel
            </AlertDialogCancel>
            <AlertDialogAction onClick={handleSaveTitle}>
              Save
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
      
      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete this conversation and cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction 
              onClick={handleDelete}
              className="bg-destructive hover:bg-destructive/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
};

export { HistoryDrawer };