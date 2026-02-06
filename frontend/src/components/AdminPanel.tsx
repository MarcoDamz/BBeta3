import React, { useState } from 'react';

const AdminPanel = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    system_prompt: '',
    llm_model: 'gpt-4o-mini',
    temperature: 0.7,
    max_tokens: 1000,
    agent_type: 'client' as 'metier' | 'client',
    first_prompt: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Logique d'envoi des données du formulaire
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Panneau d'administration</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Autres champs du formulaire existants */}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Type d'agent
          </label>
          <select
            value={formData.agent_type}
            onChange={(e) =>
              setFormData({
                ...formData,
                agent_type: e.target.value as 'metier' | 'client',
                first_prompt: e.target.value === 'client' ? '' : formData.first_prompt,
              })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="client">Client</option>
            <option value="metier">Métier</option>
          </select>
        </div>

        {formData.agent_type === 'metier' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Premier prompt *
            </label>
            <textarea
              value={formData.first_prompt}
              onChange={(e) => setFormData({ ...formData, first_prompt: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px]"
              placeholder="Message initial que l'agent enverra pour démarrer la conversation..."
              required={formData.agent_type === 'metier'}
            />
            <p className="mt-1 text-sm text-gray-500">
              Ce message sera automatiquement envoyé par l'agent métier au début de chaque conversation
            </p>
          </div>
        )}

        {/* Bouton de soumission et autres éléments */}
      </form>
    </div>
  );
};

export default AdminPanel;