from flask import Blueprint, current_app

account = Blueprint('account', __name__, url_prefix = '/account')
from . import views, errors

@account.app_context_processor
def global_variables():
    """
    Provides global variables that can be accessed directly within templates
    belonging to the 'account' blueprint.

    Returns:
        dict: A dictionary containing global variables to be injected into 
        templates.
    """
    return dict(
            app_name = current_app.config['ORGANIZATION_NAME'], 
            api_server = current_app.config['API_SERVER_INDEX']
            )
