# 🏛️ Community Hall Booking & Management System

> **VTU Community Engineering Project #78**  
> **Specialization:** Track A — Web (Python + Flask + MySQL / SQLite + HTML/CSS/JS + Bootstrap 5 + Chart.js)  
> **Program Outcome:** PO 6 (The Engineer and Society)  
> **Sustainable Development Goal:** SDG 11 (Sustainable Cities and Communities - Target 11.7)  

---

## 🌟 Measurable Engineering Outcomes Accomplished

1. **Manage Community Hall Bookings:** Complete self-service portal to browse auditoriums, check seating limits, select date/time windows, auto-calculate tariffs, and generate booking passes.
2. **Track Hall Availability:** Real-time visual availability schedule with automated slot-overlap prevention (`409 Conflict` validation).
3. **Process Booking Requests:** Municipal Admin dashboard with single-click **Approval** and **Rejection** (with citizen feedback note & notification).
4. **Schedule Maintenance:** Facility downtime scheduler that marks halls under maintenance, blocks overlapping citizen reservations, and records maintenance history.
5. **Maintain Booking Records:** Searchable audit trail of all transactions with downloadable and printable digital booking receipts.
6. **Mobile Responsive Architecture:** Accessible on desktop browsers as well as smartphones over local Wi-Fi.

---

## 📁 Repository Directory Structure

```text
my-flask-app/
├── app.py                      # Flask Application Server & REST API endpoints
├── db.py                       # SQL Database Abstraction & CRUD Operations Layer
├── requirements.txt            # Python Dependencies
├── Procfile                    # Deployment Configuration
├── database/
│   ├── schema.sql              # Standard SQL Schema & Seed Data (SQLite / MySQL)
│   ├── schema_mysql.sql        # MySQL 8.0 Script for MySQL Workbench
│   └── community_hall.db       # Active SQLite Database (instant offline execution)
├── documentation/
│   └── PROJECT_REPORT.md       # Comprehensive Project Report, PO6/SDG11 & UML Diagrams
├── test/
│   └── test_api.py             # Automated Unit & REST API Integration Tests
├── screenshots/                # Visual UI captures
├── static/                     # CSS, JS, Assets
└── templates/                  # Jinja2 Responsive UI Templates
    ├── base.html               # Shared master layout with mobile drawer & topbar
    ├── login.html              # Citizen & Admin Authentication
    ├── register.html           # New Citizen Registration
    ├── forgot_password.html    # Password Recovery
    ├── reset_password.html     # Password Reset Form
    ├── dashboard.html          # Interactive Analytics Dashboard with Chart.js
    ├── halls.html              # Searchable Community Hall Catalog & Filters
    ├── hall_detail.html        # Hall Specifications, Amenities & Tariff
    ├── book_hall.html          # Live Tariff Estimator & Reservation Form
    ├── my_bookings.html        # Booking Pass & Receipt Generation
    ├── availability.html       # Real-Time Schedule Calendar
    ├── admin.html              # Municipal Officer Control Panel & Maintenance Scheduler
    └── profile.html            # Citizen Profile Editor
```

---

## 🚀 Quick Start Guide

### 1. Requirements
- Python 3.10+ installed
- Dependencies installed via:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Run the Application
Execute the following in your project directory:
```bash
python app.py
```

### 3. Open in Browser (Desktop / Laptop)
Navigate to:
```
http://localhost:5000
```
or
```
http://127.0.0.1:5000
```

---

## 📱 How to Open and Run on Your Mobile Phone

1. Make sure your **Mobile Phone** and **Computer** are connected to the **SAME Wi-Fi network**.
2. Run `python app.py` on your computer (it is configured to host on `0.0.0.0`).
3. Open your smartphone browser (Chrome / Safari) and enter your computer's local IP address:
   ```
   http://10.143.154.227:5000
   ```
4. The web application will load in responsive mobile mode with a slide-out drawer menu, touch-friendly buttons, and mobile-optimized booking forms!

*(Note: If the page does not open on your phone, ensure Windows Firewall allows incoming connections on port 5000).*

---

## 🔑 Default Credentials

| Role | Username | Password | Email | Notes |
|---|---|---|---|---|
| **Administrator** | `admin` | `admin123` | `admin@communityhall.gov.in` | Full access to Admin Panel & Maintenance Scheduler |
| **Citizen (Sample)** | Register a new user via `/register` or sign in as admin |

---

## 🧪 Running Automated Tests

To execute the automated REST API & unit tests:
```bash
python test/test_api.py
```
Expected output:
```text
Ran 4 tests in 0.246s
OK
[PASS] test_01_get_halls_api
[PASS] test_02_get_single_hall_api
[PASS] test_03_create_booking_api
[PASS] test_04_booking_conflict_prevention
[PASS] test_05_update_booking_status_api
[PASS] test_06_analytics_api
```

---

## 📊 REST API Endpoints (Section 7 of Mandatory Syllabus)

Tested via Postman or `curl`:
- `GET /api/halls` - Returns JSON array of all facilities
- `GET /api/halls/1` - Returns single hall details
- `POST /api/bookings` - Submit reservation (JSON body: `{"hall_id": 1, "booking_date": "YYYY-MM-DD", "start_time": "HH:MM", "end_time": "HH:MM", "purpose": "...", "attendees": 50}`)
- `PUT /api/bookings/<id>` - Update status (`approved`, `rejected`, `cancelled`)
- `DELETE /api/bookings/<id>` - Delete booking record
- `GET /api/analytics` - Telemetry data for Chart.js
