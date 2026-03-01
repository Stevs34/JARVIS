import os
import json
import shutil
import subprocess
import requests
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

SKILLS_FILE = "/Users/colesteeves/Desktop/JARVIS/core/skills.py"
BACKUP_DIR = "/Users/colesteeves/Desktop/JARVIS/backups"
LEARNED_FILE = "/Users/colesteeves/Desktop/JARVIS/learned_skills.json"

def load_learned_skills():
    if os.path.exists(LEARNED_FILE):
        with open(LEARNED_FILE, 'r') as f:
            return json.load(f)
    return []

def save_learned_skill(skill):
    skills = load_learned_skills()
    skills.append(skill)
    with open(LEARNED_FILE, 'w') as f:
        json.dump(skills, f, indent=2)

def backup_skills():
    """Backup skills.py before modifying"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{BACKUP_DIR}/skills_{timestamp}.py"
    shutil.copy(SKILLS_FILE, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path

def rollback_skills():
    """Restore most recent backup"""
    if not os.path.exists(BACKUP_DIR):
        return "No backups found sir."
    backups = sorted(os.listdir(BACKUP_DIR))
    if not backups:
        return "No backups found sir."
    latest = os.path.join(BACKUP_DIR, backups[-1])
    shutil.copy(latest, SKILLS_FILE)
    return f"Rolled back to {backups[-1]} sir."

def gpt_write_skill(command):
    """Ask GPT-4 to write a new skill function"""
    prompt = f"""
You are writing a new Python skill function for JARVIS, an AI home assistant running on a Mac.

The user asked: "{command}"

Write a single Python function that handles this request. Follow these rules:
1. Function name must start with "skill_"
2. Must return a string that Jarvis will speak out loud
3. Only use these safe libraries: requests, subprocess, os, datetime, json, math, random
4. No file deletion, no system modifications, no network attacks
5. Must work on macOS
6. Keep it simple and focused on one task
7. Include a docstring

Also provide:
- action_name: a short snake_case name for this action e.g. "get_population"
- description: one sentence describing what it does
- example_phrase: what the user might say to trigger it

Respond ONLY with valid JSON in this format:
{{
    "action_name": "skill_name",
    "description": "what it does",
    "example_phrase": "what user says",
    "function_code": "def skill_name():\\n    ..."
}}
"""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.3
    )
    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)

def claude_review_skill(skill_data):
    """Ask Claude to review the skill for safety and correctness"""
    if not ANTHROPIC_KEY:
        print("No Anthropic API key — skipping Claude review")
        return True, "No Claude review — approved by default"

    prompt = f"""You are reviewing a Python function that will be automatically added to a home automation system called JARVIS.

Action: {skill_data['action_name']}
Description: {skill_data['description']}
Code:
{skill_data['function_code']}

Review this code for:
1. Safety — does it do anything dangerous, destructive or harmful?
2. Correctness — will it actually work on macOS?
3. Scope — is it focused and appropriate for a home assistant?

Respond ONLY with JSON:
{{
    "approved": true or false,
    "reason": "brief explanation",
    "concerns": "any issues found or empty string"
}}"""

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    data = response.json()
    raw = data["content"][0]["text"]
    clean = raw.replace("```json", "").replace("```", "").strip()
    result = json.loads(clean)
    return result["approved"], result.get("reason", ""), result.get("concerns", "")

def test_skill(skill_data):
    """Safely test the skill in a subprocess"""
    test_code = f"""
import sys
{skill_data['function_code']}

try:
    result = {skill_data['action_name']}()
    print("SUCCESS:", result)
except Exception as e:
    print("ERROR:", e)
    sys.exit(1)
"""
    with open("/tmp/jarvis_skill_test.py", "w") as f:
        f.write(test_code)

    result = subprocess.run(
        ["python3", "/tmp/jarvis_skill_test.py"],
        capture_output=True, text=True, timeout=10
    )

    if result.returncode == 0 and "SUCCESS" in result.stdout:
        output = result.stdout.replace("SUCCESS:", "").strip()
        return True, output
    else:
        return False, result.stderr or result.stdout

def add_skill_to_codebase(skill_data):
    """Add the new skill function to skills.py"""
    backup_skills()

    with open(SKILLS_FILE, 'r') as f:
        content = f.read()

    # Add function at the end
    new_code = f"\n\n# AUTO-LEARNED: {skill_data['description']}\n"
    new_code += f"# Added: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    new_code += skill_data['function_code']

    with open(SKILLS_FILE, 'a') as f:
        f.write(new_code)

    save_learned_skill({
        "action_name": skill_data['action_name'],
        "description": skill_data['description'],
        "example_phrase": skill_data['example_phrase'],
        "added": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return True

def learn_new_skill(command, speak_func=None):
    """Full pipeline — write, review, test and add a new skill"""

    def say(text):
        if speak_func:
            speak_func(text)
        print(f"Jarvis: {text}")

    say("Interesting request sir. Let me see if I can learn how to do that.")

    try:
        # Step 1 — GPT writes the skill
        say("Drafting the code now.")
        skill_data = gpt_write_skill(command)
        print(f"GPT wrote skill: {skill_data['action_name']}")

        # Step 2 — Claude reviews it
        say("Sending for review.")
        approved, reason, concerns = claude_review_skill(skill_data)

        if not approved:
            say(f"Claude flagged a concern with that skill sir. {concerns or reason} I won't be adding it.")
            return False, None

        print(f"Claude approved: {reason}")

        # Step 3 — Test it
        say("Running a test.")
        success, output = test_skill(skill_data)

        if not success:
            say(f"The skill failed testing sir. I won't add untested code. Error: {output[:100]}")
            return False, None

        print(f"Test passed: {output}")

        # Step 4 — Add to codebase
        add_skill_to_codebase(skill_data)

        say(f"Done sir. I've learned how to {skill_data['description'].lower()}. You can ask me again and I'll know what to do.")

        return True, skill_data

    except json.JSONDecodeError:
        say("I had trouble parsing the code response sir. Let's try again later.")
        return False, None
    except Exception as e:
        print(f"Self-learn error: {e}")
        say("I encountered an issue learning that skill sir.")
        return False, None

def get_learned_skills():
    """List all auto-learned skills"""
    skills = load_learned_skills()
    if not skills:
        return "No new skills learned yet sir."
    result = f"I have learned {len(skills)} new skills sir. "
    for s in skills[-3:]:
        result += f"{s['description']}. "
    return result
