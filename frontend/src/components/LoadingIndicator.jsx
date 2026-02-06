export default function LoadingIndicator() {
  return (
    <div className="flex gap-4 bg-input-bg p-4 rounded-lg">
      <div className="flex-shrink-0">
        <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
          <Bot size={18} />
        </div>
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className="font-semibold text-white">Agent</span>
        </div>
        <div className="flex gap-1 items-center">
          <span
            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
            style={{ animationDelay: "0ms" }}
          ></span>
          <span
            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
            style={{ animationDelay: "150ms" }}
          ></span>
          <span
            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
            style={{ animationDelay: "300ms" }}
          ></span>
        </div>
      </div>
    </div>
  );
}
