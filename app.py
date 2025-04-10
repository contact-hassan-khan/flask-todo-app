from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Path to the JSON file
DATA_FILE = 'data/data.json'

# Function to load data from JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": []}
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Function to save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# MongoDB Atlas connection string
MONGO_URI = 'mongodb+srv://mydatabase:khan02@cluster0.mongodb.net/todoDB?retryWrites=true&w=majority'
client = MongoClient(MONGO_URI)
db = mydatabase
tasks_collection = mycollection


@app.route('/')
def index():
    # Load tasks from JSON file
    data = load_data()
    return render_template('index.html', tasks=data['tasks'])

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_description = request.form['task_description']
    
    # Load existing data
    data = load_data()
    
    # Find the next ID
    next_id = 1
    if data['tasks']:
        next_id = max(task['id'] for task in data['tasks']) + 1
    
    # Add new task
    new_task = {
        'id': next_id,
        'name': task_name,
        'description': task_description
    }
    data['tasks'].append(new_task)
    
    # Save updated data
    save_data(data)
    
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    # Load existing data
    data = load_data()
    
    # Remove the task with the given ID
    data['tasks'] = [task for task in data['tasks'] if task['id'] != task_id]
    
    # Save updated data
    save_data(data)
    
    return redirect(url_for('index'))

@app.route('/api/tasks')
def api_tasks():
    # Load tasks from JSON file
    data = load_data()
    return jsonify(data['tasks'])

if __name__ == '__main__':
    app.run(debug=True)