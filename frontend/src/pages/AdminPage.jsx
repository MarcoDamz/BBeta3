import { ArrowLeft, Copy, Plus, Trash2, Zap } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { agentsAPI, conversationsAPI } from "../services/api";

export default function AdminPage() {
  const navigate = useNavigate();
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    llm_model: "azure.gpt-4.1",
    system_prompt: "",
    temperature: 0.7,
    max_tokens: 2000,
    categories: [],
    is_active: true,
  });
  const [showAutoChat, setShowAutoChat] = useState(false);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const response = await agentsAPI.list();
      setAgents(response.data.results || response.data);
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const handleSelectAgent = (agent) => {
    setSelectedAgent(agent);
    setFormData({
      name: agent.name,
      description: agent.description || "",
      llm_model: agent.llm_model,
      system_prompt: agent.system_prompt,
      temperature: agent.temperature,
      max_tokens: agent.max_tokens,
      categories: agent.categories || [],
      is_active: agent.is_active,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedAgent) {
        await agentsAPI.update(selectedAgent.id, formData);
      } else {
        await agentsAPI.create(formData);
      }
      loadAgents();
      resetForm();
      alert("Agent sauvegardé avec succès");
    } catch (error) {
      console.error("Erreur:", error);
      alert("Erreur lors de la sauvegarde");
    }
  };

  const handleDuplicate = async (agentId) => {
    try {
      await agentsAPI.duplicate(agentId);
      loadAgents();
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const handleDelete = async (agentId) => {
    if (!confirm("Supprimer cet agent ?")) return;
    try {
      await agentsAPI.delete(agentId);
      loadAgents();
      if (selectedAgent?.id === agentId) {
        resetForm();
      }
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const resetForm = () => {
    setSelectedAgent(null);
    setFormData({
      name: "",
      description: "",
      llm_model: "azure.gpt-4.1",
      system_prompt: "",
      temperature: 0.7,
      max_tokens: 2000,
      categories: [],
      is_active: true,
    });
  };

  return (
    <div className="flex h-screen bg-chat-bg text-white">
      {/* Sidebar Agents */}
      <div className="w-80 bg-sidebar-bg border-r border-gray-700 flex flex-col">
        <div className="p-4 border-b border-gray-700">
          <button
            onClick={() => navigate("/")}
            className="flex items-center gap-2 text-gray-400 hover:text-white mb-4"
          >
            <ArrowLeft size={20} />
            <span>Retour au Chat</span>
          </button>
          <button
            onClick={resetForm}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg p-3 flex items-center justify-center gap-2"
          >
            <Plus size={20} />
            <span>Nouvel Agent</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto">
          {agents.map((agent) => (
            <div
              key={agent.id}
              onClick={() => handleSelectAgent(agent)}
              className={`p-4 cursor-pointer hover:bg-white/10 border-b border-gray-700 ${
                selectedAgent?.id === agent.id ? "bg-white/20" : ""
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold">{agent.name}</span>
                <div className="flex gap-1">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDuplicate(agent.id);
                    }}
                    className="p-1 hover:text-blue-400"
                  >
                    <Copy size={16} />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(agent.id);
                    }}
                    className="p-1 hover:text-red-400"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
              <div className="text-sm text-gray-400">{agent.llm_model}</div>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-gray-700">
          <button
            onClick={() => setShowAutoChat(true)}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white rounded-lg p-3 flex items-center justify-center gap-2"
          >
            <Zap size={20} />
            <span>Mode Auto-Chat</span>
          </button>
        </div>
      </div>

      {/* Formulaire */}
      <div className="flex-1 overflow-y-auto p-8">
        <h1 className="text-3xl font-bold mb-8">
          {selectedAgent ? "Modifier l'Agent" : "Créer un Agent"}
        </h1>

        <form onSubmit={handleSubmit} className="max-w-2xl space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Nom</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              rows="3"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Modèle LLM</label>
            <select
              value={formData.llm_model}
              onChange={(e) =>
                setFormData({ ...formData, llm_model: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
            >
              <option value="azure.gpt-4.1">azure.gpt-4.1</option>
              <option value="azure.gpt-4.1-mini">azure.gpt-4.1 Turbo</option>
              <option value="azure.gpt-4o">azure.gpt-4o</option>
              <option value="azure.gpt-4o-mini">azure.gpt-4o Mini</option>
              <option value="azure.gpt-5.1-turbo">azure.gpt-5.1 Turbo</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              System Prompt
            </label>
            <textarea
              value={formData.system_prompt}
              onChange={(e) =>
                setFormData({ ...formData, system_prompt: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              rows="8"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Température ({formData.temperature})
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={formData.temperature}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    temperature: parseFloat(e.target.value),
                  })
                }
                className="w-full"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">
                Max Tokens
              </label>
              <input
                type="number"
                value={formData.max_tokens}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    max_tokens: parseInt(e.target.value),
                  })
                }
                className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="is_active"
              checked={formData.is_active}
              onChange={(e) =>
                setFormData({ ...formData, is_active: e.target.checked })
              }
              className="w-4 h-4"
            />
            <label htmlFor="is_active" className="text-sm">
              Agent actif
            </label>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-6 py-3"
            >
              {selectedAgent ? "Mettre à jour" : "Créer"}
            </button>
            {selectedAgent && (
              <button
                type="button"
                onClick={resetForm}
                className="bg-gray-600 hover:bg-gray-700 text-white rounded-lg px-6 py-3"
              >
                Annuler
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Modal Auto-Chat */}
      {showAutoChat && (
        <AutoChatModal agents={agents} onClose={() => setShowAutoChat(false)} />
      )}
    </div>
  );
}

function AutoChatModal({ agents, onClose }) {
  const [formData, setFormData] = useState({
    agent_a_id: "",
    agent_b_id: "",
    initial_message: "",
    iterations: 5,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await conversationsAPI.autoChat(formData);
      alert("Auto-chat lancé avec succès ! Vérifiez vos conversations.");
      onClose();
    } catch (error) {
      console.error("Erreur:", error);
      alert("Erreur lors du lancement de l'auto-chat");
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
      <div className="bg-sidebar-bg rounded-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6">Mode Auto-Chat</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Agent A</label>
            <select
              value={formData.agent_a_id}
              onChange={(e) =>
                setFormData({ ...formData, agent_a_id: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600"
              required
            >
              <option value="">Sélectionner</option>
              {agents.map((agent) => (
                <option key={agent.id} value={agent.id}>
                  {agent.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Agent B</label>
            <select
              value={formData.agent_b_id}
              onChange={(e) =>
                setFormData({ ...formData, agent_b_id: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600"
              required
            >
              <option value="">Sélectionner</option>
              {agents.map((agent) => (
                <option key={agent.id} value={agent.id}>
                  {agent.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Message Initial
            </label>
            <textarea
              value={formData.initial_message}
              onChange={(e) =>
                setFormData({ ...formData, initial_message: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600"
              rows="4"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Nombre d'itérations
            </label>
            <input
              type="number"
              min="1"
              max="50"
              value={formData.iterations}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  iterations: parseInt(e.target.value),
                })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600"
              required
            />
          </div>

          <div className="flex gap-3 mt-6">
            <button
              type="submit"
              className="flex-1 bg-purple-600 hover:bg-purple-700 text-white rounded-lg py-3"
            >
              Lancer
            </button>
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-600 hover:bg-gray-700 text-white rounded-lg py-3"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
