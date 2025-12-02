# Secure Incident Reporting System

Author: Cian O'Connor  
Student Number: 22109668  
Module: Secure Application Programming  

This project demonstrates the difference between secure and insecure software development through a simple incident management web application. Two branches are provided to allow direct comparison between vulnerable and hardened implementations.

---

## Branches

### secure
Secure implementation:
- Django ORM used (no raw SQL)
- CSRF protection enabled
- Internal comments restricted to staff users
- Safer logging practices
- Django escaping for output

### insecure
Insecure implementation:
- SQL injection vulnerability in incident search
- XSS demonstrations
- Weak access control on internal comments
- Sensitive data written to logs

Switch branches using:
git checkout secure
git checkout insecure

---

## Tech Stack

- Django (Python)
- SQLite
- Tailwind CSS
- Playwright for UI testing
- OWASP ZAP for security testing

---

## Setup Instructions

### Create virtual environment
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
npm install

### Apply migrations

### Create admin user

### Run server

Open in browser:
http://127.0.0.1:8000/

---

## Playwright Test

A UI test is available at:
tests/test_incident_flow.py
Run with:
pytest

Ensure the server is running first.

---

## Notes

This repository is part of an academic assignment and not intended for production use. Vulnerabilities in the insecure branch are included intentionally. In real world this would be done in env variables. 

