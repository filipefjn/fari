from flask import jsonify, request, render_template
from . import main
from ..settings import settings
import os
import re

@main.route('/', defaults={'path':''})
@main.route('/<path:path>')
def root_view(path):
    return render_template('index.html')

@main.route('/api/media-dir', methods=(['GET']))
def get_media_dir_view():
    media_dir = settings["media_dir"]
    if not os.path.exists(media_dir):
        raise Exception("media_dir does not exist")
    return { "result": media_dir }

@main.route('/api/folder-content', methods=(['POST']))
def post_folder_content():
    request_body = request.get_json(force=True)
    if "path" in request_body:
        path = request_body["path"]
    else:
        path = "/"
    path = re.sub(r'^/', '', path)
    path = re.sub(r'../', '', path)
    path = os.path.join(settings["media_dir"], path)
    if not os.path.exists(path):
        raise Exception("requested path does not exist")
    if not os.path.isdir(path):
        raise Exception("requested path is not a directory")
    dir_content = os.listdir(path)
    subfolders = []
    files = []
    for item in dir_content:
        if os.path.isdir(os.path.join(path, item)):
            subfolders.append(item)
        else:
            if "file_regex" in settings and re.search(settings["file_regex"], item) is not None:
                files.append(item)
    subfolders.sort()
    files.sort()
    return {
        "subfolders": subfolders,
        "files": files
    }
