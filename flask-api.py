from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from sql import run_query


# Load environment variables
load_dotenv()

app = Flask(__name__)

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
  result = run_query(query,[data['subject'], data['homework'], data['due'], data['notes']])
  # Return ID to confirm it was created
  return jsonify({"id": result[0]['id']}), 201

# Index Route (Get all assignments)
@app.route('/assignments', methods=['GET'])
def get_assignments():
  # Query String
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

if __name__ == "__main__":
  app.run(debug=True, port=3000)
# Adding comment to make sure I can push to github