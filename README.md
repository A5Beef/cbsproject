# cbsproject

Cyber Security Project


Vulnerability 1: OWASP A01:2021 – Broken Access Control

Affected functionality: Editing and deleting forum posts.

Root cause: The application retrieves posts using their IDs without verifying that the currently authenticated user owns them.

Impact: Any authenticated user who knows or discovers another post's ID and corresponding thread ID can modify or delete that post.

Remediation: Restrict database queries to posts belonging to the currently authenticated user, using author=request.user.