from typing import Any
from Agents.BaseAgent import BaseAgent

class GameGenAgent(BaseAgent):
    def __init__(self):
        system_prompt = None
        skills = None
        with open("Agents/prompts/game_gen_prompt.txt", 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        with open("Agents/skills/game_script_gen_skill.md", 'r', encoding='utf-8') as f:
            skills = f.read()
        super().__init__(system_prompt, skills=skills)
    
    def __call__(self, **kwds: Any) -> Any:
        game_requirements_path = kwds.get('game_details_save_path')
        game_plan_save_path = kwds.get('game_plan_save_path')
        self.game_requirements = None
        self.game_generation_plan = None
        with open(game_requirements_path, 'r', encoding='utf-8') as f:
            self.game_requirements = f.read()
        with open(game_plan_save_path, 'r', encoding='utf-8') as f:
            self.game_generation_plan = f.read()
        return super().run(user_prompt= f'Generate a game based on the game requirements: {self.game_requirements} adhere to the following generation plan: {self.game_generation_plan}')