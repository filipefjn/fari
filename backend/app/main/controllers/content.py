from flask import current_app as app
from ... import db
from ...settings import settings
from ..models import *

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

