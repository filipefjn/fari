from .. import db, ma


### intermediate table between tags and songs ###
songs_tags_association = db.Table('songs_tags',
    db.Column('song', db.String(50), db.ForeignKey('songs.id'), primary_key=True),
    db.Column('tag', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
)


### tag model ###
class TagModel(db.Model):
    __tablename__ = 'tags'
    id          = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name        = db.Column(db.String(50), nullable=False)
    songs       = db.relationship("SongModel", secondary=songs_tags_association, back_populates="tags", lazy=True)

class TagSchema(ma.Schema):
    class Meta:
        model = TagModel
        fields = (
            "id",
            "name",
        )


### song model ###
class SongModel(db.Model):
    __tablename__ = 'songs'
    id          = db.Column(db.String(50), primary_key=True, nullable=False)
    path        = db.Column(db.String(100), nullable=False)
    enabled     = db.Column(db.Boolean, default=True)
    tracknumber = db.Column(db.Integer)
    tracktitle  = db.Column(db.String(50))
    artist      = db.Column(db.String(50))
    albumartist = db.Column(db.String(50))
    album_name  = db.Column(db.String(50))
    album_id    = db.Column(db.Integer, db.ForeignKey('albums.id'))
    tags        = db.relationship("TagModel", secondary=songs_tags_association, back_populates="songs", lazy=True)

class SongSchema(ma.Schema):
    class Meta:
        model = SongModel
        fields = (
            "id",
            "path",
            "enabled",
            "tracknumber",
            "tracktitle",
            "artist",
            "albumartist",
            "album_name",
            "album_id",
            "tags",
        )
    tags = ma.Nested(TagSchema, many=True)


### artist model ###
class ArtistModel(db.Model):
    __tablename__ = 'artists'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50))
    albums      = db.relationship('AlbumModel', backref="artist", lazy=True)

class ArtistSchema(ma.Schema):
    class Meta:
        model = ArtistModel
        fields = (
            "id",
            "name",
            "albums"
        )
    albums = ma.Nested("AlbumSchema", many=True)


### album model ###
class AlbumModel(db.Model):
    __tablename__ = 'albums'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50))
    artist_id   = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    songs       = db.relationship('SongModel', backref="album", lazy=True)

class AlbumSchema(ma.Schema):
    class Meta:
        model = AlbumModel
        fields = (
            "id",
            "name",
            "songs"
        )
    songs = ma.Nested("SongSchema", many=True)

