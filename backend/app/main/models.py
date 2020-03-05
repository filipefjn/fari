from .. import db, ma

songs_tags_association = db.Table('songs_tags',
    db.Column('songs', db.String(50), db.ForeignKey('songs.id'), primary_key=True),
    db.Column('tags', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
)

class TagModel(db.Model):
    __tablename__ = 'tags'
    id          = db.Column(db.Integer, primary_key=True, nullable=False)
    name        = db.Column(db.String(50), nullable=False)
    songs       = db.relationship("SongModel", secondary=songs_tags_association, back_populates="tags", lazy=True)

class TagSchema(ma.Schema):
    class Meta:
        model = TagModel
        fields = (
            "id",
            "name",
        )

class SongModel(db.Model):
    __tablename__ = 'songs'
    id          = db.Column(db.String(50), primary_key=True, nullable=False)
    path        = db.Column(db.String(100), nullable=False)
    enabled     = db.Column(db.Boolean, default=True)
    tracknumber = db.Column(db.Integer)
    tracktitle  = db.Column(db.String(50))
    artist      = db.Column(db.String(50))
    album       = db.Column(db.String(50))
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
            "album",
            "tags"
        )
    tags = ma.Nested(TagSchema, many=True)
