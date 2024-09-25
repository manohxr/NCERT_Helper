from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import ai_handler

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ncert_helper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'bot'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database tables
with app.app_context():
    db.create_all()

# User signup
@app.route('/sign-up', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully!"}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({"message": "Login successful!", "username": user.username}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

# Query ai
@app.route('/query', methods=['POST'])
def query_ai():
    data = request.get_json()
    user_query = data.get('query')
    username = data.get('username') 

    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Save the user's query to the database
    user_chat = Chat(username=username, message=user_query, role='user')
    db.session.add(user_chat)
    db.session.commit()

    # Handle the query using ai_handler
    ai_response = ai_handler.handle_query(user_query)

    # Save the AI's response to the database
    bot_chat = Chat(username=username, message=ai_response, role='bot')
    db.session.add(bot_chat)
    db.session.commit()

    return jsonify({'answer': ai_response})

@app.route('/chats/<string:username>', methods=['GET'])
def get_chats(username):
    chats = Chat.query.filter_by(username=username).all()
    chat_history = [{"role": chat.role, "message": chat.message, "timestamp": chat.timestamp} for chat in chats]
    return jsonify(chat_history), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)