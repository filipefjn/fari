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
            # tag was found
            # look for the songs which have the tag
            song_id_list = []
            for song in SongModel.query.filter(SongModel.tags.contains(found_tag)):
                song_id_list.append(song.id)
            # delete the tag
            db.session.delete(found_tag)
            db.session.commit()
            # recreate the songs' fari file
            for song_id in song_id_list:
                LibraryController.create_fari_file(song_id)
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
        path = os.path.join(settings["library_path"], path)
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

        # get tags and rating
        song = SongModel.query.get(song_id)
        song_info["rating"] = song.rating
        tags = list(TagSchema(many=True).dump(song.tags))
        tags = list(map(lambda x: x["name"], tags))
        song_info["tags"] = tags
        song_info["enabled"] = song.enabled

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
        update_fari_file = False
        SongModel.query.filter(SongModel.id == song_id).update(song_db_update)
        song = SongModel.query.get(song_id)
        song.track_order = "%02d-%03d" % (song.discnumber, song.tracknumber)
        if 'rating' in new_song_info:
            # attempt to update rating
            rating = int(new_song_info['rating'])
            rating = max(rating, 0)
            rating = min(rating, 5)
            song.rating = rating
            update_fari_file = True
        if 'enabled' in new_song_info:
            # attempt to update enabled
            enabled = bool(new_song_info['enabled'])
            song.enabled = enabled
            update_fari_file = True
        if update_fari_file:
            # update fari file
            LibraryController.create_fari_file(song.id)

        # update artists/albums
        LibraryController.update_artists_and_albums(commit=False, song_id=song_id)

        # commit changes
        song_file.save()
        db.session.commit()
        return self.get_song_info(song_id, no_artwork=True)


    """
    Applies tag to a list of songs
    """
    @classmethod
    def apply_tag(self, tag_name, song_id_list, **kwargs):
        # get tag
        tag = TagModel.query.filter(TagModel.name.ilike(tag_name)).first()

        # if it doesn't exist, create it
        if not tag:
            self.create_tag(tag_name)
            tag = TagModel.query.filter(TagModel.name.ilike(tag_name)).first()

        for song in SongModel.query.filter(SongModel.id.in_(song_id_list)).all():
            song.tags.append(tag)
            db.session.commit()
            LibraryController.create_fari_file(song.id)

        db.session.commit()
        return True


    """
    Removes tag from a list of songs
    """
    @classmethod
    def remove_tag(self, tag_name, song_id_list, **kwargs):
        # get tag
        tag = TagModel.query.filter(TagModel.name.ilike(tag_name)).first()

        # if it doesn't exist, do nothing
        if not tag:
            return True

        for song in SongModel.query.filter(SongModel.id.in_(song_id_list)).all():
            song.tags.remove(tag)
            db.session.commit()
            LibraryController.create_fari_file(song.id)

        db.session.commit()
        return True

