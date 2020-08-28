from flask import current_app as app
from ... import db
from ...settings import settings
from ..models import *
from .common import CommonController
import os
import re
import json
import music_tag

class LibraryController:
    """
    Updates the library
    """
    @classmethod
    def update(self, **kwargs):
        app.logger.info("Starting library update")
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        # search for new songs
        new_songs_list = self.search_new_songs()

        # add new songs
        self.add_songs(new_songs_list, commit=False)

        # update the artists and albums
        self.update_artists_and_albums(commit=False)

        # commit
        if kwargs['commit']:
            db.session.commit()


    """
    Remakes the whole library
    """
    @classmethod
    def remake(self, **kwargs):
        app.logger.info("Starting library remake")
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        # delete the whole library
        self.delete(commit=False)

        # remake t he whole library
        self.update(commit=False)

        # commit
        if kwargs['commit']:
            db.session.commit()


    """
    Deletes the whole library
    """
    @classmethod
    def delete(self, **kwargs):
        app.logger.info("Starting library delete")
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        # delete all the artists (and albums)
        self.delete_artists_and_albums(commit=False)

        # delete all the songs and tags
        self.delete_songs_and_tags(commit=False)

        # commit
        if kwargs['commit']:
            db.session.commit()


    """
    Cleans the missing content from the library
    """
    @classmethod
    def clean(self, **kwargs):
        app.logger.info("Starting library clean")
        app.logger.warning("Not yet implemented")
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        # TODO implement

        # commit
        if kwargs['commit']:
            db.session.commit()


    """
    Deletes all the artists and albums
    """
    @classmethod
    def delete_artists_and_albums(self, **kwargs):
        app.logger.info("Starting artists and albums delete")
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        # delete all the albums from the database
        SongModel.query.update({"album_id": None})
        AlbumModel.query.delete()

        # delete all the artists from the database
        ArtistModel.query.delete()

        # commit
        if kwargs['commit']:
            db.session.commit()


    """
    Updates the artists and albums
    """
    @classmethod
    def update_artists_and_albums(self, **kwargs):
        app.logger.info("Starting artists and albums update")
        if 'commit' not in kwargs:
            kwargs['commit'] = True
        if 'song_id' not in kwargs:
            kwargs['song_id'] = None

        artists_added = 0
        albums_added = 0
        song_query = SongModel.query

        # check if should update only a single song
        if kwargs['song_id']:
            song_query = song_query.filter(SongModel.id == kwargs['song_id'])

        for song in song_query.all():
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
                artists_added += 1

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
                albums_added += 1

        app.logger.info("Artists added: %d", artists_added)
        app.logger.info("Albums added: %d", albums_added)

        # commit
        if kwargs['commit']:
            db.session.commit()


    """
    Deletes all the songs and tags
    """
    @classmethod
    def delete_songs_and_tags(self, **kwargs):
        app.logger.info("Starting songs and tags delete")
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        # delete all songs and tags from database
        for song in SongModel.query.all():
            db.session.delete(song)
        for tag in TagModel.query.all():
            db.session.delete(tag)

        # commit
        if kwargs['commit']:
            db.session.commit()


    """
    Creates a new tag if it doesn't exist already
    """
    @classmethod
    def create_tag(self, tag_name, **kwargs):
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        # check if the tag already exists
        queried_tag = TagModel.query.filter(TagModel.name == tag_name).first()

        if queried_tag:
            # tag already exists
            return queried_tag

        # create and add tag
        created_tag = TagModel(
            name=tag_name
        )
        db.session.add(created_tag)

        # commit
        if kwargs['commit']:
            db.session.commit()
        return created_tag


    """
    Creates a .fari file for a given song id
    """
    @classmethod
    def create_fari_file(self, song_id, **kwargs):
        # find song
        song = SongSchema().dump(SongModel.query.get(song_id))
        if song is None:
            app.logger.error("Song '%s' was not found. It was not possible to create its fari file" % song_id)
            return
        fari_file_content = {}
        fari_file_content["id"] = song["id"]
        fari_file_content["enabled"] = song["enabled"]
        fari_file_content["rating"] = song["rating"]
        fari_file_content["tags"] = []
        for tag in song["tags"]:
            fari_file_content["tags"].append(tag["name"])

        # fari file path
        song_path = re.sub(r"^/", r"", song["path"])
        fari_file_path = os.path.join(settings["library_path"], song_path) + ".fari"

        # create fari file
        with open(fari_file_path, "w") as file:
            # write file info in json
            file.write(json.dumps(fari_file_content))


    """
    Searches for new song files

    Returns a list with the file paths
    """
    @classmethod
    def search_new_songs(self, **kwargs):
        app.logger.info("Starting new songs search")

        # get songs from the library directory
        dir_files_list = []
        for root, dirs, files in os.walk(settings["library_path"]):
            for file in files:
                if re.search(re.compile(settings["file_regex"], re.IGNORECASE), file) is not None:
                    file_path = os.path.join(root, file)
                    dir_files_list.append(file_path)

        # get songs on the database
        db_files_list = []
        query_result = SongModel.query.with_entities(SongModel.path).all()
        path_prefix = re.sub(r"\/+$", "", settings["library_path"])
        for file in query_result:
            db_files_list.append(path_prefix + file[0])

        # get new songs
        new_files_list = list(set(dir_files_list) - set(db_files_list))
        app.logger.info("New songs found: %d", len(new_files_list))
        return new_files_list


    """
    Searches for missing song files

    Returns a list with the file paths
    """
    @classmethod
    def search_missing_songs(self, **kwargs):
        app.logger.info("Starting missing songs search")

        # get songs from the library directory
        dir_files_list = []
        for root, dirs, files in os.walk(settings["library_path"]):
            for file in files:
                if re.search(re.compile(settings["file_regex"], re.IGNORECASE), file) is not None:
                    file_path = os.path.join(root, file)
                    dir_files_list.append(file_path)

        # get songs on the database
        db_files_list = []
        query_result = SongModel.query.with_entities(SongModel.path).all()
        path_prefix = re.sub(r"\/+$", "", settings["library_path"])
        for file in query_result:
            db_files_list.append(path_prefix + file[0])

        # get new songs
        missing_files_list = list(set(db_files_list) - set(dir_files_list))
        app.logger.info("New songs found: %d", len(missing_files_list))
        return missing_files_list


    """
    Add songs to the library
    """
    @classmethod
    def add_songs(self, file_list, **kwargs):
        app.logger.info("Starting songs add")
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        songs_added = 0
        fari_files_found = 0
        fari_files_created = 0
        for file in file_list:
            file_absolute_path = os.path.join(settings["library_path"], file)
            file_tags = music_tag.load_file(file_absolute_path)
            song_id = CommonController.generate_id(str(file_tags["tracktitle"].value) + str(file_tags["artist"].value))
            song_tracknumber = CommonController.extract_integer_or(file_tags["tracknumber"].value, 0)
            song_discnumber = CommonController.extract_integer_or(file_tags["discnumber"].value, 1)
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

            # look for .fari file
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
                            song.tags.append(self.create_tag(tag_name, commit=False))
                    fari_files_found += 1

            # insert song into the database
            db.session.add(song)
            songs_added += 1

            # if .fari file does not exist, create one
            if not fari_file_exists:
                self.create_fari_file(song_id)
                fari_files_created += 1

        app.logger.info("Songs added: %d", songs_added)
        app.logger.info("Fari files created: %d", fari_files_created)

        # commit
        if kwargs['commit']:
            db.session.commit()


    """
    Removes songs from the library
    """
    @classmethod
    def remove_songs(self, file_list, **kwargs):
        app.logger.info("Starting songs remove")
        app.logger.warning("Not yet implemented")
        if 'commit' not in kwargs:
            kwargs['commit'] = True

        # TODO implement

        # commit
        if kwargs['commit']:
            db.session.commit()

