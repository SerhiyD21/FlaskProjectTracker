from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.sport_club

# Collections
projects = db.projects
tasks = db.tasks
users = db.users

@app.route('/')
def index():
    return render_template('index.html')

# Projects CRUD
@app.route('/projects')
def list_projects():
    all_projects = list(projects.find())
    return render_template('projects/list.html', projects=all_projects)

@app.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project = {
            'name': request.form['name'],
            'description': request.form['description'],
            'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            'end_date': datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        }
        projects.insert_one(project)
        return redirect(url_for('list_projects'))
    return render_template('projects/add.html')

@app.route('/projects/edit/<id>', methods=['GET', 'POST'])
def edit_project(id):
    if request.method == 'POST':
        projects.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': request.form['name'],
                'description': request.form['description'],
                'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
                'end_date': datetime.strptime(request.form['end_date'], '%Y-%m-%d')
            }}
        )
        return redirect(url_for('list_projects'))
    project = projects.find_one({'_id': ObjectId(id)})
    return render_template('projects/edit.html', project=project)

@app.route('/projects/delete/<id>')
def delete_project(id):
    projects.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('list_projects'))

# Tasks CRUD
@app.route('/tasks')
def list_tasks():
    all_tasks = list(tasks.find())
    
    # Додаємо імена користувачів до задач
    for task in all_tasks:
        user = users.find_one({'_id': task['assignee_id']})
        task['assignee_name'] = user['name'] if user else 'Не призначено'
    
    return render_template('tasks/list.html', tasks=all_tasks)

@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task = {
            'name': request.form['name'],
            'description': request.form['description'],
            'status': request.form['status'],
            'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            'deadline': datetime.strptime(request.form['deadline'], '%Y-%m-%d'),
            'priority': request.form['priority'],
            'assignee_id': ObjectId(request.form['assignee_id']),
            'project_id': ObjectId(request.form['project_id'])
        }
        tasks.insert_one(task)
        return redirect(url_for('list_tasks'))
    
    all_users = list(users.find())
    all_projects = list(projects.find())
    return render_template('tasks/add.html', users=all_users, projects=all_projects)

@app.route('/tasks/edit/<id>', methods=['GET', 'POST'])
def edit_task(id):
    if request.method == 'POST':
        tasks.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': request.form['name'],
                'description': request.form['description'],
                'status': request.form['status'],
                'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
                'deadline': datetime.strptime(request.form['deadline'], '%Y-%m-%d'),
                'priority': request.form['priority'],
                'assignee_id': ObjectId(request.form['assignee_id']),
                'project_id': ObjectId(request.form['project_id'])
            }}
        )
        return redirect(url_for('list_tasks'))
    
    task = tasks.find_one({'_id': ObjectId(id)})
    all_users = list(users.find())
    all_projects = list(projects.find())
    return render_template('tasks/edit.html', task=task, users=all_users, projects=all_projects)

@app.route('/tasks/delete/<id>')
def delete_task(id):
    tasks.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('list_tasks'))

# Users CRUD
@app.route('/users')
def list_users():
    all_users = list(users.find())
    return render_template('users/list.html', users=all_users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user = {
            'name': request.form['name'],
            'email': request.form['email'],
            'role': request.form['role']
        }
        users.insert_one(user)
        return redirect(url_for('list_users'))
    return render_template('users/add.html')

@app.route('/users/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        users.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': request.form['name'],
                'email': request.form['email'],
                'role': request.form['role']
            }}
        )
        return redirect(url_for('list_users'))
    user = users.find_one({'_id': ObjectId(id)})
    return render_template('users/edit.html', user=user)

@app.route('/users/delete/<id>')
def delete_user(id):
    users.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    app.run(debug=True)
