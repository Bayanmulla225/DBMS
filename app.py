from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["course_management"]
instructors_collection = db["instructors"]

@app.route('/')
def index():
    departments = ["Computer Science", "Electrical", "Automobile", "Data Science", "AIML", "Mechanical"]
    courses = ["ADA", "MC", "DBMS", "DMS", "Biology", "UHVC", "UI/UX"]
    instructors = instructors_collection.find()
    return render_template("add_instructor.html", departments=departments, courses=courses, instructors=instructors)

@app.route('/add_instructor', methods=['POST'])
def add_instructor():
    data = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "phone": request.form.get('phone'),
        "department": request.form.get('department'),
        "course": request.form.get('course')
    }
    if all(data.values()):
        instructors_collection.insert_one(data)
    return redirect(url_for('index'))

@app.route('/delete_instructor/<id>', methods=['POST'])
def delete_instructor(id):
    instructors_collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True)

    
