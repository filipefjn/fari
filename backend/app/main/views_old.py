from flask import jsonify, request, render_template, send_file
from . import main
from ..settings import settings
from .. import db
import music_tag
from base64 import b64encode
from .models import *
from .functions import remake_library, create_fari_file, remake_artists_and_albums, delete_artists_and_albums, get_song_artwork_base64
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

@main.route('/api/full-song-list', methods=['GET', 'POST'])
def full_song_list_view():
    song_list = SongModel.query.order_by(SongModel.tracktitle).all()
    return jsonify(SongSchema(many=True).dump(song_list))

@main.route('/api/full-song-list-by-artist-album', methods=['GET', 'POST'])
def full_song_list_by_artist_album_view():
    return jsonify(ArtistNestedSchema(many=True).dump(ArtistModel.query.all()))

@main.route('/api/artist-list', methods=['GET', 'POST'])
def artist_list_view():
    artist_list = ArtistSchema(many=True).dump(ArtistModel.query.order_by(ArtistModel.name.asc()).all())
    #artist_list.sort(key=lambda artist: artist["name"])
    return jsonify(artist_list)

@main.route('/api/artist-song-list', methods=['POST'])
def artist_song_list_view():
    request_body = request.get_json(force=True)
    if "id" in request_body:
        artist_id = request_body["id"]
    else:
        raise Exception("you must specify an id")
    return jsonify(ArtistNestedSchema().dump(ArtistModel.query.get_or_404(artist_id)))

@main.route('/api/album-artwork', methods=['POST'])
def album_artwork_view():
    request_body = request.get_json(force=True)
    if "id" in request_body:
        artist_id = request_body["id"]
    else:
        raise Exception("you must specify an id")
    album = AlbumSchema().dump(AlbumModel.query.get_or_404(artist_id))
    if len(album["songs"]) == 0:
        return ({}, 404)
    file_path = album["songs"][0]["path"]
    album_artwork = get_song_artwork_base64(file_path)
    if album_artwork is None:
        return ({}, 404)
    return jsonify({"artwork": album_artwork})

@main.route('/api/remake-library', methods=['GET', 'POST'])
def remake_library_view():
    return remake_library()

@main.route('/api/remake-artists-and-albums', methods=['GET', 'POST'])
def remake_artist_and_albums_view():
    return remake_artists_and_albums()

@main.route('/api/delete-artists-and-albums', methods=['GET', 'POST'])
def delete_artist_and_albums_view():
    delete_artists_and_albums()
    return {}

@main.route('/api/enable-songs', methods=['POST'])
def enable_songs_view():
    request_body = request.get_json(force=True)
    for song in request_body:
        db_song = SongModel.query.get(song["id"])
        db_song.enabled = True
    db.session.commit()
    create_fari_file(song["id"])
    return {} # TODO improve

@main.route('/api/disable-songs', methods=['POST'])
def disable_songs_view():
    request_body = request.get_json(force=True)
    for song in request_body:
        db_song = SongModel.query.get(song["id"])
        db_song.enabled = False
    db.session.commit()
    create_fari_file(song["id"])
    return {} # TODO improve

@main.route('/api/tag-list', methods=["GET"])
def tag_list_view():
    tags = TagModel.query.order_by(TagModel.name).all()
    return jsonify(TagSchema(many=True).dump(tags))

@main.route('/api/create-tag', methods=["POST"])
def create_tag_view():
    request_body = request.get_json(force=True)
    name = request_body["name"].upper()
    # check if the tag already exists
    search = TagModel.query.filter(TagModel.name == name).all()
    if search:
        return ({}, 400)
    # if it doesnt, continue
    tag = TagModel(
        name=name
    )
    db.session.add(tag)
    db.session.commit()
    return (jsonify(TagSchema().dump(tag)), 201)

@main.route('/api/delete-tag', methods=["DELETE"])
def delete_tag_view():
    request_body = request.get_json(force=True)
    tag = TagModel.query.get(request_body["id"])
    db.session.delete(tag)
    db.session.commit()
    # TODO update all affected fari files
    return ("", 204)

@main.route('/api/tag-song', methods=["POST"])
def tag_song_view():
    request_body = request.get_json(force=True)
    if "tag_id" not in request_body:
        return ("", 400)
    if "song_id" not in request_body:
        return ("", 400)
    song = SongModel.query.get(request_body["song_id"])
    tag = TagModel.query.get(request_body["tag_id"])
    song.tags.append(tag)
    db.session.commit()
    create_fari_file(request_body["song_id"])
    return ("", 200)

@main.route('/api/untag-song', methods=["POST"])
def untag_song_view():
    request_body = request.get_json(force=True)
    if "tag_id" not in request_body:
        return ("", 400)
    if "song_id" not in request_body:
        return ("", 400)
    song = SongModel.query.get(request_body["song_id"])
    tag = TagModel.query.get(request_body["tag_id"])
    song.tags.remove(tag)
    db.session.commit()
    create_fari_file(request_body["song_id"])
    return ("", 200)

@main.route('/api/add-tag-to-all', methods=['POST'])
def add_tag_to_all_view():
    # TODO remove this view
    # for testing only
    request_body = request.get_json(force=True)

    SongModel.query.order_by(SongModel.tracktitle).all()

    tag = TagModel(
        name=request_body["name"]
    )
    db.session.add(tag)

    all_songs = SongModel.query.order_by(SongModel.tracktitle).all()
    for song in all_songs:
        song.tags.append(tag)
    db.session.commit()

    return jsonify(TagSchema().dump(tag))

@main.route('/api/change-song-rating', methods=['POST'])
def change_song_rating_view():
    request_body = request.get_json(force=True)
    if "song_id" not in request_body:
        return ("", 400)
    if "rating" not in request_body:
        return ("", 400)
    song_rating = request_body["rating"]
    if not isinstance(song_rating, int):
        return ("", 400)
    song_rating = max(song_rating, 0)
    song_rating = min(song_rating, 5)
    song = SongModel.query.get_or_404(request_body["song_id"])
    song.rating = song_rating
    if song_rating == 0 or song_rating > 2:
        song.enabled = True
    else:
        song.enabled = False
    db.session.commit()
    create_fari_file(request_body["song_id"])
    return {}
