import { ArrowLeft, Copy, Plus, Trash2, Zap } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { agentsAPI, llmAPI } from "../services/api";

export default function AdminPage() {
  const navigate = useNavigate();
  const [agents, setAgents] = useState([]);
  const [llmModels, setLlmModels] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    agent_type: "client",
    first_prompt: "",
    llm_model: "gpt-4o-mini",
    system_prompt: "",
    temperature: 0.7,
    max_tokens: 2000,
    categories: [],
    is_active: true,
  });
  const [showAutoChat, setShowAutoChat] = useState(false);

  useEffect(() => {
    loadAgents();
    loadLlmModels();
  }, []);

  useEffect(() => {
    if (selectedAgent) {
      setFormData({
        name: selectedAgent.name,
        description: selectedAgent.description,
        agent_type: selectedAgent.agent_type,
        first_prompt: selectedAgent.first_prompt,
        llm_model: selectedAgent.llm_model,
        system_prompt: selectedAgent.system_prompt,
        temperature: selectedAgent.temperature,
        max_tokens: selectedAgent.max_tokens,
        categories: selectedAgent.categories,
        is_active: selectedAgent.is_active,
      });
    }
  }, [selectedAgent]);

  const loadAgents = async () => {
    try {
      const response = await agentsAPI.list();
      setAgents(response.data.results || response.data);
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const loadLlmModels = async () => {
    try {
      const response = await llmAPI.getModels();
      let modelsList = [];

      // Vérifier le format de la réponse
      if (Array.isArray(response.data.models)) {
        modelsList = response.data.models;
      } else if (response.data && typeof response.data === "object") {
        // Si c'est un dictionnaire (cas actuel du backend), on le transforme en tableau
        // Le backend retourne { "model-id": { ...config }, ... } ou { models: ... }
        // D'après analyses, le endpoint /available-models/ retourne directement le dict des modèles ou wrapped

        const dataToProcess = response.data.models || response.data;

        if (!Array.isArray(dataToProcess)) {
          modelsList = Object.entries(dataToProcess).map(([key, config]) => ({
            value: key,
            label: config.display_name || key,
            provider: config.provider,
          }));
        } else {
          modelsList = dataToProcess;
        }
      }

      setLlmModels(modelsList);

      // Mettre à jour le modèle par défaut si disponible
      if (modelsList.length > 0 && !formData.llm_model) {
        setFormData((prev) => ({
          ...prev,
          llm_model: modelsList[0].value,
        }));
      }
    } catch (error) {
      console.error("Erreur lors du chargement des modèles LLM:", error);
    }
  };

  const handleSelectAgent = (agent) => {
    setSelectedAgent(agent);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Préparer les données pour l'API
      const dataToSend = { ...formData };

      // Nettoyer first_prompt si agent_type est "client"
      if (dataToSend.agent_type === "client") {
        dataToSend.first_prompt = null;
      }

      // Retirer categories si vide
      if (!dataToSend.categories || dataToSend.categories.length === 0) {
        delete dataToSend.categories;
      }

      if (selectedAgent) {
        await agentsAPI.update(selectedAgent.id, dataToSend);
      } else {
        await agentsAPI.create(dataToSend);
      }
      loadAgents();
      resetForm();
      alert("Agent sauvegardé avec succès");
    } catch (error) {
      console.error("Erreur:", error);
      console.error("Détails:", error.response?.data);
      alert(
        "Erreur lors de la sauvegarde: " +
          (error.response?.data?.detail ||
            JSON.stringify(error.response?.data) ||
            error.message),
      );
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
      agent_type: "client",
      first_prompt: "",
      llm_model: llmModels.length > 0 ? llmModels[0].value : "gpt-4o-mini",
      system_prompt: "",
      temperature: 0.7,
      max_tokens: 2000,
      categories: [],
      is_active: true,
    });
  };

  const handleAddCategory = () => {
    const category = prompt("Nom de la catégorie :");
    if (category && category.trim()) {
      setFormData({
        ...formData,
        categories: [...formData.categories, category.trim()],
      });
    }
  };

  const handleRemoveCategory = (index) => {
    setFormData({
      ...formData,
      categories: formData.categories.filter((_, i) => i !== index),
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
                <div>
                  <span className="font-semibold">{agent.name}</span>

                  <span className="ml-2 text-xs px-2 py-1 rounded-full bg-blue-600">
                    {agent.agent_type === "client" ? "Client" : "Métier"}
                  </span>
                </div>
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
              {/* ✅ Affichage des catégories */}
              {agent.categories &&
                Array.isArray(agent.categories) &&
                agent.categories.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {agent.categories.map((cat, idx) => (
                      <span
                        key={idx}
                        className="text-xs px-2 py-0.5 rounded bg-gray-700"
                      >
                        {cat}
                      </span>
                    ))}
                  </div>
                )}
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
          {/* Nom */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Nom <span className="text-red-500">*</span>
            </label>
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

          {/* Description */}
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
              placeholder="Description de l'agent..."
            />
          </div>

          {/* Type d'Agent */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Type d'Agent <span className="text-red-500">*</span>
            </label>
            <select
              value={formData.agent_type}
              onChange={(e) =>
                setFormData({ ...formData, agent_type: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
            >
              <option value="client">Client</option>
              <option value="metier">Métier</option>
            </select>
            <p className="text-xs text-gray-400 mt-1">
              {formData.agent_type === "client"
                ? "Agent client : reçoit les messages de l'utilisateur"
                : "Agent métier : répond avec un prompt initial personnalisé"}
            </p>
          </div>

          {/* Catégories */}
          <div>
            <label className="block text-sm font-medium mb-2">Catégories</label>
            <div className="flex flex-wrap gap-2 mb-2">
              {formData.categories.map((cat, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-blue-600 rounded-full text-sm flex items-center gap-2"
                >
                  {cat}
                  <button
                    type="button"
                    onClick={() => handleRemoveCategory(idx)}
                    className="text-white hover:text-red-300"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
            <button
              type="button"
              onClick={handleAddCategory}
              className="text-sm text-blue-400 hover:text-blue-300"
            >
              + Ajouter une catégorie
            </button>
          </div>

          {/* First Prompt (seulement pour agent métier) */}
          {formData.agent_type === "metier" && (
            <div>
              <label className="block text-sm font-medium mb-2">
                Premier Prompt (Agent Métier){" "}
                <span className="text-red-500">*</span>
              </label>
              <textarea
                value={formData.first_prompt}
                onChange={(e) =>
                  setFormData({ ...formData, first_prompt: e.target.value })
                }
                className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
                rows="4"
                placeholder="Message initial que l'agent métier enverra au début de la conversation..."
                required={formData.agent_type === "metier"}
              />
              <p className="text-xs text-gray-400 mt-1">
                Ce message sera automatiquement envoyé au début de la
                conversation
              </p>
            </div>
          )}

          {/* System Prompt */}
          <div>
            <label className="block text-sm font-medium mb-2">
              System Prompt <span className="text-red-500">*</span>
            </label>
            <textarea
              value={formData.system_prompt}
              onChange={(e) =>
                setFormData({ ...formData, system_prompt: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              rows="8"
              placeholder="Instructions système pour le comportement de l'agent..."
              required
            />
          </div>

          {/* Modèle LLM */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Modèle LLM <span className="text-red-500">*</span>
            </label>
            <select
              value={formData.llm_model}
              onChange={(e) =>
                setFormData({ ...formData, llm_model: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
            >
              {llmModels.length > 0 ? (
                llmModels.map((model) => (
                  <option key={model.value} value={model.value}>
                    {model.label}
                  </option>
                ))
              ) : (
                <option value="">Chargement des LLM...</option>
              )}
            </select>
          </div>

          {/* Paramètres LLM */}
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
              <p className="text-xs text-gray-400 mt-1">
                Créativité des réponses (0 = précis, 1 = créatif)
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">
                Max Tokens
              </label>
              <input
                type="number"
                min="100"
                max="4000"
                value={formData.max_tokens}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    max_tokens: parseInt(e.target.value),
                  })
                }
                className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              />
              <p className="text-xs text-gray-400 mt-1">
                Longueur maximale des réponses
              </p>
            </div>
          </div>

          {/* Statut Actif */}
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

          {/* Boutons */}
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
    </div>
  );
}
