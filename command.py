import os
from typing import List
import platform
import webbrowser
from groq import Groq
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
GROQ_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_KEY)

def yellow_color(str):
    return f"\033[33m{str}\033[0m"


def echo(args: List[str]) ->str:
    """
    Echo the provided arguments back to the console.
    Usage: echo [text...]
    """
    return ' '.join(args) if args else' '


def list_directory(args:List[str]=None) -> str:
    """
    List directory contents.
    Usage: ls [directory]
    """
    path= args[0] if args else '.'
    try:
        return '\n'.join(os.listdir(path))
    except FileNotFoundError:
        return f"Directory not found: {path}"
    except NotADirectoryError:
        return f"Not a directory: {path}"


def make_directory(args: List[str]) ->str:
    """
    Create a new directory.
    Usage: mkdir[directory_name]
    """
    if not args:
        return"Error: Please specify a directory name"
    try:
        os.makedirs(args[0], exist_ok=True)
        return f"Created directory: {args[0]}"
    except OSError as e:
        return f"Error creating directory:{e}"


def change_directory(args: List[str])-> str:
    """
    Change the current working directory.
    Usage: cd [directory]
    """
    try: 
        if not args:
            path = os.path.expanduser("~")
        else:
            path = args[0]
            
        os.chdir(path)
        return ""
    except FileNotFoundError:
        return f"Directory Not found: {args[0]}"
    except NotADirectoryError:
        return f"Not a directory: {args[0]}"


def get_system_info() ->str:
    """
    Get system information.
    Usgae: sysinfo
    """
    info=[
        f"System: {platform.system()}",
        f"Node: {platform.node()}"
        f"Release: {platform.release()}",
        f"Version: {platform.version()}",
        f"Machine: {platform.machine()}",
        f"Processor: {platform.processor()}",
        f"Python: {platform.python_version()}",
    ]
    return '\n'.join(info)


def show_history(history_list: List[str])->str:
    """Show the last 10 commands."""
    last_commands = history_list[-10:]
    output = []
    for i, cmd in enumerate(last_commands):
        output.append(f"{i+1}: {cmd}")
    return "\n".join(output)


def google_search(args: List[str])->str:
    """Search Google directly from the shell."""
    if not args:
        return "What do you want to serach for?"
    
    query="+".join(args)
    url=f"https://www.google.com/search?q={query}"
    #special "ESCAPE CHARACTERS" taht create hyperlink since docker is running linux while operating on windows
    link_start = "\x1b]8;;" 
    link_end = "\x1b\\"
    reset = "\x1b]8;;\x1b\\"
    display_text = f" Click here to search for: {' '.join(args)}"
    return f"\n{link_start}{url}{link_end}{display_text}{reset}\n"


def clear_screen()->str:
    """Clear the terminal screen."""
    if os.name =='nt':
        os.system('cls')
    else:
        os.system('clear')
    return""


TODO_FILE="todo_list.txt"
def manage_todo(args: List[str])->str:
    """
    Add or list tasks.
    Usage: todo add 'task or todo list
    """
    if not args:
        return "Usage: todo add <task> | todo list | todo delete <num> | todo clear"
    
    action= args[0].lower()
    if action=="add":
        task=" ".join(args[1:])
        with open(TODO_FILE, "a") as f:
            f.write(task + "\n")
        return f"✅ Task added: {task}"
    
    elif action =="list":
        if not os.path.exists(TODO_FILE):
            return "No tasks found."
        with open(TODO_FILE, "r") as f:
            tasks = f.readlines()
        if not tasks:
            return "Your todo list is empty!"
        output = ["--- YOUR TASKS ---"]
        for i, t in enumerate(tasks):
            output.append(f"{i+1}. {t.strip()}")
        return "\n".join(output)
    
    elif action == "delete":
        if not args[1:]:
            return "Error: Specify the task number to delete (e.g., todo delete 1)"
        
        try:
            task_num = int(args[1]) - 1 # Convert to 0-based index
            with open(TODO_FILE, "r") as f:
                tasks = f.readlines()
            
            if 0 <= task_num < len(tasks):
                removed = tasks.pop(task_num)
                with open(TODO_FILE, "w") as f:
                    f.writelines(tasks)
                return f"❌ Deleted: {removed.strip()}"
            else:
                return f"Error: Task #{args[1]} does not exist."
        except ValueError:
            return "Error: Please provide a valid number."
    
    elif action == "clear":
        open(TODO_FILE, 'w').close()
        return "List cleared!"

    return "Unknown action. Use 'add', 'list', or 'clear'."


def get_git_status()->str:
    """
    Check if current directory is a got repo and return status.
    """
    try:
        branch= subprocess.check_output(
            ["git","branch","--show-current"],
            stderr=subprocess.DEVNULL

        ).decode().strip()

        status= subprocess.check_output(
            ["git", "status", "--short"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        if not status:
            status="Clean (Nothing to commit)"
        return f"Git Branch: {branch}\nChanges:\n{status}"
    except:
        return "Not a Git repository"
    

def dashboard(history_list: List[str]) ->str:
    """
    A master command that shows everything at once
    """
    from command import manage_todo
    
    line="-"*40
    git_info =get_git_status()
    todo_info= manage_todo(["list"])

    output=[
        yellow_color("\n DEVELOPER DASHBOARD"),
        line,
        "TODOS:",
        todo_info,
        line,
        "GET STATUS:",
        git_info,
        line,
        f"Last Command: {history_list[-2] if len(history_list) > 1 else 'None'}",
        line
    ]
    return "\n".join(output)


def ai_buddy(history_list: list[str])-> str:
    """Uses Groq to give lighting-fast fun insights."""
    if not GROQ_KEY:
        return "⚠️ AI Buddy needs a Groq API Key in your .env file!"

    if len(history_list) < 2:
        return "I'm watching! Run some more commands first. 👀"

    history_str = ", ".join(history_list[-10:])
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a supportive, fun coding buddy. Give 1-sentence responses with emojis."
                },
                {
                    "role": "user",
                    "content": f"My recent shell commands are: {history_str}. Cheer me on or give a fun fact!"
                }
            ],
            model="llama-3.3-70b-versatile", # This model is very smart and free
        )
        return f"\n⚡ AI BUDDY: {chat_completion.choices[0].message.content}"
    
    except Exception as e:
        return f"☁️ AI Buddy is offline. (Error: {str(e)[:50]}...)"


def exit_shell() ->str:
    """
    Exit the shell safely
    """
    print("Shutting down... Goodbye!!!!")
    sys.exit(0)


def help_command()->str:
    """
   Show help information for available commands.
   Usage: help
    """
    commands ={
        'echo': 'Echo the provided arguments back to console.',
        'ls': 'List directory contents',
        'mkdir':'Create a new directory',
        'cd': 'Change the current working directory',
        'sysinfo': 'Display system information',
        'google':'does searxh on google',
        'history': 'shows last 10 commands',
        'help': 'Show this help message',
        'exit/quit':'Exit the shell',
        'clear':'Clear the clean the shell from mess',
        'todo':'makes a todo list',
        'status':'Shows Git dashboard',
        'buddy':'gives fun commentary',
    }

    help_text= ["Available commands"]
    for cmd, desc in commands.items():
        help_text.append(f" {cmd:<10} - {desc}")
    return '\n'.join(help_text)

COMMANDS={
    'echo': echo,
    'ls': list_directory,
    'mkdir': make_directory,
    'cd': change_directory,
    'sysinfo': lambda _: get_system_info(),
    'history':lambda h_list: show_history(h_list),
    'google':google_search,
    'help':lambda _: help_command(),
    'clear':lambda _: clear_screen(),
    'todo':manage_todo,
    'exit':lambda _:exit_shell(),
    'quit':lambda _:exit_shell(),
    'status':lambda h_list:dashboard(h_list),
    'buddy':lambda h_list:ai_buddy(h_list),
    }