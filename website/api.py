from flask import Blueprint, request, current_app, jsonify
from flask_login import login_required, current_user
import os
from datetime import datetime, timedelta
import requests
import json

from .models import Species, UserSpecies, User
from . import db
from .img_url import img_url

api = Blueprint("api", __name__)

def request_api(save_path, lat, lon):
    url = "http://birdin-api.csie.org:12345/analyze_api"
    files = {'audio': open(save_path,'rb')}
    data = {
        'lat': lat,
        'lon': lon
    }
    r = requests.post(url, files=files, data=data)
    return r

def process_detections(results, userid):
    user = User.query.filter_by(id=userid).first()
    detected_sounds = []
    new_sounds = []
    todays_new_sounds = []
    for species_data in results:
        add_relationship = False
        if species_data["confidence"]>0.15:
            detected_sounds.append(species_data["label"])
            species = Species.query.filter_by(name=species_data["label"]).first()
            if not species:
                add_relationship = True
                species = Species(
                    name = species_data["label"],
                    change_nickname_cycle = 0,
                    nickname = None,
                    user_id = user.id,
                    collection_status = species_data["label"].split("_")[0] in img_url.keys()
                )
                db.session.add(species)
                db.session.commit()
                new_sounds.append(species_data["label"])
                print(f"added new species: {species.name}")
            else:
                # check if user gathered, if not append to list
                relationship = UserSpecies.query.filter_by(user_id=userid, species_id=species.id).first()
                if not relationship:
                    add_relationship = True
                    new_sounds.append(species_data["label"])
                elif (
                    relationship.last_gathered_date.year!=(datetime.utcnow()).year
                    or relationship.last_gathered_date.month!=(datetime.utcnow()).month
                    or relationship.last_gathered_date.day!=(datetime.utcnow()).day
                    ) and (relationship.species.name.split("_")[0] not in new_sounds):
                    print(f"{species.name} originally was {relationship.last_gathered_date}")
                    todays_new_sounds.append(species_data["label"])
                    relationship.last_gathered_date = (datetime.utcnow())
                    db.session.commit()
                    print(f"updated gathered date for {species.name} to {relationship.last_gathered_date}")
        
            # update relationship
            if add_relationship:
                new_relationship = UserSpecies(
                    user_id = userid,
                    species_id = species.id,
                    relationship_type = 0,
                    last_gathered_date = datetime.utcnow()
                )
                new_relationship.species = species
                db.session.add(new_relationship)
                user.all_owned_species.append(new_relationship)
                db.session.commit()
                print(f"added new relationship for {user.username}")
                for relationships in user.all_owned_species:
                    print(relationships.species)
                    print(relationships.species.name)
                    print(relationships.relationship_type)
                    print("\n\n")

    return detected_sounds, todays_new_sounds, new_sounds

@api.route("/analyze", methods=["POST"])
@login_required
def analyze():
    if 'audio' not in request.files:
        return jsonify("No file part"), 400

    audio = request.files['audio']

    if audio.filename == '':
        return jsonify("No selected file"), 400
    
    lat = request.form.get("lat")
    lon = request.form.get("lon")

    if lat==None or lon==None:
        return jsonify("no geo location"), 400
    
    try:
        lat = float(lat)
        lon = float(lon)
        print(lat, lon)
    except Exception as e:
        print(e)
        print(lat, lon)
        return jsonify("process geo location error"), 400
  
    # Generate a unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    filename = f"{str(current_user.id)}_{timestamp}.mp3"
    if os.environ.get("ENVIRONMENT")=="vercel":
        save_path = f"/tmp/{filename}"
    else:
        save_path = f"tmp/{filename}"
    print(save_path)
    audio.save(save_path)
    results = request_api(save_path, lat, lon)
    if results.status_code!=200:
        print(results.content, results.status_code)
        return results.content, results.status_code
    
    os.remove(save_path)
    results = json.loads(results.content)
    print(results)
    if results["detections"]=="none":
        return jsonify("no detections")
    

    detected_sounds, todays_new_sounds, new_sounds = process_detections(results["detections"], current_user.id)
    previous_user_tokens = current_user.tokens
    current_user.tokens += len(todays_new_sounds)*3
    current_user.tokens += len(new_sounds)*5
    db.session.commit()

    print(f"user tokens: {previous_user_tokens} -> {current_user.tokens}")
    print(f"detected sounds: {detected_sounds}")
    print(f"todays new sounds: {todays_new_sounds}")
    print(f"new sounds: {new_sounds}")
    derived_data = {
        "detected sounds": detected_sounds,
        "today's new sounds": todays_new_sounds,
        "new sounds": new_sounds,
        "user tokens": f"{previous_user_tokens} -> {current_user.tokens}"
    }

    results["derived data"] = derived_data
    return results




