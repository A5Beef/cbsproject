# Cyber Security Project

This project is a work in progress and will contain five security
demonstrations. This README currently documents the first three; the remaining
two will be added as they are developed. Follow these lab steps on a local
copy of the repository only. Vulnerability 1 is enabled by changing the
post-ownership checks in the code. Vulnerabilities 2 and 3 are controlled by
settings in `.env`.

## Installation and Setup

### Requirements

- Python 3
- pip

### Setup

1. Clone the repository and enter its root directory:
   ```bash
   git clone https://github.com/A5Beef/cbsproject.git
   cd cbsproject
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   ```

   Linux/macOS:
   ```bash
   source venv/bin/activate
   ```

   Windows:
   ```powershell
   source venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a Fernet key:
   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

5. In the repository root (the directory containing `README.md`), create a
   `.env` file with the generated key and the default secure setting:
   ```env
   FERNET_KEY=paste_generated_key_here
   ENCRYPT_MESSAGES=True
   VULNERABLE_SEARCH=False
   ```

   Keep this key unchanged while you have encrypted messages you want to read.

6. Enter the Django project, migrate the database, and create an admin account:
   ```bash
   cd mysite
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

   Open the app at `http://127.0.0.1:8000/` and Django Admin at
   `http://127.0.0.1:8000/admin/`. Use the superuser credentials for Admin.
   Register regular users through the app for the demonstrations.

## Vulnerability 1: OWASP A01:2021 – Broken Access Control

This demonstrates missing ownership checks on post edit/delete operations.
The checks are enabled in the starting code; make the following local change
to turn on the vulnerability.

### Enable and demonstrate

1. Open `mysite/board/views.py`.
2. In **both** `edit_post` and `delete_post`, find the `get_object_or_404`
   lookup containing this condition:
   ```python
   author=request.user
   ```
   Comment out that line in both functions:
   ```python
   # author=request.user
   ```
3. Save the file. Django's development server normally reloads automatically;
   restart it if it does not.
4. Register two regular users, for example Alice and Bob. Log in as Alice,
   create a thread, and add a reply.
5. In Django Admin, open **Board > Posts** and click Alice's reply. Note the
   post ID shown in the Admin page URL. Note the thread ID from the thread's
   URL in the app.
6. Log in to the app as Bob and open this URL, replacing the IDs with the ones
   you noted:
   ```text
   http://127.0.0.1:8000/thread/<thread_id>/post/<post_id>/edit/
   ```
   The page lets Bob edit Alice's reply even though the thread page does not
   show Bob the Edit link. The corresponding URL ending in `/delete/` also
   allows Bob to reach the delete confirmation page.

### Restore the ownership check

Uncomment `author=request.user` in both lookups in `mysite/board/views.py`.
With the checks restored, Bob's direct edit/delete URL should return a 404
instead of allowing access.

## Vulnerability 2: OWASP A02:2021 – Cryptographic Failures

This demonstrates a different issue: private-message content is stored in
plaintext when encryption is disabled. A person with database access can read
that content without using the app's message permissions. Encryption is
controlled by `.env`; a valid `FERNET_KEY` is required when it is enabled.

### Demonstrate plaintext storage

1. Stop the development server.
2. In the repository-root `.env` file, change the setting to:
   ```env
   ENCRYPT_MESSAGES=False
   ```
3. Restart the server and log in to the app as one regular user. Send a new
   private message to the other user.
4. Open Django Admin, select **Board > Messages**, and click the message you
   just sent.
5. The **Content** field shows the message in readable plaintext.

### Enable encryption and compare

1. Stop the server and set `ENCRYPT_MESSAGES=True` in `.env`. Keep the same
   valid `FERNET_KEY`.
2. Restart the server and send a **new** private message.
3. Open that message in Django Admin. Its **Content** field is encrypted
   ciphertext; open the message in the app to see the original text.

The setting affects newly sent messages only. Changing it does not convert
existing messages, so use a new message for each comparison.

## Vulnerability 3: OWASP A03:2021 – Injection

This demonstrates SQL injection in the thread-title search. When the
vulnerable setting is enabled, the search term is concatenated directly into a
SQL query. The default setting uses Django's ORM, which safely handles the
search term.

### Enable and demonstrate

1. Stop the development server.
2. In the repository-root `.env` file, add or change the setting to:
   ```env
   VULNERABLE_SEARCH=True
   ```
3. Restart the server and open **Search discussions** in the app.
4. Search for a title that does not match any thread and note that there are
   no results.
5. Search for this input:
   ```text
   ' OR '1'='1' --
   ```
   The injected condition is always true, so the vulnerable query returns all
   threads, including those whose titles do not match the search.

### Restore the safe search

1. Stop the server and set `VULNERABLE_SEARCH=False` in the repository-root
   `.env` file.
2. Restart the server and repeat the search. The input is now treated as
   ordinary text, and only matching titles are returned.

The safe implementation uses Django's ORM in `mysite/board/views.py`:
```python
threads = Thread.objects.filter(title__icontains=search_query)
```
