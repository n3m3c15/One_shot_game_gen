from typing import Any
from Agents.BaseAgent import BaseAgent
from Agents.game_gen_agent import GameGenAgent
from Agents.planning_agent import PlanningAgent
from datetime import datetime
import pytz
import os
import re
from typing import Optional, Tuple
from pathlib import Path
import sys

class EnquiryAgent(BaseAgent):
    def __init__(self):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "save_game_requirements",
                    "description": "Saves Game requirements and clarifications and return save path",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            'game_details': {
                                "type": "string",
                                "description": "All of the game details and clarifications collected from the user"
                            }
                        },
                        "required": ["game_details"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_plan",
                    "description": "Generates and Saves Game generation paln into a plan.md document and returns save path",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            'game_details_save_path': {
                                "type": "string",
                                "description": "save path provided by saving the game details file using save_game_requirements tool"
                            }
                        },
                        "required": ["game_details_save_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_game",
                    "description": "Generates game.js and index.html based on user specified requirement",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            'game_details_save_path': {
                                "type": "string",
                                "description": "save path provided by saving the game details file using save_game_requirements tool"
                            },
                            'game_plan_save_path':{
                                "type": "string",
                                "description": "save path returned on generating and saving game generation plan using generate_plan tool"
                            }
                        },
                        "required": ["game_details_save_path","game_plan_save_path"]
                    }
                }
            }
        ]
        system_prompt = None
        skills = None
        with open('D:/codes/game gen/Agents/prompts/enquiry_agent_prompt.txt', 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        with open("D:/codes/game gen/Agents/skills/requirements_gathering_skill.md", 'r', encoding='utf-8') as f:
            skills = f.read()
        super().__init__(system_prompt, skills=skills, tools=self.tools)
        
        # Register real Python function
        self.register_tool("save_game_requirements", self.save_game_requirements)
        self.register_tool("generate_plan",self.generate_plan)
        self.register_tool("generate_game", self.generate_game)

    def save_generated_files(self, agent_output, base_dir="generated_game"):

        pattern = r'<FILE path="(.*?)">(.*?)</FILE>'
        matches = re.findall(pattern, agent_output, re.DOTALL)

        all_generated_files = []
        for file_path, content in matches:

            full_path = os.path.join(base_dir, file_path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content.strip())

            print(f"Saved: {full_path}")
            all_generated_files.append(str(full_path))
        return all_generated_files
    # ------------------------
    # Local tool implementation
    # ------------------------
    def save_game_requirements(self,game_details):
        print("saving game details")
        output_dir: str = f"generated_game_{datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y_%m_%d_%H_%M_%S')}"
        # Create directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        game_details_file_name = "game_details.txt"
        game_details_path = os.path.join(output_dir, game_details_file_name)
        # Write files
        with open(game_details_path, "w", encoding="utf-8") as f:
            f.write(game_details)
        return f'game details saved to: {game_details_path}'
    
    def generate_plan(self, game_details_save_path):
        print('generating planning.md')
        plan_generator = PlanningAgent()
        planner_op = plan_generator(game_details_save_path = game_details_save_path)
        plan_file_path = game_details_save_path.split("\\")[0]
        plan_file_path = os.path.join(plan_file_path, 'plan.md')
        print(f'game genration plan generated')
        with open(plan_file_path, 'w', encoding='utf-8') as f:
            f.write(planner_op.strip())
        return f'game generation plan file saved to {plan_file_path}'
    
    def generate_game(self, game_details_save_path,game_plan_save_path):
        print(f'game generator tool called with file paths {game_details_save_path, game_plan_save_path}')
        game_generator = GameGenAgent()
        generator_op = game_generator(game_details_save_path = game_details_save_path, game_plan_save_path = game_plan_save_path)
        # print(generator_op)
        # html_code,js_code = self.extract_code_blocks(generator_op)
        game_files_path = game_details_save_path.split("\\")[0]
        print(f'saving game files to {game_files_path}')
        # self.save_game_files(html_code,js_code,game_files_path)
        all_generated_files = self.save_generated_files(generator_op,game_files_path)
        entry_point_path = None
        for path in all_generated_files:
            if 'index' in path:
                entry_point_path = path
        if entry_point_path:
            with open('current_game.txt', 'w', encoding='utf-8')as f:
                f.write(entry_point_path)
        return f'game files generated and save to {game_files_path}', entry_point_path
    
    def __call__(self, **kwds: Any) -> Any:
        user_prompt = kwds.get('user_prompt')
        return super().run(user_prompt=user_prompt)