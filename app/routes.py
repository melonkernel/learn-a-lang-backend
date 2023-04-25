# routes.py
from app import app
from app.queue import createMediaQueueEntry
from flask import request

@app.route('/queue', methods=['GET'])
def addToQueue():
    return createMediaQueueEntry(request.args["url"])
