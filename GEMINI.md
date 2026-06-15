# GEMINI.md - Finanpy Project Instructions

This document provides essential context and instructions for AI agents working on the Finanpy project.

## Project Overview
Finanpy is a personal finance management system built with **Python 3.12+** and **Django 6+**. It aims to provide a simple and efficient way for users to track bank accounts, categories, and transactions through a modern, responsive web interface.

### Architecture
- **Backend:** Django 6 (Full-stack approach).
- **Frontend:** Django Template Language (DTL) integrated with TailwindCSS.
- **Database:** SQLite3 (default for development).
- **App Structure:**
  - `core/`: Global configuration.
  - `accounts/`: Bank account management.
  - `categories/`: Transaction categorization.
  - `transactions/`: Financial movements (income/expense).
  - `profiles/`: User profile extensions.
  - `users/`: User authentication and management.

## Building and Running
The project uses a standard Django workflow.

### Commands
- **Install Dependencies:** `pip install -r requirements.txt`
- **Apply Migrations:** `python manage.py migrate`
- **Create Migrations:** `python manage.py makemigrations`
- **Start Development Server:** `python manage.py runserver`
- **Run Tests:** `python manage.py test`
- **Create Superuser:** `python manage.py createsuperuser`

## Development Conventions

### Coding Standards
- **Language:** Code (variable names, functions, classes, comments) MUST be in **English**.
- **Style:** Follow **PEP 8** strictly.
- **Strings:** Use **single quotes** (`'`) unless double quotes are necessary.
- **Imports:** Group imports according to PEP 8 (standard library, third-party, local apps).

### Architecture & Design
- **Surgical Changes:** Modify only what is necessary.
- **Models:** Include `created_at` and `updated_at` fields in all models for auditability.
- **UI:** The User Interface (templates) should be in **Portuguese (Brasil)** as per requirements.
- **Responsiveness:** Use TailwindCSS classes for a mobile-first approach.

### Documentation
- Reference `PRD.md` for business requirements and feature specifications.
- Technical documentation and guides are located in the `docs/` directory.

## Current Project Status
- The project is in the initial scaffolding phase.
- Apps are created and registered in `settings.py`, but models and views are currently placeholders.
- Implementation must align with the specifications detailed in `PRD.md`.
