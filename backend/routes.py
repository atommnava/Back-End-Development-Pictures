from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=['GET'])
def get_pictures():
    """Returns all pictures."""
    if data:
        return jsonify(data), 200
    
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Returns a specific picture by its id."""
    # Adjusting for 0-based index
    try:
        for picture in data:
            if picture['id'] == id:
                return jsonify(picture), 200
        return jsonify({"message": "Picture not found"}), 404
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=['POST'])
def create_picture():
    """Creates a new picture."""
    try:
        new_picture = request.json
        # Check if a picture with the given id already exists
        for picture in data:
            if picture['id'] == new_picture['id']:
                return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302
        # Append the new picture to the data list
        data.append(new_picture)
        return jsonify(new_picture), 201
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Updates an existing picture by its id."""
    try:
        updated_picture = request.json
        for i, picture in enumerate(data):
            if picture['id'] == id:
                data[i] = updated_picture  # Update the picture
                return jsonify(updated_picture), 200

        return jsonify({"message": "picture not found"}), 404

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Deletes a picture by its id."""
    try:
        for i, picture in enumerate(data):
            if picture['id'] == id:
                del data[i]  # Delete the picture
                return '', 204  # HTTP_204_NO_CONTENT

        return jsonify({"message": "picture not found"}), 404

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
