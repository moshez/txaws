from twisted.internet import reactor, ssl
from twisted.web.client import HTTPClientFactory

from txaws.util import parse


# XXX this will be filled in with the work from generalizing the s3 and ec2
# clients
class BaseClient(object):
    pass


class BaseQuery(object):

    def __init__(self, action=None, creds=None, endpoint=None):
        if not action:
            raise TypeError("The query requires an action parameter.")
        self.factory = HTTPClientFactory
        self.action = action
        self.creds = creds
        self.endpoint = endpoint
        self.client = None

    def get_page(self, url, *args, **kwds):
        """
        Define our own get_page method so that we can easily override the
        factory when we need to. This was copied from the following:
            * twisted.web.client.getPage
            * twisted.web.client._makeGetterFactory
        """
        contextFactory = None
        scheme, host, port, path = parse(url)
        self.client = self.factory(url, *args, **kwds)
        if scheme == 'https':
            contextFactory = ssl.ClientContextFactory()
            reactor.connectSSL(host, port, self.client, contextFactory)
        else:
            reactor.connectTCP(host, port, self.client)
        return self.client.deferred
