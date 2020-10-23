import sys
import dns.query
import dns.resolver
import dns.message

def decoder(ip):
    return ''.join(chr(int(part)) for part in ip.split('.'))

result = dns.resolver.resolve("ctfchals.hackthemidlands.com")
htm = result[0].to_text()

x = 0
y = 0
while True:
    msg = dns.message.make_query(f'{x}.{y}.mine', 'A')
    result = dns.query.udp(msg, htm, port=4003)

    try:
        ip = result.answer[0][0].to_text()
    except IndexError:
        if x == 0:
            sys.exit(0)
        else:
            x = 0
            y += 1
            print()
            continue

    metal = decoder(ip)
    if metal == "gold":
        print("X", end='', flush=True)
    else:
        print(" ", end='', flush=True)
    
    x += 1
    