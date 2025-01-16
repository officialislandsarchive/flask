from flask import Flask, request, jsonify

app = Flask(__name__)

execution_logs = {}

@app.route('/logExecution', methods=['POST'])
def log_execution():
    try:
        data = request.json
        user_id = data.get('userId')
        script_name = data.get('scriptName')

        if user_id in execution_logs:
            user_data = execution_logs[user_id]
            if script_name in user_data:
                user_data[script_name].update(data)
                user_data[script_name]['executionCount'] += 1
            else:
                user_data[script_name] = {**data, 'executionCount': 1}
        else:
            execution_logs[user_id] = {
                script_name: {**data, 'executionCount': 1}
            }

        return jsonify({"status": "success", "message": "Data logged successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/logs', methods=['GET'])
def display_logs():
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Execution Logs</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background: #121212;
            color: #e0e0e0;
            display: flex;
            height: 100vh;
        }}

        .sidebar {{
            width: 300px;
            background: #1c1c1c;
            padding: 20px;
            overflow-y: auto;
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);
        }}

        .sidebar h1 {{
            color: #bb86fc;
            text-align: center;
            font-size: 2em;
            margin-bottom: 20px;
        }}

        .search-bar {{
            margin-bottom: 20px;
            display: flex;
        }}

        .search-bar input {{
            flex: 1;
            padding: 10px;
            font-size: 1em;
            border: 1px solid #333;
            border-radius: 5px;
            background: #2c2c2c;
            color: #e0e0e0;
        }}

        .search-bar button {{
            padding: 10px;
            background: #bb86fc;
            border: none;
            color: #fff;
            font-size: 1em;
            cursor: pointer;
            border-radius: 5px;
            margin-left: 10px;
        }}

        .user-list {{
            list-style: none;
            padding: 0;
        }}

        .user-list li {{
            padding: 10px;
            margin-bottom: 10px;
            background: #2c2c2c;
            border-radius: 5px;
            cursor: pointer;
            color: #bb86fc;
            transition: background 0.3s ease;
        }}

        .user-list li:hover {{
            background: #383838;
        }}

        .content {{
            flex: 1;
            padding: 20px;
            background: #181818;
            overflow-y: auto;
        }}

        .user-info {{
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }}

        .user-info h2 {{
            color: #bb86fc;
            font-size: 1.5em;
            margin-bottom: 10px;
        }}

        .user-info .script-info {{
            background: #2c2c2c;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border-left: 4px solid #bb86fc;
        }}

        .user-info .script-info p {{
            margin: 5px 0;
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <h1>Users</h1>
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="Search by User ID" oninput="filterUsers()            <button onclick="filterUsers()">Search</button>
        </div>
        <ul class="user-list" id="userList">
            <!-- User list dynamically populated -->
        </ul>
    </div>

    <div class="content">
        <div id="defaultView">
            <h1>Welcome to the Execution Logs</h1>
            <p>Select a user from the left sidebar to view their details.</p>
        </div>
        <div id="userDetails" class="user-info">
            <h2>User ID: <span id="userId"></span></h2>
            <div id="userScripts">
                <!-- User scripts dynamically populated -->
            </div>
        </div>
    </div>

    <script>
        async function fetchExecutionLogs() {
            const response = await fetch('/logs');
            return await response.json();
        }

        let executionLogs = {};

        async function populateUser List() {
            executionLogs = await fetchExecutionLogs();
            const userListElement = document.getElementById('userList');
            userListElement.innerHTML = '';

            Object.keys(executionLogs).forEach(userId => {
                const listItem = document.createElement('li');
                listItem.textContent = userId;
                listItem.onclick = () => displayUser Details(userId);
                userListElement.appendChild(listItem);
            });
        }

        function displayUser Details(userId) {
            const userData = executionLogs[userId];
            if (!userData) return;

            const userIdElement = document.getElementById('userId');
            const userScriptsElement = document.getElementById('userScripts');
            const defaultViewElement = document.getElementById('defaultView');
            const userDetailsElement = document.getElementById('userDetails');

            userIdElement.textContent = userId;
            userScriptsElement.innerHTML = '';

            Object.entries(userData).forEach(([scriptName, log]) => {
                const scriptDiv = document.createElement('div');
                scriptDiv.className = 'script-info';
                scriptDiv.innerHTML = `
                    <p><strong>Script Name:</strong> ${scriptName}</p>
                    <p><strong>Execution Count:</strong> ${log.executionCount}</p>
                    <p><strong>Experience:</strong> <pre>${JSON.stringify(log.experience, null, 2)}</pre></p>
                    <p><strong>Experience HUD Increment:</strong> <pre>${JSON.stringify(log.experienceHudIncrement, null, 2)}</pre></p>
                    <p><strong>Gamepasses:</strong> <pre>${JSON.stringify(log.gamepasses, null, 2)}</pre></p>
                    <p><strong>Mob Kills:</strong> <pre>${JSON.stringify(log.mobKills, null, 2)}</pre></p>
                    <p><strong>Settings:</strong> <pre>${JSON.stringify(log.settings, null, 2)}</pre></p>
                    <p><strong>Shop State:</strong> <pre>${JSON.stringify(log.shopState, null, 2)}</pre></p>
                    <p><strong>Backpack Items:</strong> <pre>${JSON.stringify(log.backpack, null, 2)}</pre></p>
                    <p><strong>Island Data:</strong> <pre>${JSON.stringify(log.islandData, null, 2)}</pre></p>
                `;
                userScriptsElement.appendChild(scriptDiv);
            });

            defaultViewElement.style.display = 'none';
            userDetailsElement.style.display = 'block';
        }

        function filterUsers() {
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const users = document.querySelectorAll('.user-list li');
            users.forEach(user => {
                user.style.display = user.textContent.toLowerCase().includes(searchInput) ? '' : 'none';
            });
        }

        // Populate user list on page load
        window.onload = populateUser List;
    </script>
</body>
</html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
