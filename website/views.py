from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Profile
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        phone_country_code = request.form.get('phone_country_code')
        phone_number = request.form.get('phone_number')
        birthdate = request.form.get('birthdate')
        like_meeting = request.form.get('like_meeting')
        like_meeting_why = request.form.get('like_meeting_why')

        profile = Profile(email=email, first_name=first_name, last_name=last_name, 
                       phone_country_code=phone_country_code,
                       phone_number=phone_number,
                       birthdate=birthdate,
                       like_meeting=like_meeting,
                       like_meeting_why=like_meeting_why)
        db.session.add(profile)
        db.session.commit()
        flash('Profile Updated! You\'on your way to making some new connections! ', category='success')
        return redirect(url_for('views.home'))
    
    return render_template("profile.html", user=current_user)
