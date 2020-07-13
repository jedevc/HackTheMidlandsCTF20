from twisted.internet import reactor, defer
from twisted.names import client, dns, server, error

the_map = """
#     # ####### #     #   ### #     # ####### #     # #     # ####### ######  
#     #    #    ##   ##  #    ##    # #     # #  #  # #     # #       #     # 
#     #    #    # # # #  #    # #   # #     # #  #  # #     # #       #     # 
#######    #    #  #  # ##    #  #  # #     # #  #  # ####### #####   ######  
#     #    #    #     #  #    #   # # #     # #  #  # #     # #       #   #   
#     #    #    #     #  #    #    ## #     # #  #  # #     # #       #    #  
#     #    #    #     #   ### #     # #######  ## ##  #     # ####### #     # 
                                                                              
#######          #####  #     # ####### #     # ###   
#               #     # #     # #     # #  #  #    #  
#               #       #     # #     # #  #  #    #  
#####            #####  ####### #     # #  #  #    ## 
#                     # #     # #     # #  #  #    #  
#               #     # #     # #     # #  #  #    #  
#######          #####  #     # #######  ## ##  ###   
        #######                                       
""".strip().split('\n')
TARGET = "gold"
OTHERS = ["silv", "brnz", "iron"]

class DynamicResolver:
    _pattern = b'.mine'

    def _dynamic_required(self, query):
        if query.type == dns.A:
            return query.name.name.endswith(self._pattern)
        return False

    def _do_dynamic_response(self, query):
        labels = query.name.name.split(b'.')
        try:
            x = int(labels[0])
            y = int(labels[1])
        except ValueError:
            return [], [], []

        if not 0 <= y < len(the_map):
            return [], [], []
        if not 0 <= x < len(the_map[y]):
            return [], [], []

        item = the_map[y][x]
        if item.isspace():
            address = OTHERS[(y * 9973 + x * 433) % len(OTHERS)]
        else:
            address = TARGET
        address = '.'.join(str(ord(ch)) for ch in address)

        answer = dns.RRHeader(
            name=query.name.name,
            payload=dns.Record_A(address=address)
        )
        return [answer], [], []

    def query(self, query, timeout=None):
        if self._dynamic_required(query):
            return defer.succeed(self._do_dynamic_response(query))
        else:
            return defer.fail(error.DomainError())

def main():
    factory = server.DNSServerFactory(
        clients=[DynamicResolver()]
    )
    protocol = dns.DNSDatagramProtocol(controller=factory)
    reactor.listenUDP(10053, protocol)
    reactor.listenTCP(10053, factory)
    reactor.run()

if __name__ == "__main__":
    raise SystemExit(main())
