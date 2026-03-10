import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

from routes.translate import translate_bp
from routes.history import history_bp

app.register_blueprint(translate_bp)
app.register_blueprint(history_bp)

from services.db_service import init_db
init_db()

@app.route('/', methods=['GET'])
def home():
    return {
        'message': 'Teckia API is running! 🚀',
        'version': '1.0.0',
        'database': 'PostgreSQL local',
        'endpoints': ['/translate', '/history']
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)