from flask import jsonify, request, render_template, send_file
from . import main
from ..settings import settings
import music_tag
from base64 import b64encode
from .models import *
from .functions import hard_remake_library
import os
import re

@main.route('/', defaults={'path':''})
@main.route('/<path:path>')
def root_view(path):
    return render_template('index.html')

@main.route('/api/media-dir', methods=['GET'])
def media_dir_view():
    media_dir = settings["media_dir"]
    if not os.path.exists(media_dir):
        raise Exception("media_dir does not exist")
    return { "result": media_dir }

@main.route('/api/folder-content', methods=(['POST']))
def folder_content():
    request_body = request.get_json(force=True)
    if "path" in request_body:
        path = request_body["path"]
    else:
        path = "/"
    path = re.sub(r'^/', '', path)
    path = re.sub(r'\.\./', '', path)
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

@main.route('/api/fetch-file', methods=['POST'])
def fetch_file_view():
    request_body = request.get_json(force=True)
    if "path" in request_body:
        path = request_body["path"]
    else:
        raise Exception("you must specify a path")
    path = re.sub(r'^/', '', path)
    path = re.sub(r'\.\./', '', path)
    path = os.path.join(settings["media_dir"], path)
    if not os.path.exists(path):
        raise Exception("requested path does not exist")
    if not os.path.isfile(path):
        raise Exception("requested path is not a file")
    return send_file(path, as_attachment=True, attachment_filename=path.split("/")[-1])

@main.route('/api/file-info', methods=['POST'])
def file_info_view():
    request_body = request.get_json(force=True)
    if "path" in request_body:
        path = request_body["path"]
    else:
        raise Exception("you must specify a path")
    path = re.sub(r'^/', '', path)
    path = re.sub(r'\.\./', '', path)
    path = os.path.join(settings["media_dir"], path)
    if not os.path.exists(path):
        raise Exception("requested path does not exist")
    if not os.path.isfile(path):
        raise Exception("requested path is not a file")
    file = music_tag.load_file(path)
    # gettings tags
    tags = {}
    for tag_name in settings["file_tags"]:
        tags[tag_name] = file[tag_name].value
    response = {
        "tags": tags,
    }
    # getting artwork (if any)
    artwork = file['artwork']
    if artwork.first is not None:
        artwork_b64 = "data:" + artwork.first.mime + ";base64," + b64encode(artwork.first.data).decode('ascii')
        response["artwork"] = artwork_b64
    return response

@main.route('/api/file-artwork', methods=['POST'])
def file_artwork_view():
    request_body = request.get_json(force=True)
    if "path" in request_body:
        path = request_body["path"]
    else:
        raise Exception("you must specify a path")
    path = re.sub(r'^/', '', path)
    path = re.sub(r'\.\./', '', path)
    path = os.path.join(settings["media_dir"], path)
    if not os.path.exists(path):
        raise Exception("requested path does not exist")
    if not os.path.isfile(path):
        raise Exception("requested path is not a file")
    file = music_tag.load_file(path)
    response = {}
    # getting artwork (if any)
    artwork = file['artwork']
    if artwork.first is not None:
        artwork_b64 = "data:" + artwork.first.mime + ";base64," + b64encode(artwork.first.data).decode('ascii')
        response["artwork"] = artwork_b64
    return response

@main.route('/api/all-songs', methods=['GET', 'POST'])
def all_songs_view():
    all_songs = SongModel.query.order_by(SongModel.tracktitle).all()
    return jsonify(SongSchema(many=True).dump(all_songs))

@main.route('/api/hard-remake-library', methods=['GET', 'POST'])
def hard_remake_library_view():
    return hard_remake_library()
