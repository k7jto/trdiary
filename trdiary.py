import flask
from flask import Flask, render_template, make_response, request, url_for, jsonify, g
import json
import random

app = Flask(__name__)

entries = [
        {
            'id': 1,
            'session': 1392596278493910,
            'time': '201611161227',
            'from': 'Device123',
            "Message1": "Hello, my name is Billy",
        },
        {
            'id': 2,
            'session': 1392596278493910,
            'time': '201611161229',
            'from': 'Tom1',
            'Message': 'Hello Billy, my name is Tom Riddle',
        },
        {
            'id': 3,
            'session': 1392596278493910,
            'time': '201611161244',
            'from': 'Device124',
            'Message': 'Do you know Moaning Myrtle?',
        },
    ]


@app.route('/', methods=['GET'])
def hello():
    # Create a nonce for this page
    scriptNonce = random.getrandbits(64)
    
    parsed_entries = json.dumps(entries)
    
    templateData = {
        'title' : 'Tom Riddle Diary',
        'script_nonce' : scriptNonce,
        'entry_Collection' : parsed_entries
        }
    
    r = make_response(render_template('main.html', **templateData))
    #r = make_response(render_template('main.html', json_data=entries))
    #r.headers.set('Content-Security-Policy', "default-src 'self'; script-src 'nonce-" +     str(scriptNonce) + "' 'self'")
    return r

@app.route('/trdiary/api/v1.0/messages/', methods=['GET'])
def get_tasks():
    return jsonify({'entries': entries})

@app.route('/response/', methods=['POST'])
def response():
    
    name=request.form['yourname']
    email=request.form['youremail']
    
    r = make_response(render_template('response.html', name=name, email=email))
    
    return r

# Retrieves all messages
# curl -i http://192.168.10.54:80/trdiary/api/v1.0/messages/
@app.route('/trdiary/api/v1.0/messages/', methods=['GET'])
def get_messages():
    return jsonify({'entries': entries})

# Retrieves message by id
# curl -i http://192.168.10.54:80/trdiary/api/v1.0/messages/2
@app.route('/trdiary/api/v1.0/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = [message for message in entries if message['id'] == message_id]
    if len(message) == 0:
        abort(404)
    r = make_response(jsonify({'message': message[0]}))
    return r

# Retrieves latest message
# curl -i http://192.168.10.54:80/trdiary/api/v1.0/latest_message
@app.route('/trdiary/api/v1.0/latest_message', methods = ['GET'])
def get_latest_message():
    i = len(entries)
    message = [message for message in entries if message['id'] == i]
    r = make_response(jsonify({'message': message[0]}))
    return r

@app.after_request
def addHeaders(response):
     # Set headers
    response.headers.set('cache-control', 'no-cache, no-store')
    response.headers.set('X-XSS-Protection', '1; mode=block')
    response.headers.set('X-Content-Type-Options', 'nosniff')
    response.headers.set('X-Frame-Options', 'deny')
    response.headers['Server'] = 'no-server' # Can't remove it, so set it to nothing
    return response

if __name__ == "__main__":
    app.run(host='192.168.10.54', port=80, debug=True)