from flask import Blueprint, request, jsonify
from services.groq_service import translate_text, detect_language
from services.db_service import save_translation

translate_bp = Blueprint('translate', __name__)

@translate_bp.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Données manquantes'}), 400

        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'mg')

        if not text:
            return jsonify({'success': False, 'error': 'Texte vide'}), 400

        if len(text) > 2000:
            return jsonify({'success': False, 'error': 'Texte trop long (max 2000 caractères)'}), 400

        # Détection automatique de langue
        if source_lang == 'auto':
            source_lang = detect_language(text)
            auto_detected = True
        else:
            auto_detected = False

        # Vérification langues supportées
        supported = ['mg', 'fr', 'en', 'es', 'ar', 'zh', 'de', 'pt']
        if source_lang not in supported or target_lang not in supported:
            return jsonify({'success': False, 'error': 'Langue non supportée'}), 400

        if source_lang == target_lang:
            return jsonify({'success': False, 'error': 'Les langues source et cible sont identiques'}), 400

        # Traduction
        translation = translate_text(text, source_lang, target_lang)

        # Sauvegarde
        saved = save_translation(source_lang, target_lang, text, translation)

        return jsonify({
            'success': True,
            'translation': translation,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'auto_detected': auto_detected,
            'id': saved['id'] if saved else None
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@translate_bp.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        if not text:
            return jsonify({'success': False, 'error': 'Texte vide'}), 400

        detected = detect_language(text)
        return jsonify({'success': True, 'language': detected})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500