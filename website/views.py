from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/add-note', methods=['POST'])
@login_required
def add_note():
    note = request.form.get('note')
    mood = request.form.get('mood')

    if len(note) < 1:
        flash('Note is too short!', category='error')
    else:
        new_note = Note(data=note, mood=mood, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')

    return redirect(url_for('views.home'))

@views.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted!', category='success')
    return redirect(url_for('views.home'))

@views.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get(note_id)
    if request.method == 'POST':
        new_note = request.form.get('note')
        mood = request.form.get('mood')

        if note and note.user_id == current_user.id:
            if len(new_note) < 1:
                flash('Note is too short!', category='error')
            else:
                note.data = new_note
                note.mood = mood
                db.session.commit()
                flash('Note updated!', category='success')
                return redirect(url_for('views.home'))

    return render_template('edit_note.html', note=note)
