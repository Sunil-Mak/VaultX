from flask import jsonify

from . import ai_bp


@ai_bp.route("/")
def index():
    return jsonify(
        {
            "status": "online",
            "service": "VaultX AI",
            "version": "0.3.0"
        }
    )