from flask import current_app as app
import flask
from . import main
from .controllers import LibraryController, ContentController

"""
Returns the frontend's entrypoint
"""
@main.route('/', defaults={'path':''})
@main.route('/<path:path>')
def root_view(path):
    return flask.render_template('index.html')


"""
Deletes the library
"""
@main.route('/api/v2/library/delete', methods=['POST'])
def library_delete_view_v2():
    LibraryController.delete()
    return ""


"""
Cleans the library
"""
@main.route('/api/v2/library/clean', methods=['POST'])
def library_clean_view_v2():
    LibraryController.clean()
    return ""


"""
Updates the library
"""
@main.route('/api/v2/library/update', methods=['POST'])
def library_update_view_v2():
    LibraryController.update()
    return ""


"""
Remakes the library
"""
@main.route('/api/v2/library/remake', methods=['POST'])
def remake_library_view_v2():
    LibraryController.remake()
    return ""


"""
Returns the artists
"""
@main.route('/api/v2/artists', methods=['GET'])
def artists_view_v2():
    artist_list = ContentController.get_artists()
    return flask.jsonify(artist_list)


"""
Returns the albums and songs of an artist
"""
@main.route('/api/v2/artist/<artist_id>', methods=['GET'])
def get_artist_view_v2(artist_id):
    artist = ContentController.get_artist_content(artist_id)
    if not artist:
        return ("", 404)
    return flask.jsonify(artist)


"""
Returns the tags
"""
@main.route('/api/v2/tags', methods=['GET'])
def tags_view_v2():
    tag_list = ContentController.get_tags()
    return flask.jsonify(tag_list)


"""
Creates or deletes a tag
"""
@main.route('/api/v2/tag/<tag_name>', methods=['POST', 'DELETE'])
def tag_view_v2(tag_name):
    tag_name = tag_name.upper()
    if flask.request.method == 'POST':
        tag = ContentController.create_tag(tag_name)
        return flask.jsonify(tag)
    elif flask.request.method == 'DELETE':
        result = ContentController.delete_tag(tag_name)
        if not result:
            return ("", 404)
        else:
            return ("", 200)


"""
Returns the song's file
"""
@main.route('/api/v2/song/<song_id>/file', methods=['GET'])
def get_song_file_view_v2(song_id):
    song_path = ContentController.get_song_path(song_id)
    if not song_path:
        return ("", 404)
    return flask.send_file(song_path, as_attachment=True, attachment_filename=song_path.split("/")[-1])

