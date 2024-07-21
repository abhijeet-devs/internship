from flask import Flask, redirect, request, render_template_string
import string
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

# Create all database tables (if not exist)
with app.app_context():
    db.create_all()

# Home page with form to submit URLs
@app.route('/')
def index():
    return render_template_string('''
        <form method="POST" action="/shorten">
            <label for="url">Enter URL:</label><br>
            <input type="text" id="url" name="url" style="width: 300px;"><br><br>
            <input type="submit" value="Shorten">
        </form>
    ''')

# URL shortening endpoint
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    short_code = generate_short_code()

    with app.app_context():
        new_url = URL(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()

    short_url = request.host_url + short_code
    return f'Shortened URL: <a href="{short_url}">{short_url}</a>'

# Redirect short URLs to original long URLs
@app.route('/<short_code>')
def redirect_to_url(short_code):
    with app.app_context():
        url_entry = URL.query.filter_by(short_code=short_code).first()
        if url_entry:
            return redirect(url_entry.long_url)
        else:
            return 'Invalid short URL'

# Helper function to generate a random short code
def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for i in range(6))
    return short_code

if __name__ == '__main__':
    app.run(debug=True)
