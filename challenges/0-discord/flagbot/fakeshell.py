import shlex
import time
import inspect

FLAG = "HTM{C0M3_1_c0m3_4ll}"

def interactive():
    command = input("> ")
    output = run(command)
    print(output)

def run(command):
    args = shlex.split(command)
    if len(args) == 0:
        return

    if args[0] not in BUILTINS:
        return f"fakeshell: command not found: {args[0]}"

    command = args[0]
    args = args[1:]

    builtin = BUILTINS[command]
    try:
        return builtin(*args)
    except TypeError:
        return f"{command}: invalid arguments"

BUILTINS = {}
def shell_command(name): 
    def shell_wrapper(function): 
        BUILTINS[name] = function
        return function
    return shell_wrapper

@shell_command("whoami")
def whoami():
    return "fake"

@shell_command("echo")
def echo(*args):
    return ' '.join(args)

@shell_command("groups")
def groups(*args):
    return 'fake'

@shell_command("pwd")
def pwd():
    return '/'

@shell_command("which")
def which(program):
    if program in FILES["bin"]:
        return f"/bin/{program}"
    else:
        return f"{program} not found"

@shell_command("ls")
def ls(filename='/', flags=''):
    show_hidden = False

    if flags.startswith('-'):
        if 'a' in flags:
            show_hidden = True

    root = FILES
    components = filename.split("/")
    try:
        for component in components:
            if component:
                root = root[component]
    except KeyError:
        return f"ls: cannot access '{filename}': no such file of directory"

    if isinstance(root, dict):
        files = [key for key in root.keys() if show_hidden or not key.startswith('.')]
        return '\n'.join(files)
    else:
        return components[-1]

@shell_command("ps")
def ps():
    return "\n".join([
        "PID  TTY    CMD",
        "1    pts/1  fakeshell",
    ])

@shell_command("cat")
def cat(filename):
    root = FILES
    components = filename.split("/")
    try:
        for component in components:
            if component:
                root = root[component]
    except (KeyError, TypeError):
        return f"cat: cannot access '{filename}': no such file of directory"

    if isinstance(root, dict):
        return f"cat: {filename}: is a directory"
    elif root is None:
        return f"cat: {filename}: cannot print contents"
    else:
        return root

FILES = {
    "bin": {
        "cat": inspect.getsource(cat),
        "echo": inspect.getsource(echo),
        "groups": inspect.getsource(groups),
        "ls": inspect.getsource(ls),
        "ps": inspect.getsource(ps),
        "pwd": inspect.getsource(pwd),
        "which": inspect.getsource(which),
        "whoami": inspect.getsource(whoami),
    },
    "data": {
        "flag": "Oh no, the flag's not here! Someone must have been and hidden in it somewhere else!",
        ".hidden": FLAG,
    },
}
