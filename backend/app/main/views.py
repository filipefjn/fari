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
404 route for invalid API endpoints
"""
@main.route('/api/<path:path>')
def api_not_found_view(path):
    return ("", 404)


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
def song_file_view_v2(song_id):
    song_path = ContentController.get_song_path(song_id)
    if not song_path:
        return ("", 404)
    return flask.send_file(song_path, as_attachment=True, attachment_filename=song_path.split("/")[-1])


"""
Returns or updates the song's info
"""
@main.route('/api/v2/song/<song_id>/info', methods=['GET', 'PUT'])
def song_info_view_v2(song_id):
    if flask.request.method == 'GET':
        no_artwork = flask.request.args.get('noartwork')
        no_artwork = True if no_artwork is not None else False
        song_info = ContentController.get_song_info(song_id, no_artwork=no_artwork)
        if not song_info:
            return ("", 404)
        return flask.jsonify(song_info)
    elif flask.request.method == 'PUT':
        new_song_info = flask.request.get_json(force=True)
        if not new_song_info or not isinstance(new_song_info, dict):
            return ("", 400)
        final_song_info = ContentController.put_song_info(song_id, new_song_info)
        if not final_song_info:
            return ("", 400)
        return flask.jsonify(final_song_info)


"""
Applies tag to a list of songs
"""
@main.route('/api/v2/tag/<tag_name>/apply', methods=['POST'])
def apply_tag_view_v2(tag_name):
    tag_name = tag_name.upper()
    song_id_list = flask.request.get_json(force=True)
    if not song_id_list or not isinstance(song_id_list, list):
        return ("", 400)
    result = ContentController.apply_tag(tag_name, song_id_list)
    if not result:
        return ("", 500)
    return ""


"""
Removes tag from a list of songs
"""
@main.route('/api/v2/tag/<tag_name>/remove', methods=['POST'])
def remove_tag_view_v2(tag_name):
    tag_name = tag_name.upper()
    song_id_list = flask.request.get_json(force=True)
    if not song_id_list or not isinstance(song_id_list, list):
        return ("", 400)
    result = ContentController.remove_tag(tag_name, song_id_list)
    if not result:
        return ("", 500)
    return ""

