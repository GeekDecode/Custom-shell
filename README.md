**MyShell**

***A custom, productivity-focused command-line interface built with Python.***

This project was inspired by the challenge to build a "Unique Project" that demonstrates system-level programming, file I/O, and developer automation.

## Key Features
- ***Developer Dashboard:*** Run `status` to see Git info and Todo tasks simultaneously.
- ***Persistent Storage:*** Built-in Todo manager that saves tasks to local disk.
- ***AI Buddy:*** Integrated with `Groq (Llama 3)` for fun, context-aware coding commentary
- ***System Integration:*** Executes standard system commands (ls, git, etc.) alongside custom logic.
- ***Web Automation:*** Direct Google searching from the command line.

## Tech Stack
- ***Language:*** Python 3
- ***Libraries:*** groq, python-dotenv
- ***Concepts:*** REPL Architecture, Subprocess Management, File Handling, Lambda Functions.

## Installation
1. Clone the repo: `https://github.com/GeekDecode/Custom-shell.git`
                   `cd Custom-shell`
2. Install Dependencies:`pip install groq python-dotenv`
3. Configure AI Buddy:  Create a `.env` file in the root folder.
                        Add your Groq API Key:`GROQ_API_KEY=your_key_here`.l                        
4. Add the folder path to your System Environment Variables (Path).
5. Run by typing `myshell` in any terminal.

## Docker Cheat Sheet
1. Build the image: `docker build -t my-ai-shell .`
2. Run with Persistence: `docker run -it --env-file .env -v "${PWD}:/app" my-ai-shell` OR
                    just run `run`
                    


