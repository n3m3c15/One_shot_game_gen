# One Shot Game Generator 🎮

An **AI-powered game generation engine** that creates **fully playable browser games in a single generation step**.

The system takes a **natural language prompt describing a game** and generates a complete game with **HTML, CSS, and JavaScript**, packaged into a runnable web project.

The generated game is automatically served through a **Streamlit interface**, allowing users to instantly play the game inside the browser.

---

# Features

- 🎮 **One-shot game generation** using LLMs
- 🧠 **Prompt-engineered game design pipeline**
- 🕹️ Generates **fully playable browser games**
- 📦 Each game stored in a unique folder:
- 🖥️ **Streamlit interface** for interactive generation and testing
- 🐳 **Docker support** for easy deployment
- 🧩 Designed to work as a **tool inside a larger multi-agent system**

---

# How It Works

1. User enters a **game idea prompt**
2. **Game_description_agent** aka EnquiryAgent asks some clarifying questions and generates a text file
```
   generated_game_{timestamp}/game_details.txt
```
4. **Planning_agent** then uses the game details file to make a detailed development plan including architecture diags, tech stack selection etc based on game complexity 
5. The **Game Generation Agent** processes the request
6. The agent generates a complete game project
7. The game is saved in:

```
  generated_game_{timestamp}/index.html
```
8. Streamlit loads the latest generated game and displays it in an iframe.

---

# Project Structure

```
One_shot_game_gen/
│
├── main.py                     # Streamlit interface
│
├── Agents/
│   ├── Baseagent.py
│   ├── game_description_agent.py
│   ├── game_gen_agent.py
│   ├── planning_agent.py
│   │
│   ├── prompts/                # Prompt templates
│   └── skills/                 # Skills.MD files from Claude_Sonnet 4.6 to improve GPT-4.1 task accuracy
│
├── generated_game_{timestamp}/ # Generated game folders
│   ├── game_details.txt
│   ├── plan.md
│   ├── index.html
│   ├── assets/                 # optional based on game complexity
|   ├── scenes/                 # optional based on game complexity
|   └── systems/                # optional based on game complexity
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# Installation (Local)

1. Clone the repository:

```bash
  git clone https://github.com/n3m3c15/One_shot_game_gen.git
  cd One_shot_game_gen
```
2. Create virtual environment
3. Activate environment
4. Install dependencies
```bash
  pip install -r requirements.txt
```
5. Make .env file and add AZURE_OPENAI_API_KEY & AZURE_OPENAI_ENDPOINT
---

# Running the Application
1. Build the Docker image:

```bash
  docker build -t game-gen .
```

2. Run the container:

```bash
  docker run -p 8501:8501 game-gen
```

3. Open in browser:

```
  http://localhost:8501
```

---

# Example Prompt

```
  Create a 2D space shooter where the player controls a spaceship and destroys incoming asteroids.
```
Answer Follow-up Questions Patiently & verify game details
```
  generated_game_{timestamp}/game_details.txt
```
Verify, & Ask agent to proceed (say please)
```
  generated_game_{timestamp}/plan.md
```
Verify & respectfully ask the agent to proceed  
Generated output:

```
  generated_game_{timestamp}/index.html
```
The game will be rendered in streamlit iframe for testing and download  
Thank The AI For its efforts :P  
End chat  
```
   /quit or /q
```

---

---

# Important Constraints

- The **entry point of every generated game must always be named**

```
  index.html
```

- All assets must be **self-contained within the generated folder**

- The game must be **playable in a browser without external dependencies**

---

# Future Improvements

- Multi-step game generation pipelines i.e step-by-step automation pipeline that prioritizes output correctness, validation, and expectation–reality alignment
- Asset generation (sprites, sounds)
- Game physics engines
- Multiplayer support
- Continuous game iteration
- Evaluation metrics for generated games
- Improved Game development accuracy and reduce number of bugs

---

# License

MIT License

---

# Author

Developed by **n3m3c15**
