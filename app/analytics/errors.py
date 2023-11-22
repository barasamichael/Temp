from flask import render_template
from . import analytics


@analytics.app_errorhandler(403)
def forbidden(e):
    return render_template('analytics/403.html'), 403


@analytics.app_errorhandler(404)
def page_not_found(e):
    return render_template('analytics/404.html'), 404


@analytics.app_errorhandler(500)
def internal_server_error(e):
    return render_template('analytics/500.html'), 500
