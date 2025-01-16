from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)
data_file = "execution_data.json"

# Load data from file if it exists
if os.path.exists(data_file):
    with open(data_file, "r") as file:
        execution_counts = json.load(file)
else:
    execution_counts = {}

@app.route('/')
def home():
    return render_template_string('''
        <html>
        <head><title>Script Execution Counts</title></head>
        <body>
            <h1>Script Execution Counts</h1>
            <table border="1">
                <tr>
                    <th>User ID</th>
                    <th>Username</th>
                    <th>Script Name</th>
                    <th>Execution Count</th>
                </tr>
                {% for user_id, user_data in execution_counts.items() %}
                    {% for script_name, count in user_data["scripts"].items() %}
                    <tr>
                        <td>{{ user_id }}</td>
                        <td>{{ user_data["username"] }}</td>
                        <td>{{ script_name }}</td>
                        <td>{{ count }}</td>
                    </tr>
                    {% endfor %}
                {% endfor %}
            </table>
        </body>
        </html>
    ''', execution_counts=execution_counts)

@app.route('/logExecution', methods=['POST'])
def log_execution():
    data = request.json
    user_id = str(data.get('userId'))
    username = data.get('username')
    script_name = data.get('scriptName')

    if not user_id or not username or not script_name:
        return jsonify({'error': 'userId, username, and scriptName are required'}), 400

    if user_id not in execution_counts:
        execution_counts[user_id] = {"username": username, "scripts": {}}

    user_data = execution_counts[user_id]
    user_data["username"] = username
    user_data["scripts"][script_name] = user_data["scripts"].get(script_name, 0) + 1

    with open(data_file, "w") as file:
        json.dump(execution_counts, file)

    return jsonify({
        'message': f'Execution logged for {script_name} by {username}',
        'totalExecutions': user_data["scripts"][script_name]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
