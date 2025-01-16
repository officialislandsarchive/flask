from flask import Flask, request, jsonify

app = Flask(__name__)

execution_logs = []

@app.route('/logExecution', methods=['POST'])
def log_execution():
    try:
        data = request.json
        execution_logs.append(data)
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
