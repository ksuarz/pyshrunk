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
             defaults to 6737.
        """
        self.host = host if host is not None else "localhost"
        self.port = port if port is not None else 6737

    def create_short_url(self, long_url, netid=None):
        """Given a long URL, create a new short URL. """
        raise NotImplementedError

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
