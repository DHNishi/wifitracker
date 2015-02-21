from flask import render_template, request
from app import app
import os
from functools import wraps

# Mock stuff.
import mock_database

# TODO: Remove this shit.
HACK_UPLOADED_FILE = False

def databaseUploadRequired(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		print HACK_UPLOADED_FILE
		if HACK_UPLOADED_FILE == False:
			return render_template('databaseNotUploaded.html', title="Uh-oh!")
		return f(*args, **kwargs)
	return decorated_function

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# TODO: Add in the ability to have parameters to further drill down the views.
@app.route('/packetView')
@databaseUploadRequired
def packetView():
    title = 'Packet-by-Packet View'
    template = 'packetView.html'
    packets = mock_database.getPackets(10)
    return render_template(template, title=title, packets=packets)

@app.route('/densityGraph')
@databaseUploadRequired
def densityGraph():
    title = 'Density Graph'
    template = 'densityGraph.html'
    packets = mock_database.getPackets(10)
    return render_template(template, title=title, packets=packets)

@app.route('/loadDatabase', methods=['GET', 'POST'])
def uploadDatabase():
	uploadCompleteTitle = 'Upload Complete!'
	uploadCompleteTemplate = 'uploadComplete.html'

	uploadTitle = 'Upload a SQLite Database'
	uploadTemplate = 'loadDatabase.html'

	# Handle the file upload request.
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = "packetDatabase.db"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			global HACK_UPLOADED_FILE
			HACK_UPLOADED_FILE = True
			print "wooho"
			return render_template(uploadCompleteTemplate, title=uploadCompleteTitle)
		return render_template(uploadTemplate, title=uploadTitle, error="There was a problem uploading the file.")

	# Default to showing the upload.
	return render_template(uploadTemplate, title=uploadTitle)

'''
####################
##HELPER FUNCTIONS##
####################
'''
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# TODO: Add a page which visualizes the density of a user's presence by day of the week and time.