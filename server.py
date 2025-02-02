import os
import json
import base64
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

execution_logs = {}

@app.route('/logExecution', methods=['POST'])
def log_execution():
    try:
        data = request.json
        user_id = data.get('userId')
        username = data.get('username')
        script_name = data.get('scriptName')

        if not user_id or not username or not script_name:
            return jsonify({"status": "error", "message": "Missing userId, username, or scriptName."})

        if user_id not in execution_logs:
            execution_logs[user_id] = {'username': username, 'scripts': {}}

        user_data = execution_logs[user_id]['scripts']
        if script_name in user_data:
            user_data[script_name].update(data)
            user_data[script_name]['executionCount'] = user_data[script_name].get('executionCount', 0) + 1
        else:
            user_data[script_name] = {**data, 'executionCount': 1}

        return jsonify({"status": "success", "message": "Data logged successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/3284y23908h2893hd09823hd83jd923j09d8j238903djh2389dj8233298dh987', methods=['GET'])
def display_logs():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Execution Logs</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: #1e1e2f;
            color: #ffffff;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        .sidebar {
            width: 300px;
            background: #2b2b3d;
            padding: 20px;
            overflow-y: auto;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.5);
        }

        .sidebar h1 {
            color: #6c63ff;
            text-align: center;
            font-size: 1.8em;
            margin-bottom: 20px;
        }

        .sidebar input {
            width: calc(100% - 10px);
            padding: 10px;
            border: 2px solid #6c63ff;
            border-radius: 5px;
            background: #1e1e2f;
            color: #ffffff;
            margin-bottom: 20px;
        }

        .sidebar ul {
            list-style: none;
            padding: 0;
        }

        .sidebar ul li {
            padding: 15px;
            margin-bottom: 10px;
            background: #3d3d5a;
            border-radius: 5px;
            color: #6c63ff;
            cursor: pointer;
            transition: background 0.3s;
        }

        .sidebar ul li:hover {
            background: #4b4b6e;
        }

        .content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }

        .user-details {
            display: none;
        }

        .user-details.active {
            display: block;
        }

        .user-details h2 {
            color: #6c63ff;
            margin-bottom: 20px;
        }

        .script-section {
            margin-bottom: 20px;
        }

        .script-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            padding: 10px 15px;
            background: #3d3d5a;
            border-radius: 5px;
            transition: background 0.3s;
        }

        .script-header:hover {
            background: #4b4b6e;
        }

        .script-header h3 {
            margin: 0;
            color: #6c63ff;
        }

        .script-header span {
            font-size: 0.9em;
            color: #bbb;
        }

        .script-details {
            display: none;
            padding: 15px;
            background: #2b2b3d;
            border-radius: 5px;
            margin-top: 10px;
        }

        .script-details p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h1>Execution Logs</h1>
        <input type="text" id="search" placeholder="Search by User ID or Username" onkeyup="filterUsers()">
        <ul id="userList">
            <!-- Users will be populated dynamically -->
        </ul>
    </div>
    <div class="content">
        <div id="welcome">
            <h1>Welcome to Execution Logs</h1>
            <p>Select a user from the sidebar to view their details.</p>
        </div>
        <div id="userDetails" class="user-details">
            <h2>Username: <span id="selectedUsername"></span></h2>
            <h3>User ID: <span id="selectedUser"></span></h3>
            <div id="scriptDetails">
                <!-- Script details will be populated dynamically -->
            </div>
        </div>
    </div>
    <script>
        const executionLogs = {{ execution_logs | tojson }};
        const userList = document.getElementById('userList');
        const searchInput = document.getElementById('search');
        const userDetails = document.getElementById('userDetails');
        const scriptDetails = document.getElementById('scriptDetails');
        const welcome = document.getElementById('welcome');
        const selectedUser = document.getElementById('selectedUser');
        const selectedUsername = document.getElementById('selectedUsername');

        function populateUserList() {
            userList.innerHTML = '';
            for (const [userId, userData] of Object.entries(executionLogs)) {
                const li = document.createElement('li');
                li.textContent = `${userData.username} (${userId})`;
                li.onclick = () => displayUserDetails(userId);
                userList.appendChild(li);
            }
        }

        function displayUserDetails(userId) {
            const userData = executionLogs[userId];
            selectedUser.textContent = userId;
            selectedUsername.textContent = userData.username;
            scriptDetails.innerHTML = '';
            const scripts = Object.entries(userData.scripts).sort((a, b) => 
                b[1].executionCount - a[1].executionCount || a[0].localeCompare(b[0])
            );

            for (const [scriptName, details] of scripts) {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'script-section';

                const header = document.createElement('div');
                header.className = 'script-header';
                header.innerHTML = `
                    <h3>${scriptName}</h3>
                    <span>${details.executionCount} executions</span>
                `;
                header.onclick = () => {
                    const detailsDiv = sectionDiv.querySelector('.script-details');
                    detailsDiv.style.display = detailsDiv.style.display === 'none' ? 'block' : 'none';
                };

                const detailsDiv = document.createElement('div');
                detailsDiv.className = 'script-details';
                detailsDiv.innerHTML = `
                    <p><strong>Data:</strong> <pre>${JSON.stringify(details, null, 2)}</pre></p>
                `;

                sectionDiv.appendChild(header);
                sectionDiv.appendChild(detailsDiv);
                scriptDetails.appendChild(sectionDiv);
            }

            welcome.style.display = 'none';
            userDetails.classList.add('active');
        }

        function filterUsers() {
            const searchValue = searchInput.value.toLowerCase();
            const users = userList.querySelectorAll('li');
            users.forEach(user => {
                const userText = user.textContent.toLowerCase();
                if (userText.includes(searchValue)) {
                    user.style.display = '';
                } else {
                    user.style.display = 'none';
                }
            });
        }

        populateUserList();
    </script>
</body>
</html>
    """, execution_logs=execution_logs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
