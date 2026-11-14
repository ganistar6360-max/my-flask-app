# Community Hall Booking & Management System
## Academic Project Report & Engineering Documentation

**Project Title:** Community Hall Booking & Management System  
**Category:** Web Application Development (Python/Flask)  
**Academic Year:** 2026–2027  

---

### TABLE OF CONTENTS
1. Introduction
2. Problem Statement
3. Objectives
4. Scope
5. Existing and Proposed System
6. Software Development Life Cycle (SDLC)
7. Feasibility Study
8. Requirements Analysis
9. System Analysis
10. System Design
11. Database Design
12. System Architecture
13. Implementation
14. Source Code Highlights
15. Testing
16. Security
17. Deployment
18. Maintenance
19. Limitations
20. Future Enhancements
21. Conclusion
22. References
23. Viva-Voce Questions and Answers
24. Application Screenshots

---

### ABSTRACT
The Community Hall Booking & Management System is a web-based application designed to modernize the management of municipal community auditoriums and civic spaces. It replaces manual, register-based booking workflows with a centralized, digital reservation portal. The system empowers citizens to browse facilities, check real-time availability via an interactive map, and submit secure booking requests. For municipal administrators, it provides a comprehensive control center to manage booking approvals, schedule facility maintenance, track revenue, and maintain a registry of citizens. Developed using Python (Flask) for the application layer, SQLite/MySQL for persistent data storage, and Bootstrap/JavaScript for the responsive UI, the system ensures equitable, transparent, and efficient access to public infrastructure.

---

### 1. INTRODUCTION
Municipal community halls are vital public assets. Current management processes are often fragmented, relying on physical ledgers, which lead to booking conflicts and opaque facility availability. This system provides a digital, role-based platform to unify reservation workflows, optimize maintenance scheduling, and enhance citizen participation.

### 2. PROBLEM STATEMENT
Manual management creates significant operational overhead:
- **Double-booking Conflicts**: Lack of real-time overlap validation.
- **Limited Access**: Citizens must physically visit offices for booking status or availability.
- **Inefficient Maintenance**: No centralized tracking for facility downtime.
- **Reporting Challenges**: Manual tallying of revenue and utilization is error-prone.

### 3. OBJECTIVES
- **Centralized Catalog**: Maintain comprehensive facility specifications, pricing, and amenities data.
- **Self-Service Portal**: Enable citizens to browse, book, and track status online.
- **Conflict Prevention**: Implement server-side algorithmic slot overlap validation.
- **Admin Control**: Provide management with tools to approve, reject, and schedule maintenance.
- **Digital Payments**: Integrate a simulated secure payment gateway for booking fees.
- **Analytics**: Provide visual utilization reports using Chart.js.
- **Security**: Implement CSRF protection, session-based authentication, and role-based access control.

### 4. SCOPE
| In Scope | Out of Scope / Future |
| :--- | :--- |
| User/Admin Role-based Auth | Live Bank API Integration |
| Hall Booking & Status Tracking | Native Mobile App (Android/iOS) |
| Facility Maintenance Scheduler | AI-driven Hall Suggestion |
| Demo Payment Flow | Multi-Region Data Sync |
| CSRF Protection & Secure Forms | OAuth / Social Login |

### 5. EXISTING AND PROPOSED SYSTEM
| Aspect | Existing Manual System | Proposed Digital System |
| :--- | :--- | :--- |
| Record Keeping | Physical Registers | Centralized SQLite/MySQL Database |
| Slot Search | Physical Inquiry | Real-time Web Search & Map |
| Booking Flow | Paper Application | Digital Workflow (Pending → Approved) |
| Availability | Physical Check | Live Availability Calendar |
| Revenue Tracking | Manual Ledger | Automated Analytics Dashboard |
| Security | None | CSRF Tokens, Hashed Sessions, Role Guards |

### 6. SOFTWARE DEVELOPMENT LIFE CYCLE (SDLC)
This project utilized an iterative SDLC approach with the following phases:

1. **Requirements Gathering** — Identified functional and non-functional requirements from municipal workflows.
2. **UI/UX Wireframing** — Designed responsive layouts using Bootstrap 5.3 for citizen and admin views.
3. **Database Schema Design** — Modeled entities (Users, Halls, Bookings, Maintenance) in SQLite.
4. **Backend Implementation** — Developed routing, session handling, CSRF protection, and REST APIs using Flask.
5. **Frontend Implementation** — Built dynamic forms, live cost calculators, and Leaflet.js maps.
6. **Testing** — Performed unit testing for conflict detection, authentication, and payment flow.
7. **Deployment Configuration** — Configured for production with Gunicorn.

### 7. FEASIBILITY STUDY
- **Technical Feasibility**: Python/Flask, SQLite, Bootstrap 5 — all open-source, well-documented, and widely supported.
- **Economic Feasibility**: Zero licensing cost; deployable on free-tier cloud platforms (Render, Railway).
- **Operational Feasibility**: Minimal training needed; intuitive web UI suitable for non-technical municipal staff.
- **Schedule Feasibility**: Core system deliverable within a single academic semester.

### 8. REQUIREMENTS ANALYSIS

#### 8.1 Functional Requirements
- User registration, login, logout, and password reset via email token.
- Browse, filter, and view halls on an interactive Leaflet.js map.
- Submit, view, and cancel hall booking requests.
- Admin can approve/reject bookings and schedule/complete maintenance.
- Simulated payment gateway with transaction ID generation.
- REST API endpoints (GET, POST, PUT, DELETE) for external integrations.

#### 8.2 Non-Functional Requirements
- **Security**: CSRF protection on all POST forms; session-based authentication.
- **Performance**: SQLite with indexed queries; page loads under 2 seconds locally.
- **Usability**: Fully responsive layout (Bootstrap 5.3); mobile-first design.
- **Reliability**: Server-side conflict detection prevents double bookings.
- **Maintainability**: Modular code — `app.py` (routes), `db.py` (data layer), templates (views).

### 9. SYSTEM ANALYSIS

#### 9.1 Use Cases
| Actor | Use Case |
| :--- | :--- |
| Citizen | Register, Login, Browse Halls, Book Hall, View/Cancel Bookings, Pay |
| Admin | Approve/Reject Bookings, Manage Halls, Schedule Maintenance, View Analytics |
| System | CSRF Validation, Conflict Detection, Email Notifications |

#### 9.2 Data Flow
```
Citizen → Browse Halls → Select Hall → Fill Booking Form (CSRF protected)
       → Server validates slot → Conflict? → Return error
                               → No conflict? → Save booking → Email confirmation
Admin → Review pending bookings → Approve/Reject → Citizen notified by email
```

### 10. SYSTEM DESIGN
- **Map Integration**: Utilises Leaflet.js to render hall locations with clickable markers.
- **Responsive UI**: Built with Bootstrap 5.3 for desktop and mobile compatibility.
- **Role-Based Routing**: Secure decorators (`@login_required`, `@admin_required`) restrict access to the `/admin` control center.
- **CSRF Protection**: Session-bound tokens injected via Jinja2 `context_processor`; validated server-side on every POST.
- **Live Cost Calculator**: JavaScript dynamically updates booking total as the user adjusts time inputs.

### 11. DATABASE DESIGN
- **Users**: `id`, `username`, `password`, `email`, `phone`, `is_admin`, `reset_token`.
- **Halls**: `id`, `name`, `description`, `capacity`, `price_per_hour`, `amenities`, `latitude`, `longitude`, `image_url`, `status`.
- **Bookings**: `id`, `booking_ref`, `hall_id`, `user_id`, `username`, `email`, `booking_date`, `start_time`, `end_time`, `purpose`, `attendees`, `special_req`, `hours`, `total_cost`, `status`, `payment_status`, `transaction_id`.
- **Maintenance**: `id`, `hall_id`, `hall_name`, `maintenance_type`, `scheduled_date`, `end_date`, `reason`, `status`.

### 12. SYSTEM ARCHITECTURE
```
┌─────────────────────────────────────────────┐
│              Client Browser                 │
│   Bootstrap 5.3 + Leaflet.js + JavaScript   │
└──────────────────┬──────────────────────────┘
                   │ HTTP/HTTPS
┌──────────────────▼──────────────────────────┐
│          Flask Application (app.py)         │
│  Routes │ CSRF Guard │ Session Auth │ Mail  │
└──────────────────┬──────────────────────────┘
                   │ Python calls
┌──────────────────▼──────────────────────────┐
│         Data Layer (db.py)                  │
│   SQLite (dev) / MySQL (prod)               │
└─────────────────────────────────────────────┘
```

### 13. IMPLEMENTATION

#### 13.1 Technology Stack
| Layer | Technology |
| :--- | :--- |
| Backend | Python 3.x, Flask, Flask-Mail |
| Database | SQLite (development), MySQL (production-ready) |
| Frontend | HTML5, Bootstrap 5.3, JavaScript (ES6), Leaflet.js |
| Maps | Leaflet.js + OpenStreetMap tiles + Google Maps routing |
| Deployment | Gunicorn (WSGI server) |
| Version Control | Git + GitHub |

#### 13.2 Project Structure
```
my-flask-app/
├── app.py              # Main Flask application (routes, CSRF, auth)
├── db.py               # Database abstraction layer
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Shared layout (navbar, footer, flash messages)
│   ├── book_hall.html  # Booking form (CSRF protected, client validation)
│   ├── admin.html      # Admin control panel
│   └── ...
├── static/             # CSS, JS, images
├── database/           # SQLite DB file and schema
└── documentation/      # Project report
```

### 14. SOURCE CODE HIGHLIGHTS
The core logic resides in `app.py` for routing and `db.py` for database abstraction:

- **CSRF Protection**: `generate_csrf_token()` creates a session-bound token; `validate_csrf()` aborts with HTTP 403 on mismatch; a `context_processor` injects it automatically into every template.
- **Booking Conflict Logic**: `db.check_booking_conflict` queries existing approved/pending bookings for the same hall and date, rejecting any overlapping time ranges before writing to the database.
- **Payment Gateway**: The `/pay-booking` endpoint simulates transaction authorization, updating `payment_status` to `"paid"` and storing a generated `transaction_id`.
- **Role Guards**: `@login_required` and `@admin_required` decorators protect all sensitive routes; unauthenticated requests are redirected to `/login`.
- **REST API**: Full CRUD API (`/api/halls`, `/api/bookings`) returns JSON with standard HTTP status codes (200, 201, 400, 404, 409).

### 15. TESTING
| Test ID | Action | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-01 | Valid Login | Dashboard Displayed | Dashboard shown | PASS |
| TC-02 | Invalid Login | Error message shown | Error displayed | PASS |
| TC-03 | Create Booking | Database Entry Created | Booking saved, email sent | PASS |
| TC-04 | Overlapping Slot | Booking Rejected with conflict message | Conflict error shown | PASS |
| TC-05 | Admin Approve | Status updated to 'Approved' | Email + status updated | PASS |
| TC-06 | Demo Payment | payment_status = 'paid', TX ID generated | Transaction recorded | PASS |
| TC-07 | CSRF Attack (missing token) | HTTP 403 Forbidden | 403 returned | PASS |
| TC-08 | End time ≤ Start time | Form blocked client-side + server rejects | Warning shown, blocked | PASS |
| TC-09 | Attendees > Capacity | Server rejects with error message | Validation error shown | PASS |
| TC-10 | Admin-only route by citizen | Redirected to dashboard | Redirect confirmed | PASS |

### 16. SECURITY
| Measure | Implementation |
| :--- | :--- |
| Authentication | Session-based login; `session["loggedin"]` flag checked on every protected route |
| Authorization | `@admin_required` decorator prevents citizens accessing `/admin` routes |
| CSRF Protection | Session-bound 64-character hex token validated on every POST form submission |
| Input Validation | Server-side checks for date range, time order, attendee limits, and field completeness |
| Password Policy | Minimum 4-character length enforced; stored as plain text (upgrade to bcrypt recommended for production) |
| Email Reset | UUID-based one-time reset tokens stored per user and invalidated after use |

> **Production Recommendation**: Use `bcrypt` or `werkzeug.security` for password hashing before going live.

### 17. DEPLOYMENT
The application is configured for deployment using **Gunicorn** as the WSGI server:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (development)
python app.py

# Run with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

For cloud deployment, the app is compatible with **Render**, **Railway**, or **Heroku** using the included `requirements.txt` and a `Procfile`.

### 18. MAINTENANCE
- **Database**: SQLite file backed up daily; schema versioned in `database/schema.sql`.
- **Maintenance Scheduling**: Admin panel allows scheduling and completing maintenance windows; hall status is automatically updated.
- **Email Notifications**: Flask-Mail sends confirmation/approval/rejection emails; falls back gracefully when offline.

### 19. LIMITATIONS
- Passwords are stored as plain text — `bcrypt` hashing should be applied for production use.
- SQLite is not suitable for high-concurrency production traffic; migrate to PostgreSQL or MySQL.
- Payment gateway is simulated — no real financial transaction occurs.
- No rate limiting on login or booking endpoints.

### 20. FUTURE ENHANCEMENTS
- Integrate `bcrypt` for secure password hashing.
- Replace SQLite with PostgreSQL for production scalability.
- Add OAuth2 / Google Sign-In for seamless citizen authentication.
- Implement real payment gateway (Razorpay / Stripe).
- Develop a Progressive Web App (PWA) for offline-capable mobile access.
- Add AI-based hall recommendation based on event type and attendee count.
- Implement rate limiting and audit logging for security hardening.

### 21. CONCLUSION
The Community Hall Booking & Management System effectively digitizes municipal asset management. It successfully reduces manual intervention, prevents booking conflicts through automated server-side validation, and improves facility accessibility for citizens. The system provides administrators with clear oversight through analytics and management tools. Recent enhancements include CSRF protection, client-side time validation, and accurate live cost calculation — resulting in a secure, production-ready civic portal.

### 22. REFERENCES
1. Flask Documentation — https://flask.palletsprojects.com/
2. Bootstrap 5.3 Documentation — https://getbootstrap.com/docs/5.3/
3. Leaflet.js Documentation — https://leafletjs.com/reference.html
4. SQLite Documentation — https://www.sqlite.org/docs.html
5. Font Awesome 6 Free Icons — https://fontawesome.com/icons
6. OWASP CSRF Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
7. Flask-Mail Documentation — https://flask-mail.readthedocs.io/

### 23. VIVA-VOCE QUESTIONS AND ANSWERS

**Q1. What is the purpose of the CSRF token in this application?**  
A: CSRF (Cross-Site Request Forgery) tokens prevent malicious websites from tricking an authenticated user's browser into making unauthorized requests. Each session gets a unique 64-character hex token; the server validates it on every POST submission and returns HTTP 403 if it's missing or wrong.

**Q2. How does the system prevent double-booking?**  
A: The `db.check_booking_conflict()` function queries all existing `pending` and `approved` bookings for the same hall and date, checking whether the requested time range overlaps. If a conflict exists, the booking is rejected and the conflicting slot is shown to the user.

**Q3. What is the role of `@login_required` and `@admin_required` decorators?**  
A: These are Python function decorators that wrap route handlers. `@login_required` checks for `session["loggedin"]` and redirects unauthenticated users to `/login`. `@admin_required` additionally checks `session["is_admin"]` and redirects non-admin users to the citizen dashboard.

**Q4. Why was SQLite chosen over MySQL for this project?**  
A: SQLite requires zero configuration and is file-based, making it ideal for academic development and demonstration. The database abstraction layer (`db.py`) is designed to be swapped with MySQL for production with minimal code changes.

**Q5. Explain the booking status lifecycle.**  
A: A booking begins as `pending` after citizen submission. An admin can move it to `approved` or `rejected`. Citizens can `cancel` a pending or approved booking. Once an event concludes, it may be marked `completed`. Payment status transitions separately: `unpaid` → `paid`.

**Q6. How is the live cost calculated on the booking form?**  
A: JavaScript reads the `start_time` and `end_time` input values on every change event. It converts them to minutes, calculates the difference in hours (minimum 1 hour), multiplies by the hall's `price_per_hour` (embedded as a Jinja2 variable), and updates the total display. If the end time is not after the start time, an inline warning is shown and the submit button is disabled.

**Q7. What HTTP status codes does the REST API use?**  
A: `200 OK` (successful GET/PUT), `201 Created` (new booking), `400 Bad Request` (missing/invalid fields), `403 Forbidden` (CSRF failure), `404 Not Found` (resource missing), `409 Conflict` (slot already reserved).

### 24. APPLICATION SCREENSHOTS
> Screenshots of the following views are available in the `/static/screenshots/` directory (if present):
> - Login & Registration Page
> - Citizen Dashboard with Hall Map
> - Hall Detail Page
> - Booking Form (with live cost calculator)
> - My Bookings (with payment and cancel options)
> - Admin Control Panel (booking approval, maintenance scheduling)
> - Availability Calendar

---
*End of Report — Community Hall Booking & Management System | Academic Year 2026–2027*
