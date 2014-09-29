# external
import sys, os
from flask import redirect, render_template, request, Response
from app import app
from tempClasses import FakeDB
from json import load, dumps

db = FakeDB(8)
db.add_user('admin', 'admin')
db.add_user('rick', 'user')
db.add_user('james', 'user')

# USER FACING -----------------------------------------------------------------
# auth required
@app.route('/')
@app.route('/about')
def index():
	return render_template("index.html")

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/admin')
def admin():
	return render_template('admin.html')

# URL RETRIEVAL ---------------------------------------------------------------
@app.route('/<key>')
def lookup(key):
	
	longurl = db.retrieve(key)
	if len(longurl) == 0:
		return render_template("notFound.html");
	db.add_visit(key, request.remote_addr, '<timestamp>');
	return redirect(longurl)

@app.route('/g/<key>')
def group(key):
	return render_template("group.html")

@app.route('/logout')
# auth required
def logout():
	
	logout_user()
	return redirect(url_for('login'))

# API FUNCTIONS ---------------------------------------------------------------
# auth required
@app.route('/api/add/url', methods=['POST'])
def addUrl():

	if not request.json:
		return Response(status=415)
	if not all(j in request.json for j in ('netid', 'longurl')):
		return Response(status=415)

	params = request.json
	netid = params['netid']
	longurl = params['longurl']

	key = db.addurl(longurl, netid)
	data = {}
	if key == None:
		data['success'] = False
		data['error'] = 'Unable to add url to database'
	else:
		data['success'] = True
		data['key'] = key
		#data['shorturl'] = SERVER_NAME+'/'+key
		data['shorturl'] = 'http://localhost/'+key

	js = dumps(data)
	return Response(js, status=200, mimetype='application/json')

# auth required
@app.route('/api/delete/url', methods=['POST'])
def deleteUrl():
	
	if not request.json:
		return Response(status=415)
	if not all(j in request.json for j in ('netid', 'key')):
		return Response(status=415)

	params = request.json
	netid = params['netid']
	key = params['key']

	if not db.keyexists(key):
		return "Unable to delete non-existent url",  400
	if netid != db.getowner(key) and not db.isadmin(netid):
		return "You don't own that url", 400

	# we're going to need some real error handling eventually
	data = {}
	data['success'] = db.deleteurl(key)

	js = dumps(data)
	return Response(js, status=200, mimetype='application/json')

# auth required
@app.route('/api/retrieve/netid', methods=['GET'])
def retrieveByOwner():

	if not request.json:
		return Response(status=415)
	if not all(j in request.json for j in ('netid', 'owner')):
		return Response(status=415)

	params = request.json
	netid = params['netid']
	owner = params['owner']

	if netid != owner and not db.isadmin(netid):
		return "Unauthorized access", 400
	urls = db.getByOwner(owner)

	data = { 'success' : len(urls) > 0, 'urls' : urls }
	
	js = dumps(data)
	return Response(js, status=200, mimetype='application/json')

# auth required
@app.route('/api/retrieve/all', methods=['GET'])
def retrieveAll():
	
	# we're probably going to want to modify this later 
	# so that we can limit our search results

	if not request.json:
		return Response(status=415)
	if not 'netid' in request.json:
		return Response(status=415)

	params = request.json
	netid = params['netid']

	if not db.isadmin(netid):
		return "Unauthorized access", 400

	urls = db.getAll()

	data = { 'success' : len(urls) > 0, 'urls' : urls }
	
	js = dumps(data)
	return Response(js, status=200, mimetype='application/json')
	
# auth required
@app.route('/api/retrieve/prefix')
def retrieveByPrefix():

	if not request.json:
		return Response(status=415)
	if not all(j in request.json for j in ('netid', 'prefix')):
		return Response(status=415)

	params = request.json
	netid = params['netid']
	prefix = params['prefix']

	urls = db.getByPrefix(netid=netid, prefix=prefix)
	data = { 'results' : urls, 'count' : len(urls) }
	
	js = dumps(data)
	return Response(js, status=200, mimetype='application/json')

