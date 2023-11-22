from flask import render_template
from . import api


@api.app_errorhandler(403)
def forbidden(e):
    return render_template('api/403.html'), 403


@api.app_errorhandler(404)
def page_not_found(e):
    return render_template('api/404.html'), 404


@api.app_errorhandler(500)
def internal_server_error(e):
    return render_template('api/500.html'), 500
