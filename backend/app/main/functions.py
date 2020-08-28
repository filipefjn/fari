from flask import current_app as app
from .. import db
from .models import *
from ..settings import settings
import music_tag
from base64 import b64encode
import os
import re
import random
import hashlib
import json
import time

def gen_id(base_str):
    h = str(base_str) + str(random.randint(100000, 999999))
    h = hashlib.sha1(h.encode("utf-8"))
    return h.hexdigest()

def get_song_artwork_base64(path):
    if not path:
        return None
    path = re.sub(r'^/', '', path)
    path = re.sub(r'\.\./', '', path)
    path = os.path.join(settings["library_path"], path)
    if not os.path.exists(path):
        return None
    if not os.path.isfile(path):
        return None
    file = music_tag.load_file(path)
    artwork = file['artwork']
    if artwork.first is not None:
        return "data:" + artwork.first.mime + ";base64," + b64encode(artwork.first.data).decode('ascii')
    else:
        return None

def create_fari_file(song_id):
    # find file in database
    song_row = SongSchema().dump(SongModel.query.get(song_id))
    fari_file_content = {}
    fari_file_content["id"] = song_row["id"]
    fari_file_content["enabled"] = song_row["enabled"]
    fari_file_content["rating"] = song_row["rating"]
    fari_file_content["tags"] = []
    for tag in song_row["tags"]:
        fari_file_content["tags"].append(tag["name"])

    # generate fari file path
    song_path = re.sub(r"^/", r"", song_row["path"])
    fari_file_path = os.path.join(settings["library_path"], song_path) + ".fari"

    # create fari file
    with open(fari_file_path, "w") as file:
        # write file info in json
        file.write(json.dumps(fari_file_content))

    return fari_file_content

def get_or_create_tag(tag_name, **kwargs):
    # check if the tag already exists
    queried_tag = TagModel.query.filter(TagModel.name == tag_name).first()
    if queried_tag:
        return queried_tag
    else:
        created_tag = TagModel(
            name=tag_name
        )
        db.session.add(created_tag)
        if 'commit' not in kwargs:
            kwargs['commit'] = True
        if kwargs['commit']:
            db.session.commit()
        return created_tag

def delete_artists_and_albums():
    # set all songs' albums to null
    SongModel.query.update({"album_id": None})
    db.session.commit()
    # delete all artists and albums from database
    AlbumModel.query.delete()
    ArtistModel.query.delete()
    db.session.commit()


def remake_artists_and_albums(**kwargs):
    # start time
    start_time = time.time()

    # delete artists and albums
    if 'delete' not in kwargs:
        kwargs['delete'] = True
    if kwargs['delete']:
        delete_artists_and_albums()

    artists_found = 0
    albums_found = 0

    for song in SongModel.query.all():
        # get song's artist name
        song_artist_name = song.albumartist
        if not song_artist_name:
            song_artist_name = song.artist
        if not song_artist_name:
            song_artist_name = "Unknown artist"

        # look for artist
        song_artist = ArtistModel.query.filter(ArtistModel.name.ilike(song_artist_name)).first()
        if not song_artist:
            # create a new artist
            song_artist = ArtistModel(
                name=song_artist_name
            )
            db.session.add(song_artist)
            artists_found += 1

        # get song's album name
        song_album_name = song.album_name
        if not song_album_name:
            song_album_name = "Unknown album"

        # check if album exists
        found_album = False
        for album in song_artist.albums:
            if album.name.lower() == song_album_name.lower():
                found_album = True
                song.album = album
                break

        # if does not, create it
        if not found_album:
            song_album = AlbumModel(
                name=song_album_name,
                artist=song_artist,
                year=song.year
            )
            song.album = song_album
            albums_found += 1

    if 'commit' not in kwargs:
        kwargs['commit'] = True
    if kwargs['commit']:
        db.session.commit()

    app.logger.info("Remake artists took %.2fs" % (time.time() - start_time))

    return {
        "artists_found": artists_found,
        "albums_found": albums_found
    }

def extract_integer_or(value, default = 1):
    if isinstance(value, int):
        return value
    matches = re.match(r"^\d+", value)
    if not matches:
        return int(default)
    else:
        return int(matches.group())

def remake_library():
    app.logger.info("Starting library remake")

    # delete all artists and albums from database
    delete_artists_and_albums()

    # delete all songs and tags from database
    for song in SongModel.query.all():
        db.session.delete(song)
    for tag in TagModel.query.all():
        db.session.delete(tag)
    db.session.commit()

    # start time
    start_time = time.time()

    # search directory
    filtered_file_list = []
    for root, dirs, files in os.walk(settings["library_path"]):
        for file in files:
            if re.search(re.compile(settings["file_regex"], re.IGNORECASE), file) is not None:
                file_path = os.path.join(root, file)
                filtered_file_list.append(file_path)

    # files loop
    fari_files_found = 0
    songs_found = 0
    fari_files_created = 0
    for file in filtered_file_list:
        file_absolute_path = os.path.join(settings["library_path"], file)
        file_tags = music_tag.load_file(file_absolute_path)
        song_id = gen_id(str(file_tags["tracktitle"].value) + str(file_tags["artist"].value))
        song_tracknumber = extract_integer_or(file_tags["tracknumber"].value, 0)
        song_discnumber = extract_integer_or(file_tags["discnumber"].value, 1)
        song_track_order = "%02d-%03d" % (song_discnumber, song_tracknumber)
        song = SongModel(
            id=song_id,
            path=file_absolute_path.replace(settings["library_path"], "/", 1),
            enabled=True,
            tracknumber=song_tracknumber,
            tracktitle=file_tags["tracktitle"].value,
            albumartist=file_tags["albumartist"].value,
            artist=file_tags["artist"].value,
            album_name=file_tags["album"].value,
            discnumber=song_discnumber,
            track_order=song_track_order,
            year=file_tags["year"].value
        )
        # check for .fari file
        fari_file_absolute_path = file_absolute_path + ".fari"
        fari_file_exists = os.path.exists(fari_file_absolute_path)

        # if .fari file exists, extract info from it
        if fari_file_exists:
            with open(fari_file_absolute_path, "r") as fari_file:
                fari_file_content = json.loads(fari_file.read())
                if "id" in fari_file_content:
                    song_id = fari_file_content["id"]
                    song.id = fari_file_content["id"]
                if "enabled" in fari_file_content:
                    song.enabled = fari_file_content["enabled"]
                if "rating" in fari_file_content:
                    song.rating = fari_file_content["rating"]
                if "tags" in fari_file_content:
                    tag_list = []
                    for tag_name in fari_file_content["tags"]:
                        song.tags.append(get_or_create_tag(tag_name, commit=False))
                fari_files_found += 1

        # insert song into the database
        db.session.add(song)
        songs_found += 1

        # if .fari file does not exist, create one
        if not fari_file_exists:
            create_fari_file(song_id)
            fari_files_created += 1

    app.logger.info("Songs search took %.2fs" % (time.time() - start_time))

    # remake artists and albums
    remake_artists_and_albums_result = remake_artists_and_albums(delete=False, commit=False)

    # commit all changes
    db.session.commit()

    total_time = time.time() - start_time
    app.logger.info("Library remake took %.2fs" % total_time)

    return {
        "songs_found": songs_found,
        "fari_files_found": fari_files_found,
        "fari_files_created": fari_files_created,
        "total_time": total_time,
        **remake_artists_and_albums_result,
    }

