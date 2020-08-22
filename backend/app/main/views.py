import flask
from . import main
from .controllers import LibraryController

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
