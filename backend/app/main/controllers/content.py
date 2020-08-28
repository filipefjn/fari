from flask import current_app as app
import flask
from ... import db
from ...settings import settings
from ..models import *
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

