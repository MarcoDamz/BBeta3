"""
Service LangChain pour la gestion des LLM.
"""

from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from django.conf import settings
from agents.models import Agent
from chatagentb.llm_config import get_model_config


class LLMService:
    """Service pour interagir avec les modèles LLM via LangChain."""

    @staticmethod
    def get_llm(agent: Agent):
        """
        Retourne une instance LLM configurée pour l'agent.
        """
        model_config = get_model_config(agent.llm_model)
        provider = model_config["provider"]

        # Configuration commune
        common_config = {
            "temperature": agent.temperature,
            "max_tokens": agent.max_tokens,
        }

        # Configuration selon le provider
        # TODO: a rétablir lorsqu'on aura plusieurs provider
        if 42:  # provider == "openai":
            llm_config = {
                **common_config,
                "model": model_config["model_name"],
                "api_key": settings.OPENAI_API_KEY,
            }
            return ChatOpenAI(**llm_config)

        # elif provider == "azure":
        #     llm_config = {
        #         **common_config,
        #         "model": model_config["model_name"],
        #         "azure_deployment": model_config.get("deployment_name"),
        #         "api_key": settings.AZURE_OPENAI_API_KEY,
        #         "azure_endpoint": settings.AZURE_OPENAI_ENDPOINT,
        #         "api_version": settings.AZURE_OPENAI_API_VERSION,
        #     }
        #     if settings.OPENAI_API_BASE:
        #         llm_config["base_url"] = settings.OPENAI_API_BASE
        #     return AzureChatOpenAI(**llm_config)

        else:
            raise ValueError(f"Provider '{provider}' non supporté")

    @staticmethod
    def create_messages(conversation_history: List[Dict], system_prompt: str) -> List:
        """
        Convertit l'historique de conversation en messages LangChain.
        """
        messages = [SystemMessage(content=system_prompt)]

        for msg in conversation_history:
            if msg["role"] == "human":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "ai":
                messages.append(AIMessage(content=msg["content"]))

        return messages

    @staticmethod
    def generate_response(agent: Agent, conversation_history: List[Dict]) -> str:
        """
        Génère une réponse de l'agent en fonction de l'historique.
        """
        llm = LLMService.get_llm(agent)
        messages = LLMService.create_messages(conversation_history, agent.system_prompt)

        response = llm.invoke(messages)
        return response.content

    @staticmethod
    def generate_title(agent: Agent, first_messages: List[Dict]) -> str:
        """
        Génère un titre court pour une conversation à partir du premier message.
        """

        llm = LLMService.get_llm(agent)

        context_lines = []
        for msg in first_messages:
            # Les messages sont des dict avec 'role' et 'content'
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            # Formater le rôle pour l'affichage
            role_label = "Utilisateur" if role == "human" else "Assistant"

            # Limiter le contenu à 200 caractères
            content_preview = content[:200] + "..." if len(content) > 200 else content

            context_lines.append(f"{role_label}: {content_preview}")

        context = "\n".join(context_lines)

        prompt = f"""Génère un titre court (maximum 6 mots) pour cette conversation.
Le titre doit être concis et descriptif.

Message: {context}

Titre:"""

        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)

        title = response.content.strip().strip('"').strip("'")
        return title[:100]  # Limite à 100 caractères
