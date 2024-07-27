# Django Banking Application

## Overview

This Django project implements a banking application with the following features:
- User management
- Account management
- Deposit and withdrawal functionalities
- Money transfer between accounts
- Transaction statements

## Models

### User

Represents a user in the banking system.

- `first_name` (CharField): User's first name
- `last_name` (CharField): User's last name
- `contact_number` (CharField): User's contact number

### Account

Represents a bank account associated with a user.

- `pin` (IntegerField): Security PIN for the account
- `user` (OneToOneField): Link to the User model
- `ifsc` (CharField): IFSC code of the branch
- `account_number` (CharField): Unique account number
- `branch_name` (CharField): Name of the branch
- `balance` (DecimalField): Current balance in the account
- `account_type` (CharField): Type of the account (Savings, Current, IBAN)
- `bank_address` (CharField): Address of the bank

### Statement

Represents a transaction statement for an account.

- `account` (ForeignKey): Link to the Account model
- `date` (DateField): Date of the transaction
- `amount` (DecimalField): Amount of the transaction
- `balance` (DecimalField): Balance after the transaction

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
   git clone <repository-url>

2. cd <Bank_Project>
3. python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate'
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver



