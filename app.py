from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from pymongo import MongoClient
from Models import get_question

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

# Check MongoDB connection status
# def check_mongo_connection():
#     try:
#         client = MongoClient('mongodb://localhost:27017/')
#         # Access a specific database (replace 'your_database_name' with your actual database name)
#         db = client.mini
#         names = db.list_collection_names()
#         print("Connected Succesfully", names)
#     except Exception as e:
#         print(f"Failed to connect to MongoDB: {str(e)}")

# check_mongo_connection()
# Function to send prompt to language model
def get_bot_response(prompt,Type):
    # Replace this URL with your language model server endpoint
    # model_endpoint = "http://localhost:5000"  # Example URL
    # response = requests.post(model_endpoint, json={"prompt": prompt})
    # if response.ok:
    #     return response.json().get("bot", "Error: No response from model")
    # else:
    return "Error: Failed to get response from model"

@app.route("/")
def login():
    return render_template('index.html')

@app.route('/request_question',methods=['POST'])
def request_question():
    prompt = request.json.get("prompt", "").strip()
    # Calculate the length of each part
    part_length = len(prompt) // 10

    # Slice the prompt into 10 parts
    prompt_parts = [prompt[i * part_length:(i + 1) * part_length] for i in range(10)]

    # If there's any remainder, add it to the last part
    if len(prompt) % 10 != 0:
        prompt_parts[-1] += prompt[-(len(prompt) % 10):]

    print(prompt_parts)

    answer = request.json.get("type", "").strip()

    if prompt == "":
        return jsonify({"error": "Empty prompt"}), 400
    res = {}
    for i in range(1, 11):  # Adjusted the range to include 10 parts
        part_start = (i - 1) * part_length
        part_end = i * part_length
        if i == 10:
            part_end = None  # For the last part, take the rest of the prompt
        res[i] = get_question(answer, prompt[part_start:part_end])

# Printing the results
    for key, value in res.items():
        print(f"Part {key}: {value}")



    print(res)
    return jsonify({"questions": res})

# @app.route('/signin')
# def signin():
#     return render_template('signin.html')

# @app.route('/sign_up', methods=['POST'])
# def signup():
#     data = {
#         'firstname': request.form.get('FirstName'),
#         'lastname': request.form.get('LastName'),
#         'email': request.form.get('Email'),
#         'username': request.form.get('Username'),
#         'password': request.form.get('Password')
#     }
#     print(data)

#     client = MongoClient('mongodb://localhost:27017/')
#     db = client.mini
#     collection = db.user
#     result = collection.insert_one(data)
#     print(f"Inserted document with ID: {result.inserted_id}")

#     flash('Sign up successful! Please log in.')
#     return redirect(url_for('signin'))

# @app.route('/login', methods=['POST'])
# async def login_user():
#     print("user login ")
#     username = request.form.get('Username')
#     password = request.form.get('Password')

#     client = MongoClient('mongodb://localhost:27017/')
#     db = client.mini
#     collection = db.user

#     user =  collection.find_one({'username': username, 'password': password})
#     print(user)
#     if user is not None:
#         # User found, redirect to a logged-in page or do further processing
#         return  render_template('index.html')
#     else:
#         # User not found or incorrect credentials, redirect back to sign-in page with error message
#         flash('Invalid username or password. Please try again.')
        # return  redirect(url_for('signin'))


if __name__ == "__main__":
    app.run(debug=True)