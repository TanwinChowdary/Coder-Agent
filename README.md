#  Coder Agent (web application builder)

##  Introduction
This project is a simple but powerful example of an **agentic AI system**, built using modern GenAI tools. Instead of being a normal “chat with an AI” setup, this tool behaves more like a small team of assistants working together. Each assistant has a specific role—one plans, one designs, and one writes the code—and they hand off work to each other in a clear, structured workflow. This makes it different from a single-shot prompt you send to a language model. Here, the model follows a multi-step reasoning process that you can actually see unfold.

You can describe a project in plain English, like “build a simple calculator,” and the agents will break that idea into a plan, list out tasks, and then generate all the files needed. Everything happens inside a protected project folder, so the AI only edits what it is allowed to. The progress bars help you follow what each agent is doing, which makes the process easier to understand.

This system is a great example of how AI can automate real developer tasks, not by guessing everything at once, but by following a thoughtful, step-by-step workflow—just like a small, well-organized engineering team.

##  What This Tool Does
- Turns a plain-English idea into a working code project  
- Uses a 3-agent pipeline: Planner → Architect → Coder  
- Writes files safely inside a project sandbox  
- Gives live progress updates so you always know what's happening  

##  How It Works
### 1. Planner Agent
Understands your request and creates a high-level project plan.

### 2. Architect Agent
Breaks the plan into detailed implementation steps.

### 3. Coder Agent
Creates or edits files using safe agent tools.

##  Tech Stack
- Python  
- LangGraph  
- LangChain  
- Groq LLM  
- Pydantic  
- Custom repo_browser toolset  

##  Project Structure
```
.
├── main.py
├── agent/
│   ├── graph.py
│   ├── prompts.py
│   ├── states.py
│   ├── tools.py
└── generated_project/
```

##  Getting Started
```
python main.py
```
Then type your project idea, e.g.:

```
build a simple calculator
```

##  Safety
All file edits go through restricted tools:
- read_file  
- write_file  
- list_files  
- get_current_directory  
- run_cmd  
- print_tree  

##  Future Improvements
- Templates for different stacks  
- Git integration  
- Code preview or diff stage  
- UI dashboard  

##  License
MIT
