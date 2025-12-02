import { create } from "zustand";

interface UIStore {
  sidebarOpen: boolean;
  historyOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  toggleHistory: () => void;
  setHistoryOpen: (open: boolean) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: false,
  historyOpen: false,
  
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  
  toggleHistory: () => set((state) => ({ historyOpen: !state.historyOpen })),
  setHistoryOpen: (open) => set({ historyOpen: open }),
}));