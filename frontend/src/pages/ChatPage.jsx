import { useEffect, useState } from "react";
import ChatInput from "../components/ChatInput";
import ChatWindow from "../components/ChatWindow";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import { agentsAPI, conversationsAPI, foldersAPI } from "../services/api";
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
    updateMessage,
    isSidebarOpen,
    toggleSidebar,
    folders,
    setFolders,
    addFolder,
    updateFolder,
    deleteFolder,
    moveConversationToFolder,
  } = useStore();

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadAgents();
    loadConversations();
    loadFolders();
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

  const loadFolders = async () => {
    try {
      const response = await foldersAPI.list();
      setFolders(response.data.results || response.data);
    } catch (error) {
      console.error("Erreur lors du chargement des dossiers:", error);
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

  const handleNewConversation = () => {
    setCurrentConversation(null);
    setMessages([]);
    setSelectedAgent(agents.length > 0 ? agents[0] : null);
  };

  const handleCreateFolder = async (folderName) => {
    try {
      const response = await foldersAPI.create({ name: folderName });
      addFolder(response.data);
    } catch (error) {
      console.error("Erreur lors de la création du dossier:", error);
      alert("Erreur lors de la création du dossier");
    }
  };

  const handleDeleteFolder = async (folderId) => {
    try {
      await foldersAPI.delete(folderId);
      deleteFolder(folderId);
      // Recharger les conversations pour mettre à jour celles qui étaient dans le dossier
      loadConversations();
    } catch (error) {
      console.error("Erreur lors de la suppression du dossier:", error);
      alert("Erreur lors de la suppression du dossier");
    }
  };

  const handleRenameFolder = async (folderId, currentName) => {
    const newName = prompt("Nouveau nom du dossier:", currentName);
    if (newName && newName.trim() && newName !== currentName) {
      try {
        const response = await foldersAPI.update(folderId, {
          name: newName.trim(),
        });
        updateFolder(folderId, response.data);
      } catch (error) {
        console.error("Erreur lors du renommage du dossier:", error);
        alert("Erreur lors du renommage du dossier");
      }
    }
  };

  const handleMoveConversation = async (conversationId, folderId) => {
    try {
      await conversationsAPI.moveToFolder(conversationId, folderId);
      moveConversationToFolder(conversationId, folderId);
    } catch (error) {
      console.error("Erreur lors du déplacement de la conversation:", error);
      alert("Erreur lors du déplacement de la conversation");
    }
  };

  const handleSendMessage = async (message) => {
    if (!selectedAgent) {
      alert("Veuillez sélectionner un agent");
      return;
    }

    // Créer un message optimiste
    const optimisticId = `temp-${Date.now()}`;
    const optimisticMessage = {
      id: optimisticId,
      role: "human",
      content: message,
      created_at: new Date().toISOString(),
      agent_id: selectedAgent.id,
      conversation_id: currentConversation?.id,
    };

    // Ajouter immédiatement à l'interface
    addMessage(optimisticMessage);
    setIsLoading(true);

    try {
      const response = await conversationsAPI.sendMessage({
        message,
        agent_id: selectedAgent.id,
        conversation_id: currentConversation?.id,
      });

      // Mettre à jour le message utilisateur avec la réponse du serveur (vrai ID, timestamp, etc.)
      updateMessage(optimisticId, response.data.user_message);

      // Ajouter la réponse de l'agent
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
      // En cas d'erreur, on pourrait retirer le message optimiste ou le marquer en erreur
      // Pour l'instant on laisse tel quel ou on pourrait le retirer
      // setMessages(messages.filter(m => m.id !== optimisticId));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-chat-bg text-white">
      {isSidebarOpen && (
        <Sidebar
          conversations={conversations}
          folders={folders}
          onSelectConversation={handleSelectConversation}
          onDeleteConversation={handleDeleteConversation}
          onNewConversation={handleNewConversation}
          currentConversationId={currentConversation?.id}
          onCreateFolder={handleCreateFolder}
          onDeleteFolder={handleDeleteFolder}
          onRenameFolder={handleRenameFolder}
          onMoveConversation={handleMoveConversation}
        />
      )}

      <div className="flex-1 flex flex-col">
        <Header agents={agents} onToggleSidebar={toggleSidebar} />

        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          agents={agents}
          selectedAgent={selectedAgent}
          onSelectAgent={setSelectedAgent}
        />

        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={isLoading || !selectedAgent}
        />
      </div>
    </div>
  );
}
