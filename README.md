# Cyber Security Project

## Installation and Setup

### Requirements
- Python 3
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/A5Beef/cbsproject.git
   cd cbsproject
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the environment:
   Windows:

   ```bash
   source venv/scripts/activate
   ```

   Linux/Mac:

      ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Navigate to mysite:
   ```bash
   cd mysite
   ```

6. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

# Vulnerabilities

## Vulnerability 1: OWASP A01:2021 – Broken Access Control

Affected functionality: Editing and deleting forum posts.

Root cause: The application retrieves posts using their IDs without verifying that the currently authenticated user owns them.

Impact: Any authenticated user who knows or discovers another post's ID and corresponding thread ID can modify or delete that post.

Remediation: Restrict database queries to posts belonging to the currently authenticated user, using author=request.user.