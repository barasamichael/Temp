from flask import Blueprint, current_app

analytics = Blueprint('analytics', __name__)
from . import views, errors

@analytics.app_context_processor
def global_variables():
    """
    Provides global variables that can be accessed directly within templates
    belonging to the 'analytics' blueprint.

    Returns:
        dict: A dictionary containing global variables to be injected into 
        templates.
    """
    return dict(app_name = current_app.config['ORGANIZATION_NAME'])
