# Secure Coding Review Report
CodeAlpha Cyber Security Internship - Task 3

## Application Reviewed
vulnerable_app.py - Python Flask Web Application

## Review Method
Manual code inspection

## Findings Summary

| # | Vulnerability | Severity | Fix |
|---|--------------|----------|-----|
| 1 | Hardcoded Secret Key | Medium | Environment variable |
| 2 | Plaintext Password | High | Password hashing |
| 3 | SQL Injection | Critical | Parameterized queries |
| 4 | XSS | High | Escape output |
| 5 | Command Injection | Critical | subprocess + allow-list |
| 6 | Insecure Deserialization | Critical | Use JSON |
| 7 | Debug Mode Enabled | Medium | Disable in production |

## Detailed Findings

### Finding 1 - Hardcoded Secret Key
Bad: app.secret_key = "supersecret123"
Risk: Anyone can forge session cookies
Fix: app.secret_key = os.environ.get("FLASK_SECRET_KEY")

### Finding 2 - Plaintext Password Storage
Bad: Stores password as plain text in database
Risk: If database is leaked all passwords exposed
Fix: Use generate_password_hash() to store safely

### Finding 3 - SQL Injection (Critical)
Bad: query = "SELECT * FROM users WHERE username = '" + username + "'"
Risk: Hacker can bypass login completely
Fix: cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

### Finding 4 - Cross Site Scripting XSS
Bad: return f"<h1>Welcome, {user}!</h1>"
Risk: Hacker injects malicious scripts into browser
Fix: return f"<h1>Welcome, {escape(user)}!</h1>"

### Finding 5 - Command Injection (Critical)
Bad: os.popen("ping -c 1 " + target)
Risk: Hacker runs any command on server
Fix: subprocess.run(["ping", "-c", "1", target], shell=False)

### Finding 6 - Insecure Deserialization (Critical)
Bad: pickle.loads(raw)
Risk: Remote code execution on server
Fix: json.loads(request.data)

### Finding 7 - Debug Mode Enabled
Bad: app.run(debug=True, host="0.0.0.0")
Risk: Exposes interactive console to network
Fix: app.run(debug=False, host="127.0.0.1")

## Tools Used
- Manual code review
- Bandit (Python security analyzer)
- OWASP Top 10 checklist

## Recommendations
1. Always use parameterized queries
2. Never store plaintext passwords
3. Always escape user input before rendering
4. Never use shell=True with user input
5. Never pickle untrusted data
6. Keep secrets in environment variables
7. Disable debug mode in production
   
