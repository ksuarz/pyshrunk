""" PyShrunk - Rutgers University URL Shortener

Implements database-level interactions for the shrunk application.
"""
import datetime
import random

import pymongo


class ShrunkClient(object):
    """A class for database interactions."""

    def __init__(self, host=None, port=None):
        """
        Create a new client connection.

        This client uses MongoDB. No network traffic occurs until a data method
        is called.

        :Parameters:
          - `host` (optional): the hostname to connect to; defaults to
            "localhost"
          - `port` (optional): the port to connect to on the server; defaults to
            the database default if not present
        """
        self._mongo = pymongo.MongoClient(host, port)

    def create_short_url(self, long_url, netid=None):
        """Given a long URL, create a new short URL.
        
        Randomly creates a new short URL and updates the Shrunk database.

        :Parameters:
          - `long_url`: The original URL to shrink.
          - `netid` (optional): The creator of this URL.

        :Returns:
          The shortened URL, or None if an error occurs.
        """
        short_url  = ShrunkClient.generate_unique_key()
        db = self._mongo.shrunk_urls

#        # Update the Redis database
#        self.redis.hset("shrunk_urls", short_url, long_url)
#        if netid is not None:
#            self.redis.hset(netid, short_url, long_url)

        # Update MongoDB
        db.urls.insert({
            "_id" : short_url,
            "url" : long_url,
            "creator" : netid,
            "time_created" : datetime.datetime.now(),
            "visits" : 0
        })
        return short_url

    def delete_url(self, short_url):
        """Given a short URL, delete it from the database.

        This deletes all information associated with the short URL and wipes all
        appropriate databases.
        
        :Parameters:
          - `short_url`: The shortened URL to dete.

        :Returns:
          True if the deletion occurred successfully; false otherwise. If there
          was no such record in the database, false is returned.
        """
        pass


    def delete_user_urls(self, netid):
        """Deletes all URLs associated with a given NetID.

        :Parameters:
          - `netid`: The NetID of the URLs to delete.
        
        :Returns:
          An integer indicating the number of deleted URLs.
        """
        pass

    def get_url_info(self, short_url):
        """Given a short URL, return information about it.

        This returns a dictionary containing the following fields:
          - long_url : The original unshrunk URL
          - time_created: The time the URL was created, expressed as seconds
            since the Unix epoch
          - netid : If it exists, the creator of the shortened URL
          - visits : The number of visits to this URL

        :Parameters:
          - `short_url`: A shortened URL.
        """
        db = self._mongo.shrunk_urls
        return db.urls.find_one({"_id" : short_url})

    def get_long_url(self, short_url):
        """Given a short URL, returns the long URL."""
        result = self.get_url_info(short_url)
        if result is not None:
            return result["url"]
        else:
            return None

    def get_visits(self, short_url):
        """Returns all visit information to the given short URL."""
        # TODO Better pipeline. Project away _id and sort by timestamp??
        # An idea is to $group by timestamp and make that the new _id
        db = self._mongo.shrunk_visits
        pipeline = [{"$group" : {"_id" : "time"}},
                    {"$match" : {"url" : short_url}}]
        return ShrunkClient._aggregate(db.visits, pipeline)

    def get_num_visits(self, short_url):
        """Given a short URL, return the number of visits."""
        db = self._mongo.shrunk_urls
        pipeline = {"$group" : {"_id" : "short_url",
                                "count" : {"$add" : "1"}}}
        return ShrunkClient._aggregate(db.visits, pipeline)

    def get_urls(self, netid):
        """Gets all the URLs created by the given NetID."""
        db = self._mongo.shrunk_urls
        pipeline = {"$match" : {"netid" : netid}}
        return ShrunkClient._aggregate(db.shrunk_urls, pipeline)

    def visit(self, short_url, source_ip):
        """Visits the given URL and logs visit information.
        
        On visiting a URL, this is guaranteed to perform at least the following
        side effects:
          - Increment the hit counter
          - Log the visitor
        """
        db = self._mongo.shrunk_urls
        db.urls.update({"_id" : short_url},
                       {"$inc" : {"visits" : 1}})

        # TODO Do we need the source ip or can we detect it?
        db = self._mongo.shrunk_visits
        db.visits.insert({
            "url" : short_url,
            "source_ip" : source_ip,
            "time" : datetime.datetime.now()
        })

    @staticmethod
    def _aggregate(collection, query):
        """Performs an aggregation on the database.

        This performs an aggregation on the database. This ensures that errors
        and failed queries are handled in a uniform fashion.
        """
        results = collection.aggregate(query)
        if results is None:
            return None
        elif results[u"ok"] != 1:
            return results
        else:
            return results[u"result"]

    @staticmethod
    def _generate_unique_key():
        """Generates a unique key in the database."""
        # TODO
        length = random.choice(range(5, 10))
        return "".join(
                random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(length))
