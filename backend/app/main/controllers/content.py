from flask import current_app as app
import flask
from ... import db
from ...settings import settings
from ..models import *
from base64 import b64encode
from .library import LibraryController
import music_tag
import os
import re

class ContentController:
    """
    Return the artists
    """
    @classmethod
    def get_artists(self, **kwargs):
        artist_list = ArtistModel.query.all()
        return ArtistSchema(many=True).dump(artist_list)


    """
    Returns the albums and songs of an artist
    """
    @classmethod
    def get_artist_content(self, artist_id, **kwargs):
        artist = ArtistModel.query.get(artist_id)
        return ArtistNestedSchema().dump(artist)


    """
    Returns the tags
    """
    @classmethod
    def get_tags(self, **kwargs):
        tag_list = TagModel.query.order_by(TagModel.name).all()
        return TagSchema(many=True).dump(tag_list)


    """
    Creates a tag if it does not exist
    """
    @classmethod
    def create_tag(self, tag_name, **kwargs):
        found_tag = TagModel.query.filter(TagModel.name.ilike(tag_name)).first()
        if found_tag:
            app.logger.info("Tag '%s' already exists" % tag_name)
            # tag already exists
            return TagSchema().dump(found_tag)

        # tag does not exist, create it
        new_tag = TagModel(
            name=tag_name
        )
        db.session.add(new_tag)
        db.session.commit()
        return TagSchema().dump(new_tag)


    """
    Deletes a tag if it exists
    """
    @classmethod
    def delete_tag(self, tag_name, **kwargs):
        found_tag = TagModel.query.filter(TagModel.name.ilike(tag_name)).first()
        if found_tag:
            # tag was found, delete it
            db.session.delete(found_tag)
            db.session.commit()
            app.logger.info("Tag '%s' deleted" % tag_name)
            return True
        else:
            # tag was not found
            app.logger.info("Tag '%s' was not found" % tag_name)
            return False


    """
    Get a song's path
    """
    @classmethod
    def get_song_path(self, song_id, **kwargs):
        song = SongModel.query.get(song_id)
        if not song:
            # the song was not found
            return False

        # prepare path
        path = os.path.normpath(song.path)
        path = re.sub(r"^\/", "", path)
        path = os.path.join(settings["media_dir"], path)
        path = os.path.normpath(path)

        # check if path exists and is a file
        if not os.path.exists(path) or not os.path.isfile(path):
            app.logger.info("File '%s' does not exist" % path)
            return False

        return path


    """
    Get a song's info
    """
    @classmethod
    def get_song_info(self, song_id, **kwargs):
        if 'no_artwork' not in kwargs:
            kwargs['no_artwork'] = False
        song_path = self.get_song_path(song_id)
        if not song_path:
            # the song was not found
            return False

        # get metadata
        song_info = {}
        song_file = music_tag.load_file(song_path)
        for metadata_tag in settings["metadata_tags"]:
            song_info[metadata_tag] = song_file[metadata_tag].value

        if not kwargs['no_artwork']:
            # get artwork if any
            song_artwork = song_file['artwork']
            if song_artwork.first is not None:
                song_info["artwork"] = "data:" + song_artwork.first.mime + ";base64," + b64encode(song_artwork.first.data).decode('ascii')

        return song_info


    """
    Updates a song's info
    """
    @classmethod
    def put_song_info(self, song_id, new_song_info, **kwargs):
        song_path = self.get_song_path(song_id)
        if not song_path:
            # the song was not found
            return False

        song_file = music_tag.load_file(song_path)

        # get the valid metadata tags from new song info
        new_song_info_keys = list(new_song_info.keys())
        new_song_info_keys = list(set(new_song_info_keys) & set(settings["metadata_tags"]))

        # TODO artwork

        # update song file
        song_db_update = {}
        for metadata_tag in new_song_info_keys:
            song_file[metadata_tag] = new_song_info[metadata_tag]
            if metadata_tag in settings["metadata_tags_to_song_model"]:
                song_db_update[settings["metadata_tags_to_song_model"][metadata_tag]] = new_song_info[metadata_tag]

        # update song on the database
        SongModel.query.filter(SongModel.id == song_id).update(song_db_update)
        song = SongModel.query.get(song_id)
        song.track_order = "%02d-%03d" % (song.discnumber, song.tracknumber)
        LibraryController.update_artists_and_albums(commit=False, song_id=song_id)

        # commit changes
        song_file.save()
        db.session.commit()
        return self.get_song_info(song_id, no_artwork=True)

