from random import choice
import string

class FakeLDAP(dict):

	def __init__(self):
		self['users'] = {}

	def ldap_api(self, netid, passwd, db):
		if netid in self['users'] and self['users'][netid] == passwd:
			if not netid in db['users']:
				db.add_user(netid, 'user') 
			return True
		return False

class FakeDB(dict):

	def __init__(self, hashlen=16):
		self['urls'] = {}
		self['visits'] = {}
		self['users'] = {}
		self['hashlen'] = hashlen
	def retrieve(self, key):
		if not key in self['urls']: return ""
		return 'http://www.'+str(self['urls'][key])
	def keyexists(self, key):
		return key in self['urls']

	def add_user(self, netid, privlevel):
		self['users'][netid] = {
				'netid' : netid,
				'privlevel' : privlevel,
				'keys' : []
		}
	def add_visit(self, key, ip_addr, timestamp):
		self['visits'][key] = {'ip' : ip_addr, 'timestamp' : timestamp}
	def keyexists(self, key):
		return key in self['urls']
	def isadmin(self, netid):
		return netid in self['users'] and self['users'][netid]['privlevel'] == 'admin'
	def getByPrefix(self, netid, prefix):
		return {key : val for key,val in self['urls'].iteritems() if str(val).startswith(prefix) and key in self['users'][netid]['keys']}
	def getAll(self):
		return self['urls']
	def getowner(self, key):
		if not key in self['urls']:
			return ""
		for netid in self['users'].keys():
			if key in self['users'][netid]['keys']:
				print "returning",netid
				return netid
		return ""
	def getByOwner(self, owner):
		if owner in self['users']:
			return {key:val for key,val in self['urls'].iteritems() if key in self['users'][owner]['keys']}
		return None
	def deleteurl(self, key):
		if not key in self['urls']:
			return False
		del self['urls'][key]
		return True

	def addurl(self, longurl, netid):
		while True:
			key = ''.join(choice(string.letters+string.digits) for n in range(self['hashlen']))
			if not key in self['urls']:
				self['urls'][key] = longurl.replace('http://','').replace('https://','').replace('www.','')
				self['users'][netid]['keys'].append(key)
				return key


