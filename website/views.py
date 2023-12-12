from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from urllib.parse import unquote

from .models import User, Species, UserSpecies
from .img_url import img_url

views = Blueprint("views", __name__)

@views.route("/about")
def about():
    return render_template("about.html", user=current_user)

@views.route("/developer")
def developer():
    return render_template("developer.html", user=current_user)

@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/profile/<uuid>")
@login_required
def profile(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if not user:
        flash("User profile not found.")
        return redirect(url_for("views.home"))
    else:
        return render_template("profile.html", user=User.query.filter_by(uuid=uuid).first(), img_url=img_url)
    
@views.route("/species_detail/<name>")
@login_required
def species_detail(name):
    name = unquote(name)
    species = Species.query.filter_by(name=name).first()
    if not species:

        flash("Species not found.")
        return redirect(url_for("views.home"))
    else:
        return render_template("species.html", species=species, user=current_user, UserSpecies=UserSpecies, img_url=img_url)
        
