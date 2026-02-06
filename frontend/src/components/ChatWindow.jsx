import { format } from "date-fns";
import { Bot, User } from "lucide-react";
import { useEffect, useRef } from "react";

export default function ChatWindow({ messages, isLoading }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-400">
          <div className="text-center">
            <Bot size={48} className="mx-auto mb-4 opacity-50" />
            <p>Sélectionnez un agent et commencez une conversation</p>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-4 ${
                message.role === "human" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`flex gap-3 max-w-[75%] ${
                  message.role === "human"
                    ? "bg-blue-600/20 border border-blue-500/30"
                    : "bg-input-bg border border-gray-700"
                } p-4 rounded-lg`}
              >
                {message.role === "ai" && (
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                      <Bot size={18} />
                    </div>
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-semibold text-white">
                      {message.role === "human"
                        ? "Vous"
                        : message.agent_name || "Agent"}
                    </span>
                    <span className="text-xs text-gray-400">
                      {format(new Date(message.created_at), "HH:mm")}
                    </span>
                    {message.is_auto_chat && (
                      <span className="text-xs bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded">
                        AUTO
                      </span>
                    )}
                  </div>
                  <div className="text-gray-200 whitespace-pre-wrap">
                    {message.content}
                  </div>
                </div>
                {message.role === "human" && (
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                      <User size={18} />
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex gap-4 justify-start">
              <div className="flex gap-3 max-w-[75%] bg-input-bg border border-gray-700 p-4 rounded-lg">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <Bot size={18} />
                  </div>
                </div>
                <div className="flex items-center">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}
