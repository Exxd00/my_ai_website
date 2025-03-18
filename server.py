from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def run_command(command):
    """ Helper function to run shell commands """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.json
    
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    if 'pusher' in data:
        print("📢 GitHub Push Event Detected!")
        response = run_command("git pull origin main")
        return jsonify({"message": "Updated repository", "output": response}), 200
    
    if 'error' in data:
        print("🚨 GitHub Error Detected!")
        error_message = data.get('error')
        response = run_command("git status")
        return jsonify({"message": "Checked Git Status", "error": error_message, "output": response}), 200
    
    return jsonify({"message": "Unhandled event"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
