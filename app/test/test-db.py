""" PyShrunk - Rutgers University URL Shortener

Unit tests for the database.
"""

from db import ShrunkClient


def get_shrunk_connection():
    return ShrunkClient("localhost")


def setup():
    pass


def test_urls():
    """Puts and retrieves URLs from the database."""
    shrunk = get_shrunk_connection()
    long_urls = ["foo.com", "bar.net", "báz7.edu.fr"]
    short_urls = []

    for url in long_urls:
        result = shrunk.create_short_url(url, netid="shrunk_test")
        short_urls.append(result)

    results = [shrunk.get_long_url(url) for url in short_urls]
    assert long_urls == results


def test_visit():
    """Tests logic when "visiting" a URL."""
    # TODO What do we even want to test
    

    # Keep this simple
    pass


def test_hitcount():
    """Tests the hit counters for URLs."""
    shrunk = get_shrunk_connection()
    hits = 4
    long_url = "test.edu"
    short_url = shrunk.create_short_url(long_url)

    for i in range(0, hits):
        shrunk.visit(short_url)

    assert shrunk.get_num_visits == hits


def test_deletion():
    """Tests a deletion from the database."""
    shrunk = get_shrunk_connection()
    long_url = "foo.com"
    short_url = shrunk.create_short_url(url, netid="shrunk_test")
    assert short_url is not None

    shrunk.delete_url(short_url)
    assert shrunk.get_long_url(short_url)

def teardown():
    shrunk = get_shrunk_connection()
    shrunk.delete_user_urls("shrunk_test")
