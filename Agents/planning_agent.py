from Agents.BaseAgent import BaseAgent
from typing import Any

class PlanningAgent(BaseAgent):
    def __init__(self):
        system_prompt = None
        skills = None
        with open('Agents/prompts/planning_agent_prompt.txt', 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        with open("Agents/skills/planning_skills.md", 'r', encoding='utf-8') as f:
            skills = f.read()
        super().__init__(system_prompt, skills=skills)
        
    def __call__(self, **kwds: Any) -> Any:
        game_requirements_path = kwds.get('game_details_save_path')
        self.game_requirements = None
        with open(game_requirements_path, 'r', encoding='utf-8') as f:
            self.game_requirements = f.read()
        return super().run(user_prompt= f'make a game generaation plan based on the following game requirements: {self.game_requirements}')