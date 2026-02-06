import { useEffect, useState } from "react";
import { conversationsAPI } from "../services/api";

function AutoChatModal({ agents, onClose }) {
  const [formData, setFormData] = useState({
    agent_a_id: "",
    agent_b_id: "",
    initial_message: "",
    iterations: 5,
  });

  // Effet pour initialiser le message avec le first_prompt de l'agent métier sélectionné
  useEffect(() => {
    if (formData.agent_a_id) {
      const selectedAgent = agents.find(
        (agent) => agent.id === parseInt(formData.agent_a_id),
      );
      if (selectedAgent && selectedAgent.first_prompt) {
        setFormData((prev) => ({
          ...prev,
          initial_message: selectedAgent.first_prompt,
        }));
      }
    }
  }, [formData.agent_a_id, agents]);

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
      <div className="bg-sidebar-bg rounded-lg p-8 max-w-md w-full text-white">
        <h2 className="text-2xl font-bold mb-6">Mode Auto-Chat</h2>
        <p className="text-sm text-gray-400 mb-6">
          Lancez une conversation automatique entre deux agents IA
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Agent métier
            </label>
            <select
              value={formData.agent_a_id}
              onChange={(e) =>
                setFormData({ ...formData, agent_a_id: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              required
            >
              <option value="">Sélectionner un agent métier</option>
              {agents
                .filter((agent) => agent.agent_type === "metier")
                .map((agent) => (
                  <option key={agent.id} value={agent.id}>
                    {agent.name} ({agent.llm_model})
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
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              rows="4"
              placeholder="Ex: Discutez de l'intelligence artificielle..."
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Agent Client
            </label>
            <select
              value={formData.agent_b_id}
              onChange={(e) =>
                setFormData({ ...formData, agent_b_id: e.target.value })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              required
            >
              <option value="">Sélectionner un agent client</option>
              {agents
                .filter((agent) => agent.agent_type === "client")
                .map((agent) => (
                  <option key={agent.id} value={agent.id}>
                    {agent.name} ({agent.llm_model})
                  </option>
                ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Nombre d'itérations
            </label>
            <input
              type="number"
              min="1"
              max="20"
              value={formData.iterations}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  iterations: parseInt(e.target.value),
                })
              }
              className="w-full bg-input-bg text-white rounded-lg px-4 py-2 border border-gray-600 focus:outline-none focus:border-gray-500"
              required
            />
          </div>

          <div className="flex gap-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-700 hover:bg-gray-600 text-white rounded-lg py-2 transition"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="flex-1 bg-purple-600 hover:bg-purple-700 text-white rounded-lg py-2 transition"
            >
              Lancer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AutoChatModal;
