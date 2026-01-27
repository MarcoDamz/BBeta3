import { useEffect, useState } from "react";
import ChatInput from "../components/ChatInput";
import ChatWindow from "../components/ChatWindow";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import { agentsAPI, conversationsAPI } from "../services/api";
import { useStore } from "../store/useStore";

export default function ChatPage() {
  const {
    agents,
    setAgents,
    selectedAgent,
    setSelectedAgent,
    conversations,
    setConversations,
    currentConversation,
    setCurrentConversation,
    messages,
    setMessages,
    addMessage,
    isSidebarOpen,
    toggleSidebar,
  } = useStore();

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadAgents();
    loadConversations();
  }, []);

  const loadAgents = async () => {
    try {
      const response = await agentsAPI.list();
      setAgents(response.data.results || response.data);
    } catch (error) {
      console.error("Erreur lors du chargement des agents:", error);
    }
  };

  const loadConversations = async () => {
    try {
      const response = await conversationsAPI.list();
      setConversations(response.data.results || response.data);
    } catch (error) {
      console.error("Erreur lors du chargement des conversations:", error);
    }
  };

  const handleSelectConversation = async (conversationId) => {
    try {
      const response = await conversationsAPI.get(conversationId);
      setCurrentConversation(response.data);
      setMessages(response.data.messages || []);
      if (response.data.agents_details?.length > 0) {
        setSelectedAgent(response.data.agents_details[0]);
      }
    } catch (error) {
      console.error("Erreur lors du chargement de la conversation:", error);
    }
  };

  const handleDeleteConversation = async (conversationId) => {
    if (!confirm("Êtes-vous sûr de vouloir supprimer cette conversation ?"))
      return;

    try {
      await conversationsAPI.delete(conversationId);
      setConversations(conversations.filter((c) => c.id !== conversationId));
      if (currentConversation?.id === conversationId) {
        setCurrentConversation(null);
        setMessages([]);
      }
    } catch (error) {
      console.error("Erreur lors de la suppression de la conversation:", error);
    }
  };

  const handleSendMessage = async (message) => {
    if (!selectedAgent) {
      alert("Veuillez sélectionner un agent");
      return;
    }

    setIsLoading(true);
    try {
      const response = await conversationsAPI.sendMessage({
        message,
        agent_id: selectedAgent.id,
        conversation_id: currentConversation?.id,
      });

      // Ajouter les messages à l'affichage
      addMessage(response.data.user_message);
      addMessage(response.data.ai_message);

      // Mettre à jour la conversation courante
      if (!currentConversation) {
        const convResponse = await conversationsAPI.get(
          response.data.conversation_id,
        );
        setCurrentConversation(convResponse.data);
        loadConversations();
      }
    } catch (error) {
      console.error("Erreur lors de l'envoi du message:", error);
      alert("Erreur lors de l'envoi du message");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-chat-bg text-white">
      {isSidebarOpen && (
        <Sidebar
          conversations={conversations}
          onSelectConversation={handleSelectConversation}
          onDeleteConversation={handleDeleteConversation}
          currentConversationId={currentConversation?.id}
        />
      )}

      <div className="flex-1 flex flex-col">
        <Header
          selectedAgent={selectedAgent}
          agents={agents}
          onSelectAgent={setSelectedAgent}
          onToggleSidebar={toggleSidebar}
        />

        <ChatWindow messages={messages} />

        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={isLoading || !selectedAgent}
        />
      </div>
    </div>
  );
}
