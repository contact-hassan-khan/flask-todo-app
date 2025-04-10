from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas connection string
MONGO_URI = 'mongodb+srv://mydatabase:khan02@cluster0.mongodb.net/todoDB?retryWrites=true&w=majority'
client = MongoClient(MONGO_URI)
db = mydatabase
tasks_collection = mycollection


@app.route('/')
def index():
    tasks = tasks_collection.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_description = request.form['task_description']
    tasks_collection.insert_one({
        'name': task_name,
        'description': task_description
    })
    return redirect(url_for('index'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)