from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# المسار إلى المستودع الخاص بك، قم بتعديله وفقًا لموقعك الفعلي
REPO_PATH = "C:/Users/kunde/my_ai_website"

def run_command(command):
    """ Helper function to run shell commands inside the repo """
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=REPO_PATH)
    return result.stdout if result.returncode == 0 else result.stderr

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    # عند اكتشاف Push Event
    if 'pusher' in data:
        print("📢 GitHub Push Event Detected!")
        response = run_command("git pull origin main")
        return jsonify({"message": "Repository updated", "output": response}), 200
    
    # عند استقبال خطأ من GitHub
    if 'error' in data:
        print("🚨 GitHub Error Detected!")
        error_message = data.get('error')
        response = run_command("git status")
        return jsonify({"message": "Checked Git Status", "error": error_message, "output": response}), 200
    
    return jsonify({"message": "Unhandled event"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
