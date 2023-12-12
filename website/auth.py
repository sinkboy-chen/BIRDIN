from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired

from . import db
from .models import User, UnverifiedUser
from .email import *

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.")
        else:
            unverified_user = UnverifiedUser.query.filter_by(email=email).first()
            if unverified_user:
                flash("Your email is unverified. Please check your inbox and spam folder for the verification email, or sign up again.")
            else:
                flash("Email does not exist.")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        show_student_id = request.form.get("show_student_id")!=None

        user = User.query.filter_by(email=email).all()
        
        if user:
            flash("Email already exists.")
        elif password1 != password2:
            flash("Passwords don\"t match.")
        elif len(password1) < 4:
            flash("Password must be at least 4 characters.")
        elif len(username) < 2:
            flash("Username must be at least 2 characters.")
        elif not is_valid_email(email):
            flash("Email address must be from the domain 'ntu.edu.tw'.")
        else:
            UnverifiedUser.query.filter_by(email=email).delete()
            new_user = UnverifiedUser(
                email=email,
                username=username,
                password=generate_password_hash(password1, method="scrypt"),
                show_student_id=show_student_id,
            )
            db.session.add(new_user)
            db.session.commit()
            send_verification_email(email)

            print(len(UnverifiedUser.query.all()))
            for user in UnverifiedUser.query.all():
                print(f"{user.username} {user.email} {user.id}")

            return redirect(url_for("auth.email_sent"))

    return render_template("sign_up.html", user=current_user)

@auth.route("/email_sent")
def email_sent():
    return render_template("email_sent.html", user=current_user)

@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = current_app.mail_verify_serializer.loads(token, salt='email_verify_salt', max_age=600)
        if len(UnverifiedUser.query.filter_by(email=email).all())==1:
            data = UnverifiedUser.query.filter_by(email=email).first()
            new_user = User(
                email = data.email,
                username = data.username,
                password = data.password,
                show_student_id = data.show_student_id,
                tokens = 0,
            )
            db.session.add(new_user)
            UnverifiedUser.query.filter_by(email=email).delete()
            db.session.commit()
        else:
            if len(User.query.filter_by(email=email).all())==1:
                flash("The user has already been verified. Please login.")
                return redirect(url_for("auth.login"))
            flash("Something went wrong. Please sign up again.")
            return redirect(url_for("auth.signup"))
        flash("The token works! Please login.")
        return redirect(url_for("auth.login"))
    
    except Exception as e:
        print(e)
        flash("Token expired or something went wrong. Please sign up again.")
        return redirect(url_for("auth.signup"))