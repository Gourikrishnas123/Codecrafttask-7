

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS

def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tasks table if not exists
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    with get_db_connection() as conn:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
        return jsonify([
            {
                'id': task['id'],
                'text': task['title'],  # ✅ match with frontend 'text'
                'completed': bool(task['completed'])
            } for task in tasks
        ])

# Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Task text is required'}), 400

    with get_db_connection() as conn:
        conn.execute('INSERT INTO tasks (title, completed) VALUES (?, ?)', (text, False))
        conn.commit()
    return jsonify({'message': 'Task added'}), 201

# Update task status
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.get_json()
    completed = data.get('completed')

    with get_db_connection() as conn:
        cur = conn.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed, task_id))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task updated'})

# Delete task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with get_db_connection() as conn:
        cur = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    print("✅ Flask server running at http://127.0.0.1:5000")
    app.run(debug=True)