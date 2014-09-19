pyshrunk
========
A URL shortener using Redis.

Python code should be written for _Python 2.7_.

Virtual Environment
-------------------
Python dependencies are enumerated in `pip.req`. You can set up an appropriate
virtual environment with the following:

    $ virtualenv --no-site-packages --python="python2.7" virtualenv
    $ source virtualenv/bin/activate
    $ pip install -r pip.req

Features
--------
### Web Application
- Log in with a Rutgers NetID
- Create a short URL from a long URL
- Given a NetID, what URLs have they created?
- Analytics on visits

### URL Shortening Service
- Given a short URL, redirect to the long URL
- Track visits to the short URL
- Track popularity and number of clicks

Future Ideas
------------
### Bundles
Bundle together a collection of related links together. The entire bundle has
one easy name that points to it.

### Organizations
Multiple people can log in to the same organization and manage shared links. It
will work like GitHub: you log in to your normal account and have the option of
switching to any one of the organizational accounts to which you have access.

We should have an organizational search feature so others can discover other
organizations, as well as avoid creating duplicates.

### Administrator Features
We want an administrator panel that can give global analytics and a table of all
links that have been created. It would be nice to have a white list and black
list of links, as well as the ability to use filters to block linking to certain
sites. We also need spam detection.
