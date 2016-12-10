import flask as fl

from flask import Blueprint
from glb.controllers.store import StoreController
from glb.model import Platforms

bp = Blueprint('consumer', __name__, url_prefix='/observer-mode/rest/consumer')

@bp.route('/')
def main():
    return ''

@bp.route('/version')
def version():
    return '1.82.102'

@bp.route('/getGameMetaData/<platform_name>/<game_id>/token')
def meta_data(platform_name, game_id):
    platform = Platforms.from_name(platform_name)
    return StoreController(platform, game_id).meta_data()

@bp.route('/getGameDataChunk/<platform_name>/<game_id>/<chunk_id>/token')
def chunk_frame(platform_name, game_id, chunk_id):
    platform = Platforms.from_name(platform_name)
    return StoreController(platform, game_id).chunk_frame(chunk_id)

@bp.route('/getLastChunkInfo/<platform_name>/<game_id>/0/token')
def last_chunk_info(platform_name, game_id):
    platform = Platforms.from_name(platform_name)
    return StoreController(platform, game_id).last_chunk()

@bp.route('/getKeyFrame/<platform_name>/<game_id>/<frame_id>/token')
def key_frame(platform_name, game_id, frame_id):
    platform = Platforms.from_name(platform_name)
    return StoreController(platform, game_id).key_frame(frame_id)
