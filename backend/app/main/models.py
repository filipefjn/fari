from .. import db, ma

class SongModel(db.Model):
    __tablename__ = 'songs'
    id          = db.Column(db.String(50), primary_key=True, nullable=False)
    path        = db.Column(db.String(100), nullable=False)
    enabled     = db.Column(db.Boolean, unique=True)
    tracknumber = db.Column(db.Integer)
    tracktitle  = db.Column(db.String(50))
    artist      = db.Column(db.String(50))
    album       = db.Column(db.String(50))

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
            "album"
        )
