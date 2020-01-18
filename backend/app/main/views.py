from flask import jsonify, request, render_template
from . import main

@main.route('/', defaults={'path':''})
@main.route('/<path:path>')
def root_view(path):
    return render_template('index.html')

