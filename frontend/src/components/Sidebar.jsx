import { formatDistanceToNow } from "date-fns";
import { fr } from "date-fns/locale";
import { FolderPlus, MessageSquare, Trash2 } from "lucide-react";
import { useState } from "react";
import FolderTree from "./FolderTree";

export default function Sidebar({
  conversations,
  folders = [],
  onSelectConversation,
  onDeleteConversation,
  onNewConversation,
  currentConversationId,
  onCreateFolder,
  onDeleteFolder,
  onRenameFolder,
  onMoveConversation,
}) {
  const [showNewFolderInput, setShowNewFolderInput] = useState(false);
  const [newFolderName, setNewFolderName] = useState("");

  const handleCreateFolder = () => {
    if (newFolderName.trim()) {
      onCreateFolder(newFolderName.trim());
      setNewFolderName("");
      setShowNewFolderInput(false);
    }
  };

  const handleDropConversation = (conversationId, folderId) => {
    onMoveConversation(conversationId, folderId);
  };

  const handleDropToRoot = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const conversationId = parseInt(e.dataTransfer.getData("conversationId"));
    if (conversationId) {
      onMoveConversation(conversationId, null);
    }
    e.currentTarget.classList.remove("bg-white/20");
  };

  const handleDragOverRoot = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add("bg-white/20");
  };

  const handleDragLeaveRoot = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove("bg-white/20");
  };

  const uncategorizedConversations = conversations.filter((c) => !c.folder);

  return (
    <div className="w-64 bg-sidebar-bg text-white flex flex-col h-screen">
      <div className="p-4 border-b border-gray-700 space-y-2">
        <button
          onClick={onNewConversation}
          className="w-full bg-transparent border border-white/20 hover:bg-white/10 text-white rounded-lg p-3 flex items-center justify-center gap-2"
        >
          <MessageSquare size={20} />
          <span>Nouvelle conversation</span>
        </button>

        <button
          onClick={() => setShowNewFolderInput(true)}
          className="w-full bg-transparent border border-white/20 hover:bg-white/10 text-white rounded-lg p-3 flex items-center justify-center gap-2"
        >
          <FolderPlus size={20} />
          <span>Nouveau dossier</span>
        </button>

        {showNewFolderInput && (
          <div className="flex gap-2">
            <input
              type="text"
              value={newFolderName}
              onChange={(e) => setNewFolderName(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleCreateFolder()}
              placeholder="Nom du dossier"
              className="flex-1 bg-white/10 border border-white/20 rounded-lg p-2 text-sm text-white placeholder-gray-400"
              autoFocus
            />
            <button
              onClick={handleCreateFolder}
              className="bg-blue-600 hover:bg-blue-700 rounded-lg px-3 text-sm font-medium"
            >
              OK
            </button>
            <button
              onClick={() => {
                setShowNewFolderInput(false);
                setNewFolderName("");
              }}
              className="bg-gray-600 hover:bg-gray-700 rounded-lg px-3 text-sm font-medium"
            >
              ✕
            </button>
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto">
        {/* Dossiers */}
        {folders.map((folder) => (
          <FolderTree
            key={folder.id}
            folder={folder}
            conversations={conversations}
            currentConversationId={currentConversationId}
            onSelectConversation={onSelectConversation}
            onDeleteConversation={onDeleteConversation}
            onDropConversation={handleDropConversation}
            onDeleteFolder={onDeleteFolder}
            onRenameFolder={onRenameFolder}
          />
        ))}

        {/* Conversations non classées */}
        {uncategorizedConversations.length > 0 && (
          <div
            className="mt-4 border-t border-gray-700 pt-2"
            onDrop={handleDropToRoot}
            onDragOver={handleDragOverRoot}
            onDragLeave={handleDragLeaveRoot}
          >
            <div className="px-3 py-2 text-xs text-gray-400 font-semibold">
              NON CLASSÉES
            </div>
            {uncategorizedConversations.map((conv) => (
              <div
                key={conv.id}
                draggable
                onDragStart={(e) => {
                  e.dataTransfer.setData("conversationId", conv.id.toString());
                }}
                onClick={() => onSelectConversation(conv.id)}
                className={`p-3 cursor-pointer hover:bg-white/10 flex items-center justify-between group ${
                  currentConversationId === conv.id ? "bg-white/20" : ""
                }`}
              >
                <div className="flex-1 min-w-0">
                  <div className="font-medium truncate">
                    {conv.title || "Sans titre"}
                  </div>
                  <div className="text-xs text-gray-400">
                    {formatDistanceToNow(new Date(conv.updated_at), {
                      locale: fr,
                      addSuffix: true,
                    })}
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (
                      confirm(
                        `Supprimer la conversation "${conv.title || "Sans titre"}" ?`,
                      )
                    ) {
                      onDeleteConversation(conv.id);
                    }
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-500"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
