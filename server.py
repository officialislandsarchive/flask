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
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                max-width: 960px;
                margin: 20px auto;
                padding: 20px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                text-align: center;
                color: #555;
                margin-bottom: 20px;
                font-size: 2.5em;
            }}
            .user-log {{
                margin-bottom: 15px;
                border: 1px solid #e3e3e3;
                border-radius: 5px;
                padding: 15px;
                background: #fafafa;
            }}
            .user-log h2 {{
                font-size: 1.5em;
                margin-bottom: 10px;
                color: #007BFF;
            }}
            .script-info {{
                padding: 10px;
                margin-bottom: 10px;
                border-left: 4px solid #007BFF;
                background: #f9f9f9;
                border-radius: 4px;
            }}
            .script-info p {{
                margin: 5px 0;
                font-size: 0.95em;
                color: #555;
            }}
            .script-info pre {{
                background: #f4f4f9;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
                font-size: 0.9em;
                border: 1px solid #e3e3e3;
            }}
            .footer {{
                text-align: center;
                padding: 10px 0;
                margin-top: 20px;
                font-size: 0.85em;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Execution Logs</h1>
            {generate_logs_html()}
        </div>
        <div class="footer">&copy; 2025 Execution Logger</div>
    </body>
    </html>
    """
    return html_content


def generate_logs_html():
    """Generates the HTML for execution logs dynamically."""
    if not execution_logs:
        return "<p>No logs available yet.</p>"

    log_entries = ""
    for user_id, user_data in execution_logs.items():
        log_entries += f"""
        <div class="user-log">
            <h2>User ID: {user_id}</h2>
        """
        for script_name, log in user_data.items():
            log_entries += f"""
            <div class="script-info">
                <p><strong>Script Name:</strong> {script_name}</p>
                <p><strong>Execution Count:</strong> {log['executionCount']}</p>
                <p><strong>Experience:</strong> <pre>{log.get('experience', 'N/A')}</pre></p>
                <p><strong>Experience HUD Increment:</strong> <pre>{log.get('experienceHudIncrement', 'N/A')}</pre></p>
                <p><strong>Gamepasses:</strong> <pre>{log.get('gamepasses', 'N/A')}</pre></p>
                <p><strong>Mob Kills:</strong> <pre>{log.get('mobKills', 'N/A')}</pre></p>
                <p><strong>Settings:</strong> <pre>{log.get('settings', 'N/A')}</pre></p>
                <p><strong>Shop State:</strong> <pre>{log.get('shopState', 'N/A')}</pre></p>
                <p><strong>Backpack Items:</strong> <pre>{log.get('backpack', 'N/A')}</pre></p>
                <p><strong>Island Data:</strong> <pre>{log.get('islandData', 'N/A')}</pre></p>
            </div>
            """
        log_entries += "</div>"

    return log_entries


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
