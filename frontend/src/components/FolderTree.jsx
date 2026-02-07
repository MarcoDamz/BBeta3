import { formatDistanceToNow } from "date-fns";
import { fr } from "date-fns/locale";
import {
  ChevronDown,
  ChevronRight,
  Folder,
  FolderOpen,
  MoreVertical,
  Trash2,
} from "lucide-react";
import { useState } from "react";

export default function FolderTree({
  folder,
  conversations,
  currentConversationId,
  onSelectConversation,
  onDeleteConversation,
  onDropConversation,
  onDeleteFolder,
  onRenameFolder,
}) {
  const [isOpen, setIsOpen] = useState(true);
  const [showMenu, setShowMenu] = useState(false);

  const folderConversations = conversations.filter(
    (c) => c.folder === folder.id,
  );

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const conversationId = parseInt(e.dataTransfer.getData("conversationId"));
    if (conversationId) {
      onDropConversation(conversationId, folder.id);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add("bg-white/20");
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove("bg-white/20");
  };

  return (
    <div className="folder-tree">
      <div
        className="flex items-center justify-between p-2 hover:bg-white/10 cursor-pointer group relative"
        onDrop={(e) => {
          handleDrop(e);
          e.currentTarget.classList.remove("bg-white/20");
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <div
          className="flex items-center gap-2 flex-1"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          {isOpen ? <FolderOpen size={16} /> : <Folder size={16} />}
          <span className="text-sm font-medium">{folder.name}</span>
          <span className="text-xs text-gray-400">
            ({folderConversations.length})
          </span>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            setShowMenu(!showMenu);
          }}
          className="opacity-0 group-hover:opacity-100 p-1 hover:bg-white/20 rounded"
        >
          <MoreVertical size={14} />
        </button>

        {showMenu && (
          <div className="absolute right-2 top-8 bg-gray-800 rounded-lg shadow-lg z-10 py-1 min-w-[120px]">
            <button
              onClick={() => {
                onRenameFolder(folder.id, folder.name);
                setShowMenu(false);
              }}
              className="w-full text-left px-4 py-2 hover:bg-white/10 text-sm"
            >
              Renommer
            </button>
            <button
              onClick={() => {
                if (
                  confirm(
                    `Supprimer le dossier "${folder.name}" ? Les conversations ne seront pas supprimées.`,
                  )
                ) {
                  onDeleteFolder(folder.id);
                }
                setShowMenu(false);
              }}
              className="w-full text-left px-4 py-2 hover:bg-white/10 text-sm text-red-500"
            >
              Supprimer
            </button>
          </div>
        )}
      </div>

      {isOpen && (
        <div className="ml-4">
          {folderConversations.map((conv) => (
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
                <div className="font-medium truncate text-sm">
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
  );
}
