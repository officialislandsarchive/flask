from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Simulated database for execution logs
execution_logs = {}

@app.route('/logExecution', methods=['POST'])
def log_execution():
    try:
        data = request.json
        user_id = data.get('userId')
        script_name = data.get('scriptName')

        if not user_id or not script_name:
            return jsonify({"status": "error", "message": "Missing userId or scriptName."})

        if user_id not in execution_logs:
            execution_logs[user_id] = {}

        user_data = execution_logs[user_id]
        if script_name in user_data:
            user_data[script_name].update(data)
            user_data[script_name]['executionCount'] = user_data[script_name].get('executionCount', 0) + 1
        else:
            user_data[script_name] = {**data, 'executionCount': 1}

        return jsonify({"status": "success", "message": "Data logged successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/logs', methods=['GET'])
def display_logs():
    # Pass execution logs to the template
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

        .script-info {
            margin-bottom: 20px;
            padding: 15px;
            background: #3d3d5a;
            border-left: 5px solid #6c63ff;
            border-radius: 5px;
        }

        .script-info p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h1>Execution Logs</h1>
        <input type="text" id="search" placeholder="Search User ID" onkeyup="filterUsers()">
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
            <h2>User ID: <span id="selectedUser"></span></h2>
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

        function populateUserList() {
            userList.innerHTML = '';
            for (const userId in executionLogs) {
                const li = document.createElement('li');
                li.textContent = userId;
                li.onclick = () => displayUserDetails(userId);
                userList.appendChild(li);
            }
        }

        function displayUserDetails(userId) {
            const userData = executionLogs[userId];
            selectedUser.textContent = userId;
            scriptDetails.innerHTML = '';
            for (const [scriptName, details] of Object.entries(userData)) {
                const scriptDiv = document.createElement('div');
                scriptDiv.className = 'script-info';
                scriptDiv.innerHTML = `
                    <p><strong>Script Name:</strong> ${scriptName}</p>
                    <p><strong>Execution Count:</strong> ${details.executionCount}</p>
                    <p><strong>Data:</strong> <pre>${JSON.stringify(details, null, 2)}</pre></p>
                `;
                scriptDetails.appendChild(scriptDiv);
            }
            welcome.style.display = 'none';
            userDetails.classList.add('active');
        }

        function filterUsers() {
            const searchValue = searchInput.value.toLowerCase();
            const users = userList.querySelectorAll('li');
            users.forEach(user => {
                if (user.textContent.toLowerCase().includes(searchValue)) {
                    user.style.display = '';
                } else {
                    user.style.display = 'none';
                }
            });
        }

        // Populate the user list on page load
        populateUserList();
    </script>
</body>
</html>
    """, execution_logs=execution_logs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
