from flask import Flask, request, jsonify

app = Flask(__name__)

execution_logs = {}

@app.route('/logExecution', methods=['POST'])
def log_execution():
    try:
        data = request.json
        user_id = data.get('userId')

        if user_id in execution_logs:
            user_data = execution_logs[user_id]
            script_name = data.get('scriptName')
            if script_name in user_data:
                if user_data[script_name] != data:
                    user_data[script_name] = data
            else:
                user_data[script_name] = data
            user_data[script_name]['executionCount'] = user_data[script_name].get('executionCount', 0) + 1
        else:
            execution_logs[user_id] = {
                data.get('scriptName'): {
                    **data,
                    'executionCount': 1
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
                font-family: 'Roboto', sans-serif;
                background: #1f1f1f;
                color: #e0e0e0;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .container {{
                width: 85%;
                max-width: 1200px;
                background: #2c2c2c;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            }}
            h1 {{
                text-align: center;
                color: #64ffda;
                margin-bottom: 20px;
                font-size: 2rem;
            }}
            .log {{
                background: #333;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            }}
            .log strong {{
                color: #64ffda;
            }}
            pre {{
                background: #444;
                padding: 10px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                color: #b0b0b0;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            table {{
                width: 100%;
                margin-top: 30px;
                border-collapse: collapse;
                text-align: left;
            }}
            th, td {{
                padding: 12px 15px;
                border-bottom: 1px solid #444;
            }}
            th {{
                background-color: #1a1a1a;
                color: #64ffda;
            }}
            td {{
                background-color: #333;
                color: #e0e0e0;
            }}
            tr:hover {{
                background-color: #444;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Execution Logs</h1>
            <div id="log-entries">
                {generate_logs_html()}
            </div>
            <h2 style="text-align: center;">Scripts Executed</h2>
            {generate_scripts_table()}
        </div>
    </body>
    </html>
    """
    return html_content

def generate_scripts_table():
    """Generates the table for scripts executed with counts."""
    if not execution_logs:
        return "<p>No script execution data available.</p>"
    
    script_counts = {}
    for log in execution_logs:
        script_name = log.get('scriptName', 'Unknown')
        if script_name not in script_counts:
            script_counts[script_name] = 1
        else:
            script_counts[script_name] += 1
    
    script_entries = ""
    for script_name, count in script_counts.items():
        script_entries += f"""
        <tr>
            <td>{script_name}</td>
            <td>{count}</td>
        </tr>
        """
    
    return f"""
    <table>
        <thead>
            <tr>
                <th>Script Name</th>
                <th>Execution Count</th>
            </tr>
        </thead>
        <tbody>
            {script_entries}
        </tbody>
    </table>
    """
    
def generate_logs_html():
    """Generates the HTML for execution logs dynamically."""
    if not execution_logs:
        return "<p>No logs available.</p>"
    
    log_entries = ""
    for log in execution_logs:
        log_entries += f"""
        <div class="log">
            <strong>User ID:</strong> {log.get('userId', 'N/A')} <br>
            <strong>Username:</strong> {log.get('username', 'N/A')} <br>
            <strong>Script Name:</strong> {log.get('scriptName', 'N/A')} <br>
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
    return log_entries

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
