import { LogOut, Menu, Settings, Zap } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useStore } from "../store/useStore";
import AutoChatModal from "./AutoChatModal";

export default function Header({ agents, onToggleSidebar }) {
  const navigate = useNavigate();
  const { user, logout } = useStore();
  const [showAutoChat, setShowAutoChat] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <>
      <div className="bg-chat-bg border-b border-gray-700 p-4 flex items-center justify-between text-white">
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="p-2 hover:bg-white/10 rounded-lg"
          >
            <Menu size={20} />
          </button>
        </div>

        <div className="flex items-center gap-3">
          {user && (
            <span className="text-sm text-gray-300">👤 {user.username}</span>
          )}

          {/* Bouton Auto-Chat - visible uniquement pour les admins */}
          {user &&
            (user.is_admin ||
              user.is_staff ||
              user.is_superuser ||
              (user.groups && user.groups.includes("Administrators"))) && (
              <button
                onClick={() => setShowAutoChat(true)}
                className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition"
                title="Mode Auto-Chat"
              >
                <Zap size={18} />
                <span className="hidden md:inline">Auto-Chat</span>
              </button>
            )}

          {/* Bouton Admin - visible uniquement pour les admins */}
          {user &&
            (user.is_admin ||
              user.is_staff ||
              user.is_superuser ||
              (user.groups && user.groups.includes("Administrators"))) && (
              <button
                onClick={() => navigate("/admin")}
                className="flex items-center gap-2 bg-transparent border border-white/20 hover:bg-white/10 px-4 py-2 rounded-lg"
              >
                <Settings size={18} />
                <span className="hidden md:inline">Admin</span>
              </button>
            )}

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition"
            title="Déconnexion"
          >
            <LogOut size={18} />
            <span className="hidden md:inline">Déconnexion</span>
          </button>
        </div>
      </div>

      {/* Modal Auto-Chat */}
      {showAutoChat && (
        <AutoChatModal agents={agents} onClose={() => setShowAutoChat(false)} />
      )}
    </>
  );
}
