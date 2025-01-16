from flask import Flask, request, jsonify, render_template

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
    return render_template('logs.html', logs=execution_logs)

if __name__ == '__main__':
    app.run(debug=True)
