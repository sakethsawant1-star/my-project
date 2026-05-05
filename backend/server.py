from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from phase3 import build_prompt
from phase4 import get_recommendations

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    payload = request.json
    if not payload:
        return jsonify({"error": "No payload provided"}), 400
        
    # Phase 3: Construct Prompt
    prompt, error = build_prompt(payload)
    if error:
        return jsonify({"error": error}), 404
        
    # Phase 4: Get LLM Recommendations
    recommendations = get_recommendations(prompt)
    
    return jsonify(recommendations)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
