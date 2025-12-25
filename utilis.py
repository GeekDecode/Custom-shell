import os
import random

def check_if_dir_exists(path: str) -> bool:
    return os.path.isdir(path)

def get_startup_message():
    quotes=[
        "Heya Partner!!!!Missed You😽",
        "Aha!! Ms.Unmotivated feeling motivated for few hours😏",
        "Write the damn Code!!!🧑‍💻",
        "It's tough to be your property😪"
    ]
    quote=random.choice(quotes)

    line ="~" * 50
    return f"\n{line}\n WELCOME TO YOUR CUSTOM SHELL\n \"{quote}\"\n{line}\n"