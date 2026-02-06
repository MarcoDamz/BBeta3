"""
Service LangChain pour la gestion des LLM.
"""

from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from django.conf import settings
from agents.models import Agent
from chatagentb.llm_config import get_model_config, DEFAULT_TITLE_MODEL


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
    def generate_title(first_message: str) -> str:
        """
        Génère un titre court pour une conversation à partir du premier message.
        """
        model_config = get_model_config(DEFAULT_TITLE_MODEL)

        # Configuration de base
        llm_config = {
            "model": model_config["model_name"],
            "temperature": 0.3,
            "max_tokens": 50,
            "api_key": settings.OPENAI_API_KEY,
        }

        # Ajouter l'URL de base si elle est configurée
        if settings.OPENAI_API_BASE:
            llm_config["base_url"] = settings.OPENAI_API_BASE

        llm = ChatOpenAI(**llm_config)

        prompt = f"""Génère un titre court (maximum 6 mots) pour cette conversation.
Le titre doit être concis et descriptif.

Message: {first_message}

Titre:"""

        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)

        title = response.content.strip().strip('"').strip("'")
        return title[:100]  # Limite à 100 caractères
