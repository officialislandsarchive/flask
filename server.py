from flask import Flask, request, jsonify

app = Flask(__name__)

execution_logs = {}

@app.route('/logExecution', methods=['POST'])
def log_execution():
    try:
        data = request.json
        user_id = data.get('userId')

        # If user already exists, we update their logs
        if user_id in execution_logs:
            user_data = execution_logs[user_id]

            # Check if the script type has been executed before and update accordingly
            script_name = data.get('scriptName')
            if script_name in user_data:
                # If data exists and has changed, update it
                if user_data[script_name] != data:
                    user_data[script_name] = data
            else:
                # If the script name is new, add it
                user_data[script_name] = data
            
            # Increment execution count for that script
            user_data[script_name]['executionCount'] = user_data[script_name].get('executionCount', 0) + 1

        else:
            # New user, add them to the logs
            execution_logs[user_id] = {
                data.get('scriptName'): {
                    **data,
                    'executionCount': 1  # Set the initial execution count to 1
                }
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
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                text-align: center;
            }}
            .log {{
                border-bottom: 1px solid #ddd;
                padding: 10px 0;
            }}
            .log:last-child {{
                border-bottom: none;
            }}
            .log pre {{
                background: #eee;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
                white-space: pre-wrap;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Execution Logs</h1>
            {generate_logs_html()}
        </div>
    </body>
    </html>
    """
    return html_content


def generate_logs_html():
    """Generates the HTML for execution logs dynamically."""
    if not execution_logs:
        return "<p>No logs available.</p>"
    
    log_entries = ""
    for user_id, user_data in execution_logs.items():
        log_entries += f"""
        <div class="log">
            <h2>User ID: {user_id}</h2>
        """
        for script_name, log in user_data.items():
            log_entries += f"""
            <div class="log">
                <strong>Script Name:</strong> {script_name} <br>
                <strong>Execution Count:</strong> {log['executionCount']} <br>
                <strong>Experience:</strong> <pre>{log.get('experience', {})}</pre>
                <strong>Experience HUD Increment:</strong> <pre>{log.get('experienceHudIncrement', {})}</pre>
                <strong>Gamepasses:</strong> <pre>{log.get('gamepasses', {})}</pre>
                <strong>Mob Kills:</strong> <pre>{log.get('mobKills', {})}</pre>
                <strong>Settings:</strong> <pre>{log.get('settings', {})}</pre>
                <strong>Shop State:</strong> <pre>{log.get('shopState', {})}</pre>
                <strong>Backpack Items:</strong> <pre>{log.get('backpack', {})}</pre>
                <strong>Island Data:</strong> <pre>{log.get('islandData', {})}</pre>
            </div>
            """
        log_entries += "</div>"

    return log_entries


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
