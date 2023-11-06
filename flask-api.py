# This is the main page of the backend server which serves as the API (Application Programming Interface) for the full-stack application 'Assignments'. The purpose of this page is to create an application which can handle requests from the front-end once the two sides are connected.

# Import dependencies (pieces of software that this .py file needs in order to do what it's supposed to)
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from sql import run_query
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Define app variable to initialize the app; used to configure and definte routes
app = Flask(__name__)

# Initialize CORS (Cross Origin Resource Sharing)
CORS(app)

# Run this at the start to ensure the table exists
def create_table():
  create_table_query = """
  CREATE TABLE IF NOT EXISTS assignments (
  id SERIAL PRIMARY KEY,
  subject VARCHAR NOT NULL,
  homework VARCHAR NOT NULL,
  due VARCHAR NOT NULL,
  notes VARCHAR NOT NULL
  );
  """
  run_query(create_table_query)

create_table()

#CREATE ROUTE (Create an assignment)
@app.route('/assignments', methods=['POST'])
def add_assignment():
  data = request.get_json()
  # SQL query
  query = "INSERT INTO assignments (subject, homework, due, notes) VALUES (%s, %s, %s, %s) RETURNING id;"
  # Run query and get back results
  result = run_query(query,[data['subject'], data['homework'], data['due'], data['notes']])
  # Return ID to confirm it was created
  return jsonify({"id": result[0]['id']}), 201

# Index Route (Get all assignments)
@app.route('/assignments', methods=['GET'])
def get_assignments():
  # SQL query
  query = "SELECT * FROM assignments;"
  # Run query and get back results
  results = run_query(query)
  # Turn results into an array of dictionaries (id, subject, homework, due, notes)
  results = [{'id': result['id'], 'subject': result['subject'], 'homework': result['homework'], 'due': result['due'], 'notes': result['notes']} for result in results]
  # Return results as json
  return jsonify(results), 200

# Show Route (Display one assignment)
@app.route('/assignments/<int:assignments_id>', methods=['GET'])
def get_assignment(assignments_id):
  query = "SELECT * FROM assignments WHERE id = %s;"
  result = run_query(query, [assignments_id])
  if not result:
    return jsonify({"error": "Assignments not found"}), 404
  result = [{'id': result[0]['id'], 'subject': result[0]['subject'], 'homework': result[0]['homework'], 'due': result[0]['due'], 'notes': result[0]['notes']}]
  return jsonify(result)

# Update Route
@app.route('/assignments/<int:assignments_id>', methods=['PUT'])
def update_assignment(assignments_id):
  data = request.get_json()
  query = "UPDATE assignments SET subject = %s, homework = %s, due = %s, notes = %s WHERE id = %s;"
  run_query(query, [data['subject'], data['homework'], data['due'], data['notes'], assignments_id])
  return jsonify({"message": "Assignment updated succesfully"})

# Delete Route
@app.route('/assignments/<int:assignments_id>', methods=['DELETE'])
def delete_assignment(assignments_id):
  query = "DELETE FROM assignments WHERE id = %s;"
  run_query(query, [assignments_id])
  return jsonify({"message": "Assignment deleted succesfully"})

# Script to start Flask application and host it on port 3000 with debug mode enabled  (for more detailed error messages and automatic reloading)
if __name__ == "__main__":
  app.run(debug=True, port=3000)