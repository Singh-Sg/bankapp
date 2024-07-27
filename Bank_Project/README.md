# Django Banking Application

## Overview

This Django project implements a banking application with the following features:
- Deposit and withdrawal functionalities
- Money transfer between accounts
- Transaction statements

## API Endpoints

### Deposit

- **Endpoint**: `/api/deposit/<account_number>/`
- **Method**: `PATCH`
- **Description**: Deposit money into the specified account.

### Withdrawal

- **Endpoint**: `/api/withdrawal/<account_number>/`
- **Method**: `PATCH`
- **Description**: Withdraw money from the specified account.

### Money Transfer

- **Endpoint**: '/api/transfer/'
- **Method**: 'POST'
- **Description**: Transfer money from one account to another.

### Statement

- **Endpoint**: '/api/statements/<account_number>/'
- **Method**: 'GET'
- **Description**: Retrieve transaction statements for a specified account.

## Setup

### Prerequisites

- Python 3.8+
- Django 3.x+
- Django REST Framework

### Installation

1. Clone the repository:
   ```bash
   git clone <https://github.com/Singh-Sg/bankapp.git>

2. cd <Bank_Project>
3. python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate'
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver

