""" PyShrunk - Rutgers University URL Shortener

Implements database-level interactions for the shrunk application.
"""


class ShrunkClient(object):
    """A class for database interactions."""

    def __init__(self, host=None, port=None):
        """
        Create a new client connection.

        This client uses Redis as a database. You can define another client
        class with a different database by implementing the API.

        No network traffic occurs until a data method is called.

        :Parameters:
          - `host` (optional): hostname or IP address of the database to connect
             to.  If none is specified, defaults to localhost.
          - `port` (optional): port number to connect to. If none is specified,
             defaults to 6379.
        """
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else 6737
        self.redis = redis.StrictRedis(host=host, port=port)

    def create_short_url(self, long_url, netid=None):
        """Given a long URL, create a new short URL. """
        short_url  = ShrunkClient().generate_unique_key()

        # Set the short URL association
        self.redis.hset(short_url, "long_url", long_url)
        self.redis.hset(short_url, "time_created", int(time.time()))
        if netid is not None:
            self.redis.hset(short_url, "netid", netid)

        # Set the NetID association
        if netid is not None:
            self.redis.sadd(netid, short_url)

        # Set the visits database
        # TODO

        # Set the clicks database
        self.redis.set("foo", 0)

    def get_url_info(self, short_url):
        """Given a short URL, return information about it.

        This returns a dictionary containing the following fields:
          - long_url : The original unshrunk URL
          - time_created: The time the URL was created, expressed as seconds
            since the Unix epoch
          - netid : If it exists, the creator of the shortened URL

        :Parameters:
          - `short_url`: A shortened URL.
        """
        return self.redis.hgetall(short_url)

    def get_long_url(self, short_url):
        """Given a short URL, returns the long URL. """
        raise NotImplementedError

    def get_visits(self, short_url):
        """Returns all visit information to the given short URL."""
        raise NotImplementedError

    def get_num_visits(self, short_url):
        """Given a short URL, return the number of visits."""
        raise NotImplementedError

    def get_urls(self, netid):
        """Gets all the URLs created by the given NetID."""
        raise NotImplementedError
