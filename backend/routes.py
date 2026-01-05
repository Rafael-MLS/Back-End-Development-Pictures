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
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a specific picture by ID"""
    # Loop through each picture in the data list
    for picture in data:
        # Check if the current picture has the matching id
        if picture["id"] == id:
            # Return the found picture as JSON with 200 status
            return jsonify(picture), 200
    
    # If no picture found with the given id, return 404 error
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["POST"])
@app.route("/picture", methods=["POST"])
def create_picture():

    # get data from the json body
    picture_in = request.json
    print(picture_in)

    # if the id is already there, return 303 with the URL for the resource
    for picture in data:
        if picture_in["id"] == picture["id"]:
            return {
                "Message": f"picture with id {picture_in['id']} already present"
            }, 302

    data.append(picture_in)
    return picture_in, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    # Get the updated picture data from the request body
    updated_picture = request.get_json()
    
    # Check if the picture data is valid
    if not updated_picture:
        return jsonify({"message": "Invalid input"}), 400
    
    # Look for the picture with the given id
    for i, picture in enumerate(data):
        if picture["id"] == id:
            # Update the existing picture with new data
            # Keep the id from the URL, not from request body
            updated_picture["id"] = id
            data[i] = updated_picture
            return jsonify(updated_picture), 200
    
    # If picture not found, return 404
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by id"""
    # Look for the picture with the given id
    for i, picture in enumerate(data):
        if picture["id"] == id:
            # Remove the picture from the data list
            del data[i]
            # Return empty body with 204 No Content status
            return "", 204
    
    # If picture not found, return 404
    return jsonify({"message": "picture not found"}), 404
