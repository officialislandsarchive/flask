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
                background: linear-gradient(45deg, #1f1c2c, #4f4b5d);
                color: #f5f5f5;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
            }}
            .container {{
                width: 100%;
                max-width: 1200px;
                background: rgba(0, 0, 0, 0.75);
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                overflow-y: auto;
                max-height: 85vh;
                transition: all 0.3s ease;
            }}
            h1 {{
                text-align: center;
                color: #ff00ff;
                font-size: 2.5em;
                letter-spacing: 2px;
                margin-bottom: 25px;
                text-transform: uppercase;
                font-weight: bold;
                background: linear-gradient(45deg, #ff00ff, #4c6bff);
                -webkit-background-clip: text;
                color: transparent;
            }}
            .user-log {{
                background: #1b1b2f;
                border-radius: 12px;
                margin-bottom: 20px;
                padding: 20px;
                transition: transform 0.3s ease;
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.15);
                position: relative;
                cursor: pointer;
                overflow: hidden;
            }}
            .user-log:hover {{
                transform: translateY(-10px);
                box-shadow: 0 10px 30px rgba(0, 255, 255, 0.25);
            }}
            .user-log h2 {{
                font-size: 1.5em;
                color: #00d4d4;
                text-transform: uppercase;
                margin-bottom: 10px;
                font-weight: bold;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .user-log h2 span {{
                background: #ff00ff;
                padding: 5px 12px;
                border-radius: 8px;
                font-size: 1.2em;
            }}
            .script-info {{
                padding: 12px;
                background: #25253b;
                border-radius: 8px;
                margin-bottom: 15px;
                transition: background 0.3s ease;
            }}
            .user-log:hover .script-info {{
                background: #333340;
            }}
            .script-info pre {{
                background: #1f1f2b;
                color: #a0a0a0;
                border-radius: 8px;
                padding: 10px;
                white-space: pre-wrap;
                word-wrap: break-word;
                font-family: 'Courier New', Courier, monospace;
                font-size: 1em;
                overflow: auto;
            }}
            .execution-count {{
                font-weight: bold;
                color: #ff80e1;
                margin-top: 8px;
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
        return "<p style='color: #ff80e1;'>No logs available yet.</p>"

    log_entries = ""
    for user_id, user_data in execution_logs.items():
        log_entries += f"""
        <div class="user-log">
            <h2>User ID: {user_id} <span>{len(user_data)} Scripts Executed</span></h2>
        """
        for script_name, log in user_data.items():
            log_entries += f"""
            <div class="script-info">
                <strong>Script Name:</strong> {script_name} <br>
                <div class="execution-count">Executed {log['executionCount']} times</div>
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
