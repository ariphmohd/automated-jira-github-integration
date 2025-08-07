**Automated Jira-GitHub Integration**

Seamlessly convert GitHub Issues into Jira tickets with a simple comment!

This repository hosts an automation solution that bridges GitHub and Jira, eliminating manual ticket creation. When a developer comments /Jira on a GitHub Issue, the system automatically generates a corresponding Jira ticket.

**How It Works**

GitHub Webhook Trigger – Listens for /Jira comments on issues.
Python + Flask Backend – Processes the webhook payload and handles Jira API communication.
AWS EC2 Hosting – Ensures reliable 24/7 operation.
Jira API Integration – Creates tickets with issue details, maintaining traceability.


**🔧 Prerequisites**

EC2 instance with port 5000 open in the security group.
Python 3.x and pip installed.
Access to a GitHub repository.
Jira API token & user email (from Atlassian).
Your Jira domain (e.g., yourcompany.atlassian.net).


**1. ⚙️ Prepare EC2 & Flask Environment**
SSH into your EC2 and install required packages:

sudo apt update && sudo apt install -y python3-pip
pip3 install flask requests
 {
    In ubuntu machine need to use python virtual environment
    sudo apt-get update
    sudo apt-get install python3-venv  # install venv module if not present
    python3 -m venv myenv  # create a new virtual env
    source myenv/bin/activate  # activate the environment
    pip install flask
}


**2. 🧪 Create Flask Webhook Listener**
Save this as app.py:

**3. 🛠️ Set Environment Variables (or use .env)**
Edit .bashrc or use a .env loader:

{
   🔧 Step-by-step:
    Install python-dotenv in your virtual environment:
    pip install python-dotenv
    Create a .env file in your project directory:
    nano .env
    Paste the following:
    JIRA_EMAIL=your-email@domain.com
    JIRA_API_TOKEN=your-api-token
    JIRA_DOMAIN=yourdomain.atlassian.net
    JIRA_PROJECT_KEY=DEV

    Save and exit.
    Start your Flask app:
    If it runs without error, your environment is loading correctly.

 
}

**4. 🚀 Run Flask App**
python3 app.py


**5. 🧷 Configure GitHub Webhook**
Go to your GitHub repo.
Settings → Webhooks → Add webhook
Payload URL: http://<EC2-IP>:5000/webhook
Content type: application/json
Secret: (optional but recommended)
Events to trigger: Select "Issue comments".
Save.


**6. 🧪 Test the Flow**
Go to any Issue or Pull Request in the repo.
Comment exactly /Jira
Your Flask app should receive the payload and create a Jira ticket.
