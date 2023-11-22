import os
import flask
import glob
from flask_login import login_required, current_user
from . import account
from ..models import User


@account.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    """Renders details of user with user_id for display"""
    return flask.render_template('account/user_profile.html', user_id = user_id)


@account.route('/dashboard')
@login_required
def dashboard():
    """"""
    return flask.render_template('account/dashboard.html')


@account.route('/users')
@login_required
def view_users():
    """"""
    return flask.render_template('account/get_users.html')


@account.route('/authors')
@login_required
def view_authors():
    """"""
    return flask.render_template('account/get_authors.html')


@account.route('/roles')
@login_required
def view_roles():
    """"""
    return flask.render_template('account/get_roles.html')


@account.route('/books')
@login_required
def view_books():
    """"""
    return flask.render_template('account/get_books.html')


@account.route('/raffles')
@login_required
def view_raffles():
    """"""
    return flask.render_template('account/get_raffles.html')


@account.route('/tickets')
@login_required
def view_tickets():
    """"""
    return flask.render_template('account/view_tickets.html')


@account.route('/profile')
@login_required
def view_profile():
    """"""
    return flask.render_template('account/view_profile.html')


@account.route('/settings')
@login_required
def settings():
    """"""
    return flask.render_template('account/settings.html')


@account.route('/categories')
@login_required
def view_categories():
    """"""
    return flask.render_template('account/get_categories.html')


@account.route('/book/image')
@login_required
def upload_book_image():
    """"""
    return flask.render_template('account/upload_book_image.html')


@account.route('/book/images')
@login_required
def upload_book_images():
    """"""
    return flask.render_template('account/upload_book_images.html')


@account.route('/author/image')
@login_required
def upload_author_image():
    """"""
    return flask.render_template('account/upload_author_image.html')


@account.route('/user/image')
@login_required
def upload_user_image():
    """"""
    return flask.render_template('account/upload_user_image.html')

@account.route("/user/update")
@login_required
def update_user():
    return flask.render_template("account/update_user.html")


@account.route('/transactions')
@login_required
def view_transactions():
    """"""
    return flask.render_template('account/transactions.html')


@account.route('/gallery')
@login_required
def gallery():
    """"""
    image_folder = os.path.join(flask.current_app.config["BASE_DIRECTORY"] + 
            '/app/static/img/nduundune/')
    images = glob.glob(os.path.join(image_folder, '*'))
    images = [image.rsplit('/')[-1] for image in images]
    return flask.render_template('account/gallery.html', images = images)


@account.route('/events')
@login_required
def view_events():
    """"""
    return flask.render_template('account/view_events.html')


@account.route('/explore-books')
@login_required
def explore_books():
    """"""
    return flask.render_template('account/explore_books.html')


@account.route('/explore-authors')
@login_required
def explore_authors():
    """"""
    return flask.render_template('account/explore_authors.html')


@account.route('/explore-raffles')
@login_required
def explore_raffles():
    """"""
    return flask.render_template('account/explore_raffles.html')


@account.route('/explore-tickets')
@login_required
def explore_tickets():
    """"""
    return flask.render_template('account/explore_tickets.html')


@account.route('/won_raffles')
@login_required
def won_raffles():
    """"""
    return flask.render_template('account/won_raffles.html')


@account.route('/explore_winners')
@login_required
def explore_winners():
    """"""
    return flask.render_template('account/explore_winners.html')


@account.route('/past-raffles')
@login_required
def past_raffles():
    """"""
    return flask.render_template('account/past_raffles.html')


@account.route('/reports')
@login_required
def reports():
    """"""
    return flask.render_template('account/reports.html')


@account.route('/notifications')
@login_required
def notifications():
    """"""
    return flask.render_template('account/notifications.html')


@account.route('/explore-events')
@login_required
def explore_events():
    """"""
    return flask.render_template('account/explore_events.html')


@account.route('/authors/<int:author_id>')
@login_required
def author_profile(author_id):
    """"""
    return flask.render_template('account/author_profile.html', 
            author_id = author_id)
