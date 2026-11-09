from flask import Blueprint, jsonify, request

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/image", methods=["POST"])
def upload_image():
    file = request.files.get("file")
    if not file:
        return jsonify({"success": False, "message": "No file received."}), 400

    filename = file.filename or "upload.png"
    return jsonify({"success": True, "message": "Upload endpoint ready.", "filename": filename})
