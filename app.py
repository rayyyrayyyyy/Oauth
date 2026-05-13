from flask import Flask, redirect, url_for, session, jsonify, render_template_string
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)

# Change this for your lab only
app.secret_key = "SECRET_KEY_FOR_LAB"

oauth = OAuth(app)

github = oauth.register(
    name='github',
    client_id='Ov23liU04TZb9vF9isjM',
    client_secret='YOUR_CLIENT_SECRET_HERE',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/')
def home():
    return render_template_string("""
    <h1>GitHub OAuth Login</h1>
    <p>This is the login page before authentication.</p>
    <a href="/login">
        <button>Login with GitHub</button>
    </a>
    """)

@app.route('/login')
def login():
    return github.authorize_redirect(url_for('callback', _external=True))

@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    user = github.get('user').json()

    session['user'] = user
    return redirect('/profile')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized. Please login first.", 401

    user = session['user']

    return jsonify({
        "message": "Login successful",
        "username": user.get("login"),
        "name": user.get("name"),
        "github_id": user.get("id"),
        "profile_url": user.get("html_url"),
        "avatar_url": user.get("avatar_url")
    })

@app.route('/api/secure-data')
def secure_data():
    if 'user' not in session:
        return jsonify({
            "error": "Unauthorized access. Please login first."
        }), 401

    return jsonify({
        "message": "This is protected secure data.",
        "status": "Access granted",
        "user": session['user'].get("login")
    })

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template_string("""
    <h1>Logged Out</h1>
    <p>You have successfully logged out.</p>
    <a href="/profile">Try accessing profile again</a>
    """)

if __name__ == '__main__':
    app.run(debug=True)