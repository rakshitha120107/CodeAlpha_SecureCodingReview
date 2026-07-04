# CodeAlpha_SecureCodingReview
## Secure Coding Review
CodeAlpha Cyber Security Internship - Task 3

## Overview
This project involves auditing a vulnerable Python 
Flask web application to identify security flaws 
and provide fixes and recommendations.

## Files
- vulnerable_app.py - App with 7 security bugs
- secure_app.py - Fixed and secure version
- SECURE_CODING_REVIEW.md - Full audit report

## Vulnerabilities Found
1. Hardcoded Secret Key
2. Plaintext Password Storage
3. SQL Injection
4. Cross Site Scripting (XSS)
5. Command Injection
6. Insecure Deserialization
7. Debug Mode Enabled

## Tools Used
- Manual Code Review
- Bandit Python Security Analyzer
- OWASP Top 10

## What I Learned
- How SQL Injection works and how to prevent it
- How XSS attacks work and how to escape output
- How command injection works and safe alternatives
- Why passwords must always be hashed
- Importance of keeping secrets out of code
- Why debug mode must be disabled in production

## Language
Python - Flask Web Framework
