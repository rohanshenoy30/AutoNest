# AutoNest - Property Rental Management System

A comprehensive Django-based platform for managing residential rental properties, bridging the gap between property owners and tenants through streamlined communication, financial tracking, and maintenance coordination.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [User Roles](#user-roles)
- [Core Modules](#core-modules)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)

---

## 🎯 Overview

AutoNest is a two-sided rental management platform designed to simplify property rental operations. It provides property owners with tools to manage their portfolio and tenants with a convenient way to handle rent payments and maintenance requests. The system eliminates communication silos by centralizing all rental-related interactions in one place.

**Key Problem It Solves:**
- Manual rent collection and tracking
- Disorganized maintenance request workflows
- Lack of clear communication between owners and tenants
- Difficulty tracking property expenses and services
- No structured way to handle rent adjustments

---

## ✨ Features

### 🏠 For Property Owners
- **Property Portfolio Management**
  - Add and manage multiple properties with addresses and details
  - View all properties at a glance
  
- **Tenant Management**
  - Assign tenants to properties
  - Optionally link tenant accounts for system access
  - Track tenant contact information
  
- **Financial Management**
  - Record rent payments from tenants
  - Track property expenses (utilities, repairs, maintenance)
  - Log services provided (cleaning, landscaping, pest control, etc.)
  - Monitor payment status and history
  
- **Maintenance Workflow**
  - Receive maintenance requests from tenants
  - Review request details (title, description)
  - Approve or deny maintenance requests
  - Track request status (Pending → Approved/Denied)
  
- **Rent Management**
  - Submit rent change demands to tenants
  - Justify rent increases with detailed reasons
  - Track current vs. proposed rent amounts

### 👥 For Tenants
- **Payment Management**
  - Submit rent payments with confirmation
  - Track payment history
  - View payment status
  
- **Maintenance Requests**
  - Submit maintenance/repair requests for their rental unit
  - Provide detailed descriptions of issues
  - Track request status and owner responses
  
- **Rent Notifications**
  - Receive and review rent change demands
  - Understand the reasons for rent adjustments

### 🔐 Security & Authentication
- Secure user authentication with Django's built-in auth system
- Google OAuth integration via Django Allauth
- Email verification support
- Login-required views to protect sensitive data
- Role-based access control (Owner vs. Tenant)

---

## 🏗️ System Architecture

### High-Level Flow

```
User Registration/Login (with Google OAuth option)
    ↓
Select Role (Owner or Tenant)
    ↓
├─→ OWNER DASHBOARD ─→ Property Management ─→ Tenant Assignment ─→ Financial Tracking
│                    ├─→ Expense Tracking
│                    ├─→ Service Logging
│                    ├─→ Maintenance Approval
│                    └─→ Rent Change Management
│
└─→ TENANT DASHBOARD ─→ Payment Submission ─→ Maintenance Requests ─→ Rent Notifications
```

### Data Flow
1. **Owner** creates properties
2. **Owner** adds tenants to properties
3. **Owner** (optionally) links tenant system accounts
4. **Tenant** logs in and views assigned properties
5. **Tenant** submits payments and maintenance requests
6. **Owner** reviews and approves/denies requests
7. **System** maintains audit trail of all transactions

---

## 👨‍💼 User Roles

### Owner Role
- **Permissions**: Full access to property management features
- **Responsibilities**: 
  - Add properties
  - Manage tenants
  - Track finances
  - Approve/deny maintenance requests
  - Send rent change demands

### Tenant Role
- **Permissions**: Limited to submission and viewing of own rental records
- **Responsibilities**:
  - Submit rent payments
  - Submit maintenance requests
  - Review rent change notifications

### Role Switching
Users can switch between Owner and Tenant roles dynamically via the "Set Role" option, allowing property managers who also rent properties to use both personas.

---

## 📦 Core Modules

### 1. **User Profile Management**
```python
UserProfile
├── user (OneToOne with Django User)
├── role (Owner or Tenant)
└── Timestamps (auto-managed)
```
Tracks user role assignment and preferences.

### 2. **Property Management**
```python
Property
├── owner (ForeignKey to User)
├── name (e.g., "Downtown Apartment")
├── address (full property address)
└── Related tenants, expenses, services, maintenance requests
```

### 3. **Tenant Records**
```python
Tenant
├── owner (the property owner who created this tenant record)
├── tenant_user (optional link to Django User account)
├── name, phone (contact info)
├── property (ForeignKey to Property)
└── Related payments & maintenance requests
```

### 4. **Financial Tracking**

**Payments**
```python
Payment
├── owner (who recorded the payment)
├── tenant (which tenant made the payment)
├── amount (rent/payment amount)
├── date (payment date)
└── status (Submitted, Approved, Rejected, etc.)
```

**Expenses**
```python
Expense
├── owner (property owner)
├── property (which property)
├── type (e.g., "Plumbing Repair", "Electricity Bill")
├── amount
└── date
```

**Services**
```python
Service
├── owner (property owner)
├── property
├── service_type (e.g., "Cleaning", "Pest Control")
├── cost
└── date
```

### 5. **Maintenance Workflow**
```python
MaintenanceRequest
├── tenant (tenant requesting)
├── owner (property owner)
├── property
├── title (issue title)
├── description (detailed description)
├── status (Pending → Approved/Denied)
└── created_at (timestamp)
```

### 6. **Rent Management**
```python
RentChangeDemand
├── tenant (affected tenant)
├── owner (property owner)
├── property
├── current_rent (existing rent amount)
├── proposed_rent (new rent amount)
├── reason (justification for increase)
└── created_at (timestamp)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Django 3.2+
- pip package manager
- Virtual environment (recommended)

### Steps

1. **Clone the repository**
   ```bash
   cd AutoNest
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   (If no requirements.txt exists, install: `pip install django django-allauth`)

4. **Navigate to project directory**
   ```bash
   cd rental_system
   ```

5. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

---

## 📖 Usage Guide

### First-Time Setup

1. **Register an Account**
   - Visit the signup page
   - Create account or use Google OAuth
   
2. **Select Your Role**
   - Choose "Owner" if you manage properties
   - Choose "Tenant" if you rent properties
   - You can switch roles anytime

### Owner Workflow

#### Adding a Property
1. Go to Dashboard
2. Click "Add Property"
3. Enter property name and address
4. Submit form
5. Property appears in your portfolio

#### Adding Tenants
1. Click "Add Tenant"
2. Select property from dropdown
3. Enter tenant name and phone
4. Optionally link to system user (search by username)
5. Submit
6. Tenant now appears in property records

#### Recording Payments
1. Click "Add Payment"
2. Select tenant from dropdown
3. Enter amount and date
4. Set status (Approved/Submitted/Rejected)
5. Submit
6. Payment logged for record-keeping

#### Tracking Expenses
1. Click "Add Expense"
2. Select property
3. Enter expense type and amount
4. Set date
5. Submit
6. Expense tracked for property analytics

#### Logging Services
1. Click "Add Service"
2. Select property
3. Enter service type and cost
4. Set date
5. Submit
6. Service recorded

#### Managing Maintenance Requests
1. View "Maintenance Requests" section on dashboard
2. Review tenant's request (title, description)
3. Click update button
4. Set status to "Approved" or "Denied"
5. Save
6. Tenant receives notification

#### Requesting Rent Changes
1. Click "Add Rent Change Demand"
2. Select tenant
3. Enter current and proposed rent amounts
4. Add reason for increase
5. Submit
6. Tenant can review demand

### Tenant Workflow

#### Submitting Payments
1. Go to Dashboard
2. Click "Add Payment"
3. Select which property/tenant record
4. Enter amount, date, and status (auto-set to "Submitted")
5. Submit
6. Payment marked for owner review

#### Requesting Maintenance
1. Click "Add Maintenance Request"
2. Select your tenant record
3. Enter issue title and detailed description
4. Submit
5. Owner receives request and can approve/deny

#### Reviewing Rent Changes
1. View "Rent Change Demands" section
2. See current rent vs. proposed rent
3. Review owner's reasoning
4. No action required (informational)

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 3.2+ |
| **Database** | SQLite (development) |
| **Authentication** | Django Auth + Google OAuth (django-allauth) |
| **Frontend** | HTML5, CSS3, Bootstrap |
| **Template Engine** | Django Templates |
| **Security** | CSRF protection, SQL injection prevention |

### Key Libraries
- `django-allauth` - User authentication & social login
- `django` - Web framework & ORM
- `psycopg2` (optional) - PostgreSQL support for production

---

## 📊 Database Schema

### Entity Relationship Diagram

```
User (Django Auth)
├── UserProfile (1:1) → role (Owner/Tenant)
├── Property (1:N) → properties owned
├── Tenant (1:N) → as owner
├── Tenant (1:N) → as tenant_user
├── Payment (1:N) → payments recorded
├── Expense (1:N) → expenses tracked
├── Service (1:N) → services logged
├── MaintenanceRequest (1:N) → as owner
└── RentChangeDemand (1:N) → as owner

Property (1:N)
├── Tenant
├── Expense
├── Service
└── MaintenanceRequest

Tenant (1:N)
├── Payment
├── MaintenanceRequest
└── RentChangeDemand
```

### Key Relationships
- **User → Property**: One owner has many properties
- **User → Tenant**: One owner has many tenant records
- **Property → Tenant**: One property has many tenants
- **Tenant → Payment**: One tenant has many payments
- **Tenant → MaintenanceRequest**: One tenant has many requests
- **Property → Expense**: One property has many expenses
- **Property → Service**: One property has many services

---

## 🔒 Security Considerations

### Current Implementation
- Login required for all data views (`@login_required`)
- Role-based access control on all operations
- CSRF protection enabled
- SQL injection prevention via Django ORM

### Best Practices for Deployment
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Configure `ALLOWED_HOSTS` properly
- Use PostgreSQL instead of SQLite in production
- Enable HTTPS
- Set up proper backups

---

## 📝 Future Enhancement Ideas

- SMS notifications for maintenance requests
- Email reminders for rent payments
- Automated rent payment processing
- Document upload (lease agreements, inspection reports)
- Advanced reporting and analytics
- Mobile app for tenants
- Property photos gallery
- Rating/review system
- Late payment notifications
- Tenant screening workflow

---

## 📧 Support & Contact

For issues, feature requests, or improvements, please refer to the project structure and code documentation.

---

**AutoNest** - Making property rental management simple and efficient. 🏠
