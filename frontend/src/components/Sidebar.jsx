import { formatDistanceToNow } from "date-fns";
import { fr } from "date-fns/locale";
import { MessageSquare, Trash2 } from "lucide-react";

export default function Sidebar({
  conversations,
  onSelectConversation,
  onDeleteConversation,
  onNewConversation,
  currentConversationId,
}) {
  return (
    <div className="w-64 bg-sidebar-bg text-white flex flex-col h-screen">
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={onNewConversation}
          className="w-full bg-transparent border border-white/20 hover:bg-white/10 text-white rounded-lg p-3 flex items-center justify-center gap-2"
        >
          <MessageSquare size={20} />
          <span>Nouvelle conversation</span>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {conversations.map((conv) => (
          <div
            key={conv.id}
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
                onDeleteConversation(conv.id);
              }}
              className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-500"
            >
              <Trash2 size={16} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
