from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()   

app = Flask(__name__)

# Load Jira config from environment variables
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

def create_jira_ticket(summary, description):
    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Format description in Atlassian Document Format (ADF)
    description_adf = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "text": description,
                        "type": "text"
                    }
                ]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": summary,
            "description": description_adf,
            "issuetype": {
                "name": "Task"
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    return response.status_code, response.json()


@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.json

    if "comment" in data and data["comment"]["body"].strip() == "/Jira":
        issue_url = data["issue"]["html_url"]
        issue_title = data["issue"]["title"]
        user = data["comment"]["user"]["login"]

        summary = f"[GitHub] {issue_title}"
        description = f"Auto-created from GitHub by {user}\n\nOriginal issue: {issue_url}"

        status, result = create_jira_ticket(summary, description)
        return jsonify({"status": status, "jira_response": result}), status
    else:
        return jsonify({"message": "No action taken"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
