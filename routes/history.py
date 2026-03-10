from flask import Blueprint, request, jsonify
from services.db_service import get_history, delete_translation, toggle_favorite

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
def get_history_route():
    try:
        limit = request.args.get('limit', 50, type=int)
        favorites_only = request.args.get('favorites', 'false').lower() == 'true'
        translations = get_history(limit=limit, favorites_only=favorites_only)
        return jsonify({
            'success': True,
            'translations': translations,
            'count': len(translations)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@history_bp.route('/history/<int:translation_id>', methods=['DELETE'])
def delete_history_item(translation_id):
    try:
        deleted = delete_translation(translation_id)
        if deleted:
            return jsonify({'success': True, 'message': 'Traduction supprimée'})
        return jsonify({'success': False, 'error': 'Traduction non trouvée'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@history_bp.route('/history/<int:translation_id>/favorite', methods=['POST'])
def toggle_favorite_route(translation_id):
    try:
        result = toggle_favorite(translation_id)
        if result:
            return jsonify({'success': True, 'is_favorite': result['is_favorite']})
        return jsonify({'success': False, 'error': 'Traduction non trouvée'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500