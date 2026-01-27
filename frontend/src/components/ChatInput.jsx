import { Send } from "lucide-react";
import { useState } from "react";

export default function ChatInput({ onSendMessage, disabled }) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage("");
    }
  };

  return (
    <div className="border-t border-gray-700 p-4 bg-chat-bg">
      <form onSubmit={handleSubmit} className="flex gap-3">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Écrivez votre message..."
          disabled={disabled}
          className="flex-1 bg-input-bg text-white rounded-lg px-4 py-3 border border-gray-600 focus:outline-none focus:border-gray-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg px-6 py-3 flex items-center gap-2 transition-colors"
        >
          <Send size={18} />
          <span>Envoyer</span>
        </button>
      </form>
    </div>
  );
}
