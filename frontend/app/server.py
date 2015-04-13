from flask import render_template, request
from app import app
import os
from functools import wraps
from collections import defaultdict

# Mock stuff.
import mock_database

# Database imports.
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect, MetaData
import database

# TODO: Remove this shit.
engine = None
session = None

# Wrappers.
def databaseUploadRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print app.config['DATABASE']
        if not os.path.isfile(app.config['DATABASE']):
            return render_template('databaseNotUploaded.html', title="Uh-oh!")
        initializeDatabaseIfNotInitialized()
        return f(*args, **kwargs)
    return decorated_function

def initializeDatabaseIfNotInitialized():
    global engine
    if engine is None:
        engine = database.buildEngine(app.config['DATABASE'])
        print "engine built!"
        m = MetaData()
        m.reflect(engine)
        for table in m.tables.values():
            print table.name
            for c in table.c:
                print c.name

        database.Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        global session
        session = Session()
        print "session set up"


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

    maybe_ssid = request.args.get("ssid")
    maybe_mac = request.args.get("mac")

    packets = _filterPackets(maybe_ssid, maybe_mac)
    #packets = session.query(database.Packet)
    return render_template(template, title=title, packets=packets, ssid=maybe_ssid, mac=maybe_mac)

@app.route('/packetViewRepeat')
@databaseUploadRequired
def repeatPacketView():
    title = 'Packet-by-Packet View'
    template = 'packetView.html'

    packets = session.query(database.Packet)
    repeat_users = get_return_users(packets)
    rackets = _filterPacketsByUsers(repeat_users)
    return render_template(template, title=title, packets=rackets)


def _filterPackets(ssid, mac):
    query = session.query(database.Packet)
    if ssid is not None:
        query = query.filter(database.Packet.ssid == ssid)
    if mac is not None:
        query = query.filter(database.Packet.mac == mac)
    return query

def _filterPacketsByUsers(macs):
    query = session.query(database.Packet)
    query = query.filter(database.Packet.mac.in_(macs))
    return query

@app.route('/repeatDensityGraph')
@databaseUploadRequired
def densityGraph():
    title = 'Density Graph'
    template = 'densityGraph.html'
    packets = session.query(database.Packet)
    repeat_users = get_return_users(packets)
    packets = _filterPacketsByUsers(repeat_users)
    hour_count = countByHour(packets)

    # Attempt to get the real database.
    initializeDatabaseIfNotInitialized();
    return render_template(template, title=title, packets=packets, hour_count=hour_count)


@app.route('/densityGraph')
@databaseUploadRequired
def userDensityGraph():
    title = 'Density Graph'
    template = 'userDensityGraph.html'

    maybe_mac = request.args.get("mac")
    maybe_ssid = request.args.get("ssid")
    packets = _filterPackets(maybe_ssid, maybe_mac)
    all_packets = session.query(database.Packet)
    hour_count = countByHour(packets)

    # Attempt to get the real database.
    initializeDatabaseIfNotInitialized();

    print get_return_users(all_packets);
    return render_template(template, title=title, packets=packets, hour_count=hour_count, ssid=maybe_ssid, mac=maybe_mac,
                           users=flatten_users(all_packets), macs=flatten_macs(all_packets))

"""
countByHour creates a count of unique MAC addresses encountered and breaks it down by hour.
"""
def countByHour(packets):
    hour_counter = defaultdict(set)
    for packet in packets:
        hour_counter[packet.time.hour].add(packet.mac)

    visitors = {h: len(v) for (h, v) in hour_counter.iteritems()}
    for i in xrange(0,24):
        if i not in visitors:
            visitors[i] = 0

    print visitors
    return visitors 

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

def flatten_users(packets):
    ssids = set()
    for packet in packets:
        ssids.add(packet.ssid)
    return ssids

def flatten_macs(packets):
    macs = set()
    for packet in packets:
        macs.add(packet.mac)
    return macs

def get_return_users(packets):
    user_day_map = defaultdict(set)
    for packet in packets:
        user_day_map[packet.mac].add(packet.time.date())

    macs = []
    print user_day_map
    for mac in user_day_map:
        if len(user_day_map[mac]) > 1:
            print "found one", mac
            macs.append(mac)

    return macs
# TODO: Add a page which visualizes the density of a user's presence by day of the week and time.