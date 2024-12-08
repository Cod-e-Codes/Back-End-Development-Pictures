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
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id): 
    if data:
        for x in data:
            if x["id"] == id:
                return jsonify(x), 200
    return {"message": "Internal server error"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        # Parse the incoming JSON data
        data2 = request.get_json()

        # Print incoming data for debugging
        print(f"Incoming Data: {data2}")

        # Check if the required fields are in the incoming data
        required_fields = ["id", "pic_url", "event_country", "event_state", "event_city", "event_date"]
        if not all(field in data2 for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        # Check if a picture with the same ID already exists
        for x in data:
            if x["id"] == data2["id"]:
                print(f"Duplicate found: {data2['id']}")
                return jsonify({"Message": f"picture with id {data2['id']} already present"}), 302

        # If no picture with the same ID exists, append the new picture
        data.append(data2)
        print(f"Added picture: {data2}")

        # Return the ID of the newly created picture with a 201 Created status
        return jsonify({"id": data2["id"]}), 201

    except Exception as e:
        # If any error occurs, return a 500 Internal Server Error with the error message
        return jsonify({"message": str(e)}), 500


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    data2 = request.get_json()

    # Find the picture by ID
    for i in range(len(data)):
        if data[i]["id"] == id:
            # Update the picture with the new data
            data[i].update(data2)  # Update with new data
            return jsonify(data[i]), 200  # Return the updated picture

    # If the picture was not found
    return jsonify({"message": "picture not found"}), 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        for i in range(len(data)):
            if data[i]["id"] == id:
                data.pop(i)
                return jsonify(Message=f"OK"), 204

    return {"message": "picture not found"}, 404