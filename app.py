# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database Configuration - will use environment variables
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'postgres')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '5432')
db_name = os.environ.get('DB_NAME', 'postgres')

# You can also use DATABASE_URL directly if provided
database_url = os.environ.get('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Simple Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.id}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note_content = request.form['content']
        new_note = Note(content=note_content)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'There was an issue adding your note: {e}'

    else:
        notes = Note.query.order_by(Note.date_created.desc()).all()
        return render_template('index.html', notes=notes)

@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Note.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that note'

@app.route('/db-info')
def db_info():
    """Display database connection information"""
    info = {
        'DB_USER': os.environ.get('DB_USER', 'Not set'),
        'DB_HOST': os.environ.get('DB_HOST', 'Not set'),
        'DB_PORT': os.environ.get('DB_PORT', 'Not set'),
        'DB_NAME': os.environ.get('DB_NAME', 'Not set'),
        'DATABASE_URL': os.environ.get('DATABASE_URL', 'Not set'),
        'Connection': app.config['SQLALCHEMY_DATABASE_URI']
    }
    return info

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)