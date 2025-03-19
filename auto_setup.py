import os
import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Successfully ran: {command}")
    else:
        print(f"❌ Error running: {command}\n{result.stderr}")

# Step 1: Update README.md
readme_content = """# My AI Website

مشروع ذكاء اصطناعي لتحليل البيانات والمحادثات باستخدام **Python** و **Flask**.

## 💡 الميزات
- تحليل البيانات باستخدام الذكاء الاصطناعي
- دعم المحادثات التفاعلية
- سهل النشر والاستخدام

## 🚀 كيفية التشغيل
```sh
git clone https://github.com/exxd00/my_ai_website.git
cd my_ai_website
pip install -r requirements.txt
python app.py
```

## 📌 روابط مفيدة
🔗 [الموقع الرسمي](https://exxd00.github.io/my_ai_website/)  
📖 [التوثيق](https://github.com/exxd00/my_ai_website/wiki)
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
print("✅ README.md updated successfully.")

# Step 2: Generate requirements.txt
run_command("pip freeze > requirements.txt")

# Step 3: Setup GitHub Actions workflow
github_actions_path = ".github/workflows/deploy.yml"
os.makedirs(os.path.dirname(github_actions_path), exist_ok=True)
github_actions_content = """
name: Deploy My AI Website

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run application
        run: python app.py
"""

with open(github_actions_path, "w", encoding="utf-8") as f:
    f.write(github_actions_content)
print("✅ GitHub Actions workflow created.")

# Step 4: Commit and push changes
git_commands = [
    "git add .",
    'git commit -m \"Automated setup: Updated README, added requirements.txt, and setup GitHub Actions\"',
    "git pull --rebase origin main",
    "git push origin main"
]

for cmd in git_commands:
    run_command(cmd)

print("🚀 Setup complete! Your project is updated and deployed.")
