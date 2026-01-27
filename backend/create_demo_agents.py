"""
Script pour créer des agents de démonstration.
À exécuter : docker-compose exec backend python create_demo_agents.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatagentb.settings')
django.setup()

from agents.models import Agent

def create_demo_agents():
    """Crée des agents de démonstration si aucun n'existe."""
    
    if Agent.objects.exists():
        print("Des agents existent déjà. Suppression pour réinitialisation...")
        Agent.objects.all().delete()
    
    agents = [
        {
            'name': 'Assistant Python',
            'description': 'Expert en programmation Python, frameworks web et bonnes pratiques',
            'categories': ['développement', 'python', 'backend'],
            'llm_model': 'azure.gpt-4.1',
            'system_prompt': '''Tu es un expert en programmation Python avec une connaissance approfondie de:
- Django, Flask, FastAPI
- Python avancé (asyncio, decorators, metaclasses)
- Bonnes pratiques (PEP 8, tests, documentation)
- Optimisation et performance

Réponds de manière concise et technique. Fournis des exemples de code quand c'est pertinent.''',
            'temperature': 0.3,
            'max_tokens': 2000,
        },
        {
            'name': 'Expert JavaScript',
            'description': 'Spécialiste React, Node.js et écosystème JavaScript moderne',
            'categories': ['développement', 'javascript', 'frontend'],
            'llm_model': 'azure.gpt-4.1',
            'system_prompt': '''Tu es un expert en JavaScript et TypeScript avec une expertise en:
- React, Vue.js, Angular
- Node.js et Express
- Build tools (Webpack, Vite, esbuild)
- Tests (Jest, Vitest, Cypress)

Recommande les meilleures pratiques modernes et les patterns actuels.''',
            'temperature': 0.4,
            'max_tokens': 2000,
        },
        {
            'name': 'Architecte Cloud',
            'description': 'Expert en architecture cloud (AWS, GCP, Azure) et DevOps',
            'categories': ['cloud', 'devops', 'architecture'],
            'llm_model': 'azure.gpt-4.1',
            'system_prompt': '''Tu es un architecte cloud senior spécialisé en:
- AWS, GCP, Azure
- Kubernetes, Docker
- CI/CD (GitHub Actions, GitLab CI)
- Infrastructure as Code (Terraform, CloudFormation)
- Sécurité et monitoring

Propose des solutions scalables, sécurisées et cost-effective.''',
            'temperature': 0.4,
            'max_tokens': 2500,
        },
        {
            'name': 'Analyste de Données',
            'description': 'Expert en data science, machine learning et visualisation',
            'categories': ['data', 'ml', 'analytics'],
            'llm_model': 'claude-3-sonnet',
            'system_prompt': '''Tu es un data scientist expérimenté spécialisé en:
- Python data stack (pandas, numpy, scikit-learn)
- Machine Learning et Deep Learning
- Visualisation (matplotlib, plotly, seaborn)
- SQL et bases de données
- Statistical analysis

Explique les concepts techniques de manière accessible tout en restant rigoureux.''',
            'temperature': 0.5,
            'max_tokens': 2500,
        },
        {
            'name': 'Assistant Créatif',
            'description': 'Aide à la rédaction, brainstorming et génération d\'idées',
            'categories': ['créatif', 'rédaction', 'brainstorming'],
            'llm_model': 'claude-3-sonnet',
            'system_prompt': '''Tu es un assistant créatif qui aide à:
- Générer des idées originales
- Rédiger des contenus engageants
- Brainstormer des solutions créatives
- Améliorer des textes existants

Tu es enthousiaste, créatif et constructif. Tu proposes toujours plusieurs alternatives.''',
            'temperature': 0.8,
            'max_tokens': 2000,
        },
        {
            'name': 'Professeur Pédagogue',
            'description': 'Explique des concepts complexes de manière simple et progressive',
            'categories': ['éducation', 'pédagogie', 'vulgarisation'],
            'llm_model': 'azure.gpt-4.1',
            'system_prompt': '''Tu es un professeur passionné qui excelle à:
- Expliquer des concepts complexes simplement
- Adapter ton niveau au public
- Utiliser des analogies et des exemples concrets
- Structurer l'apprentissage de manière progressive
- Encourager la réflexion et les questions

Tu es patient, encourageant et pédagogue.''',
            'temperature': 0.6,
            'max_tokens': 2000,
        },
    ]
    
    created_count = 0
    for agent_data in agents:
        agent = Agent.objects.create(**agent_data)
        created_count += 1
        print(f"✓ Agent créé: {agent.name} ({agent.llm_model})")
    
    print(f"\n✓ {created_count} agents de démonstration créés avec succès!")
    print("\nAccédez à l'interface admin pour les voir:")
    print("  http://localhost:8000/admin/agents/agent/")
    print("\nOu utilisez-les directement dans le chat:")
    print("  http://localhost:3000/")

if __name__ == '__main__':
    create_demo_agents()
