from flask import Flask, jsonify, abort, request
from enum import Enum

app = Flask(__name__)

class TaskStatus(Enum):
    INCOMPLETE = "Incomplete"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

tasks = []
task_id = 1

def find_task_by_id(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id
    if not request.json or 'title' not in request.json:
        abort(400)
    title = request.json['title']
    description = request.json.get('description', '')
    due_date = request.json.get('due_date', '')
    status = TaskStatus.INCOMPLETE.value
    task = {'id': task_id, 
            'title': title, 
            'description': description,
            'due_date': due_date,
            'status': status
            }
    tasks.append(task)
    task_id += 1
    return jsonify({'task': task}), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task_by_id(task_id)
    if task is None:
        abort(404)
    return jsonify({'task': task})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task_by_id(task_id)
    if task is None:
        abort(404)

    if not request.json:
        abort(400)

    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'description' in request.json:
        task['description'] = request.json['description']
    if 'due_date' in request.json:
        task['due_date'] = request.json['due_date']
    if 'status' in request.json:
        status = request.json['status']
        if status not in [s.value for s in TaskStatus]:
            abort(400)
        task['status'] = status

    return jsonify({'task': task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task_by_id(task_id)
    if task is None:
        abort(404)
    tasks.remove(task)
    return jsonify({'result': True})

@app.route('/tasks', methods=['GET'])
def list_tasks():
    per_page = int(request.args.get('per_page', 2))
    page = int(request.args.get('page', 1))
    
    total_tasks = len(tasks)
    total_pages = (total_tasks + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_tasks = tasks[start:end]
    
    return jsonify({
        'tasks': paginated_tasks,
        'total_tasks': total_tasks,
        'total_pages': total_pages,
        'current_page': page
    })

if __name__ == '__main__':
    app.run(debug=True)


