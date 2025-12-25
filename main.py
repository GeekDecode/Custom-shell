import os, re, subprocess, shlex
from command import COMMANDS,  manage_todo
from utilis import check_if_dir_exists, get_startup_message

def yellow_color(str):
    return f"\033[33m{str}\033[0m"

def red_color(str):
    return f"\033[31m{str}\033[0m"

print(yellow_color(get_startup_message()))
print(manage_todo(["list"]))
print("-" * 50)

history= []

while True:
    try:
        absolute_dir=os.getcwd()
        current_dir=os.path.basename(absolute_dir)

        if not current_dir:
            current_dir = absolute_dir

        prompt= "--"+yellow_color(current_dir) + "✨ "
        user_input = input(f"{prompt} ")

        user_input_stripped = user_input.strip()
        if not user_input_stripped:
            continue
        history.append(user_input_stripped)

        try:
            user_inputs = shlex.split(user_input_stripped)
        except ValueError as e:
            print(red_color(f" Quotation error: {e}"))
            continue

        command= user_inputs[0]
        args=user_inputs[1:]
 
        if command in COMMANDS:
            try:
                if command in["history","status"]:
                    result = COMMANDS[command](history)
                else:
                    result = COMMANDS[command](args)

                if result:
                    print(result)
            except Exception as e:
                print(red_color(f"  Error executing commands: {e}"))
        else:
            os.system(user_input_stripped)
        
    except KeyboardInterrupt:
        print("You have opted out")
        break
