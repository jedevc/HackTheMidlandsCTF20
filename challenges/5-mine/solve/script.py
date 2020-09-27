import subprocess

def main():
    y = 0
    x = 0
    while True:
        code = lookup(x, y)
        if not code:
            print()
            if x == 0:
                break
            else:
                x = 0
                y += 1
                continue

        result = '#' if mineral(code) == "gold" else ' '
        print(result, end='', flush=True)

        x += 1

def lookup(x, y):
    proc = subprocess.run(f"dig '{x}.{y}.mine' -p4003 @127.0.0.1 +short", shell=True, check=True, stdout=subprocess.PIPE)
    return proc.stdout.decode().strip()

def mineral(code):
    return ''.join(chr(int(ch)) for ch in code.split('.'))

if __name__ == "__main__":
    main()
