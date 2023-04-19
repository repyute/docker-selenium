from flask import Blueprint

from src.services.script import vnc

image_blueprint = Blueprint('image_blueprint', __name__)


@image_blueprint.route('/vnc/restart', methods=['GET'])
def restart_vnc():
    return vnc.restart()
