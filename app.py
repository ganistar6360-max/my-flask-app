from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail, Message
import re
import uuid
from datetime import datetime
from functools import wraps
import db

app = Flask(__name__)
app.secret_key = "community_hall_secret_key_vtu_sdg11"

# Initialize SQLite database and default seed data
db.init_db()

# Optional Flask-Mail configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "ganistar6360@gmail.com"
app.config["MAIL_PASSWORD"] = "ifxh fypd ysyv iqjs"
mail = Mail(app)

def send_notification_email(recipient, subject, body):
    try:
        msg = Message(subject, sender="ganistar6360@gmail.com", recipients=[recipient])
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[Mail Notification Skipped / Network Offline]: {e}")
        return False

# Access Control Decorators
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "loggedin" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "loggedin" not in session:
            return redirect(url_for("login"))
        if not session.get("is_admin"):
            flash("Administrator privileges required to access the Admin Panel.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated

# ----------------- AUTHENTICATION ROUTES -----------------
@app.route("/")
def index():
    if "loggedin" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "loggedin" in session:
        return redirect(url_for("dashboard"))
    msg = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = db.get_user_by_credentials(username, password)
        if user:
            session["loggedin"] = True
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user["email"]
            session["phone"] = user.get("phone", "")
            session["is_admin"] = bool(user["is_admin"])
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            msg = "Invalid username or password. Please verify your credentials."
    return render_template("login.html", msg=msg)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    success = False
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        existing = db.get_user_by_username_or_email(username, email)
        if existing:
            if existing["username"].lower() == username.lower():
                msg = f"Username '{username}' is already taken! If this is your account, please sign in."
            else:
                msg = f"Email '{email}' is already registered! If this is your account, please sign in."
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Please provide a valid email address!"
        elif not re.match(r"^[A-Za-z0-9_]{3,20}$", username):
            msg = "Username must be 3-20 characters and contain letters/numbers/underscore."
        elif len(password) < 4:
            msg = "Password must be at least 4 characters long."
        else:
            # Check if this is the first user registered (grant admin)
            all_users = db.get_all_users()
            is_admin = 1 if len(all_users) == 0 else 0
            db.create_user(username, password, email, phone, is_admin)
            success = True
            msg = "Registration successful! You can now log in."
    return render_template("register.html", msg=msg, success=success)

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    msg = ""
    success = False
    token = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        user = db.get_user_by_email(email)
        if user:
            token = str(uuid.uuid4())
            db.set_reset_token(email, token)
            reset_link = url_for("reset_password", token=token, _external=True)
            sent = send_notification_email(
                email,
                "Password Reset - Community Hall System",
                f"Hello {user['username']},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore."
            )
            success = True
            if sent:
                msg = f"A password reset link has been dispatched to {email}."
            else:
                msg = f"Reset token generated! (Offline simulation): Link is {reset_link}"
        else:
            msg = "No account found associated with that email address."
    return render_template("forgot_password.html", msg=msg, success=success, token=token)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = db.get_user_by_reset_token(token)
    if not user:
        flash("Invalid or expired reset token.", "danger")
        return redirect(url_for("login"))
    msg = ""
    if request.method == "POST":
        new_password = request.form.get("password", "").strip()
        if len(new_password) < 4:
            msg = "Password must be at least 4 characters long."
        else:
            db.update_password_with_token(token, new_password)
            flash("Your password has been successfully reset! Please sign in.", "success")
            return redirect(url_for("login"))
    return render_template("reset_password.html", token=token, msg=msg)

# ----------------- MAIN DASHBOARD & HALLS -----------------
@app.route("/dashboard")
@login_required
def dashboard():
    halls_list = db.get_all_halls()
    my_bookings = db.get_bookings_by_user(session["user_id"])
    metrics = db.get_dashboard_metrics()
    
    # Recent bookings
    all_bookings = db.get_all_bookings()
    recent_bookings = all_bookings[:5] if session.get("is_admin") else my_bookings[:5]
    
    return render_template(
        "dashboard.html",
        halls=halls_list,
        my_bookings=my_bookings,
        recent_bookings=recent_bookings,
        metrics=metrics
    )

@app.route("/halls")
@login_required
def view_halls():
    query = request.args.get("q", "").lower()
    capacity_filter = request.args.get("capacity", "")
    all_halls = db.get_all_halls()
    
    filtered_halls = []
    for h in all_halls:
        match_query = (not query) or (query in h["name"].lower()) or (query in h["description"].lower())
        match_capacity = True
        if capacity_filter == "small":
            match_capacity = h["capacity"] <= 50
        elif capacity_filter == "medium":
            match_capacity = 50 < h["capacity"] <= 200
        elif capacity_filter == "large":
            match_capacity = h["capacity"] > 200
            
        if match_query and match_capacity:
            filtered_halls.append(h)
            
    return render_template("halls.html", halls=filtered_halls, query=query, capacity=capacity_filter)

@app.route("/hall/<int:hall_id>")
@login_required
def hall_detail(hall_id):
    hall = db.get_hall_by_id(hall_id)
    if not hall:
        flash("Hall not found.", "danger")
        return redirect(url_for("view_halls"))
    
    # Amenities split
    amenities = [a.strip() for a in hall["amenities"].split(",") if a.strip()]
    return render_template("hall_detail.html", hall=hall, amenities=amenities)

# ----------------- BOOKING SYSTEM -----------------
@app.route("/book/<int:hall_id>", methods=["GET", "POST"])
@login_required
def book_hall(hall_id):
    hall = db.get_hall_by_id(hall_id)
    if not hall:
        flash("Hall not found.", "danger")
        return redirect(url_for("view_halls"))

    msg = ""
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if request.method == "POST":
        booking_date = request.form.get("booking_date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        purpose = request.form.get("purpose", "").strip()
        attendees = int(request.form.get("attendees", 1))
        special_req = request.form.get("special_requirements", "").strip()

        # Validation
        if not booking_date or not start_time or not end_time or not purpose:
            msg = "Please fill in all required fields."
        elif booking_date < today_str:
            msg = "Booking date cannot be in the past!"
        elif start_time >= end_time:
            msg = "Start time must be before End time!"
        elif attendees > hall["capacity"]:
            msg = f"Attendees ({attendees}) exceed maximum capacity of {hall['capacity']} seats!"
        else:
            # Check availability conflict
            conflict = db.check_booking_conflict(hall_id, booking_date, start_time, end_time)
            if conflict:
                msg = f"Hall is already booked on {booking_date} between {conflict['start_time']} and {conflict['end_time']}!"
            else:
                fmt = "%H:%M"
                t1 = datetime.strptime(start_time, fmt)
                t2 = datetime.strptime(end_time, fmt)
                hours = round((t2 - t1).seconds / 3600.0, 2)
                if hours < 1.0:
                    hours = 1.0
                total_cost = round(hours * hall["price_per_hour"], 2)
                booking_ref = "BK-" + uuid.uuid4().hex[:8].upper()

                db.create_booking(
                    booking_ref=booking_ref,
                    hall_id=hall_id,
                    user_id=session["user_id"],
                    username=session["username"],
                    email=session["email"],
                    booking_date=booking_date,
                    start_time=start_time,
                    end_time=end_time,
                    purpose=purpose,
                    attendees=attendees,
                    special_req=special_req,
                    hours=hours,
                    total_cost=total_cost
                )

                # Send confirmation email
                send_notification_email(
                    session["email"],
                    f"Booking Request Submitted: {booking_ref}",
                    f"Dear {session['username']},\n\nYour booking request for {hall['name']} on {booking_date} ({start_time} - {end_time}) has been registered!\nReference: {booking_ref}\nEstimated Cost: Rs. {total_cost}\n\nCurrent Status: PENDING (Admin approval required)\n\nThank you for choosing Community Hall Services."
                )

                flash(f"Booking request submitted successfully! Reference: {booking_ref}", "success")
                return redirect(url_for("my_bookings"))

    return render_template("book_hall.html", hall=hall, msg=msg, today=today_str)

@app.route("/my-bookings")
@login_required
def my_bookings():
    user_bookings = db.get_bookings_by_user(session["user_id"])
    return render_template("my_bookings.html", bookings=user_bookings)

@app.route("/cancel-booking/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    b = db.get_booking_by_id(booking_id)
    if b and b["user_id"] == session["user_id"]:
        if b["status"] in ["pending", "approved"]:
            db.update_booking_status(booking_id, "cancelled", "Cancelled by user")
            flash("Booking cancelled successfully.", "info")
        else:
            flash("Cannot cancel a booking that is already completed or rejected.", "warning")
    return redirect(url_for("my_bookings"))

# ----------------- AVAILABILITY CALENDAR -----------------
@app.route("/availability")
@login_required
def availability():
    all_halls = db.get_all_halls()
    selected_hall = request.args.get("hall_id", type=int)
    all_bookings = db.get_all_bookings()
    
    if selected_hall:
        display_bookings = [b for b in all_bookings if b["hall_id"] == selected_hall and b["status"] in ["approved", "pending"]]
    else:
        display_bookings = [b for b in all_bookings if b["status"] in ["approved", "pending"]]
        
    return render_template(
        "availability.html",
        halls=all_halls,
        selected_hall=selected_hall,
        bookings=display_bookings
    )

# ----------------- ADMIN PANEL -----------------
@app.route("/admin")
@admin_required
def admin_panel():
    all_bookings = db.get_all_bookings()
    all_users = db.get_all_users()
    all_halls = db.get_all_halls()
    maintenance_records = db.get_all_maintenance()
    metrics = db.get_dashboard_metrics()
    
    return render_template(
        "admin.html",
        bookings=all_bookings,
        users=all_users,
        halls=all_halls,
        maintenance=maintenance_records,
        metrics=metrics
    )

@app.route("/admin/approve/<int:booking_id>", methods=["POST"])
@admin_required
def approve_booking(booking_id):
    booking = db.get_booking_by_id(booking_id)
    if booking:
        db.update_booking_status(booking_id, "approved")
        send_notification_email(
            booking["email"],
            f"Booking Approved! Reference: {booking['booking_ref']}",
            f"Dear {booking['username']},\n\nYour booking for {booking['hall_name']} on {booking['booking_date']} from {booking['start_time']} to {booking['end_time']} has been APPROVED.\nReference: {booking['booking_ref']}\nTotal: Rs. {booking['total_cost']}\n\nWe look forward to hosting your community event."
        )
        flash(f"Booking {booking['booking_ref']} approved successfully!", "success")
    return redirect(url_for("admin_panel"))

@app.route("/admin/reject/<int:booking_id>", methods=["POST"])
@admin_required
def reject_booking(booking_id):
    reason = request.form.get("reason", "Hall unavailable for requested slot").strip()
    booking = db.get_booking_by_id(booking_id)
    if booking:
        db.update_booking_status(booking_id, "rejected", reason)
        send_notification_email(
            booking["email"],
            f"Booking Request Update: {booking['booking_ref']}",
            f"Dear {booking['username']},\n\nWe regret to inform you that your booking request {booking['booking_ref']} for {booking['hall_name']} on {booking['booking_date']} could not be approved.\n\nReason: {reason}\n\nPlease check the availability schedule for alternative slots."
        )
        flash(f"Booking {booking['booking_ref']} rejected.", "info")
    return redirect(url_for("admin_panel"))

@app.route("/admin/schedule-maintenance", methods=["POST"])
@admin_required
def schedule_maintenance():
    hall_id = int(request.form.get("hall_id"))
    hall = db.get_hall_by_id(hall_id)
    maintenance_type = request.form.get("maintenance_type", "General Inspection")
    scheduled_date = request.form.get("scheduled_date")
    end_date = request.form.get("end_date")
    reason = request.form.get("reason", "Routine upkeep")

    if hall and scheduled_date and end_date:
        db.create_maintenance(hall_id, hall["name"], maintenance_type, scheduled_date, end_date, reason)
        flash(f"Maintenance scheduled for {hall['name']}.", "success")
    return redirect(url_for("admin_panel"))

@app.route("/admin/complete-maintenance/<int:mid>/<int:hall_id>", methods=["POST"])
@admin_required
def complete_maintenance(mid, hall_id):
    db.complete_maintenance(mid, hall_id)
    flash("Maintenance marked as completed and hall status restored to available.", "success")
    return redirect(url_for("admin_panel"))

@app.route("/admin/update-hall-status/<int:hall_id>", methods=["POST"])
@admin_required
def update_hall_status(hall_id):
    new_status = request.form.get("status", "available")
    db.update_hall_status(hall_id, new_status)
    flash("Hall status updated.", "success")
    return redirect(url_for("admin_panel"))

# ----------------- USER PROFILE -----------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = db.get_user_by_id(session["user_id"])
    msg = ""
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Please provide a valid email address."
        else:
            db.update_user_profile(session["user_id"], phone, email)
            session["email"] = email
            session["phone"] = phone
            user = db.get_user_by_id(session["user_id"])
            flash("Profile updated successfully!", "success")
    return render_template("profile.html", user=user, msg=msg)

# ----------------- REST API ENDPOINTS (SECTION 7 OF SYLLABUS) -----------------
# Meets: GET, POST, PUT, DELETE, JSON, HTTP Status Codes, Postman Basics
@app.route("/api/halls", methods=["GET"])
def api_get_halls():
    halls_list = db.get_all_halls()
    return jsonify({"success": True, "count": len(halls_list), "data": halls_list}), 200

@app.route("/api/halls/<int:hall_id>", methods=["GET"])
def api_get_hall(hall_id):
    hall = db.get_hall_by_id(hall_id)
    if not hall:
        return jsonify({"success": False, "error": "Hall not found"}), 404
    return jsonify({"success": True, "data": hall}), 200

@app.route("/api/bookings", methods=["GET", "POST"])
def api_bookings():
    if request.method == "GET":
        user_id = request.args.get("user_id", type=int)
        if user_id:
            bookings_data = db.get_bookings_by_user(user_id)
        else:
            bookings_data = db.get_all_bookings()
        return jsonify({"success": True, "count": len(bookings_data), "data": bookings_data}), 200
        
    elif request.method == "POST":
        data = request.get_json() or {}
        required = ["hall_id", "booking_date", "start_time", "end_time", "purpose", "attendees"]
        for field in required:
            if field not in data:
                return jsonify({"success": False, "error": f"Missing required parameter: {field}"}), 400
                
        hall = db.get_hall_by_id(data["hall_id"])
        if not hall:
            return jsonify({"success": False, "error": "Specified hall does not exist"}), 404
            
        conflict = db.check_booking_conflict(data["hall_id"], data["booking_date"], data["start_time"], data["end_time"])
        if conflict:
            return jsonify({"success": False, "error": "Slot already reserved by another booking"}), 409
            
        fmt = "%H:%M"
        try:
            t1 = datetime.strptime(data["start_time"], fmt)
            t2 = datetime.strptime(data["end_time"], fmt)
            hours = max(round((t2 - t1).seconds / 3600.0, 2), 1.0)
        except Exception:
            return jsonify({"success": False, "error": "Invalid time format (use HH:MM)"}), 400
            
        total_cost = round(hours * hall["price_per_hour"], 2)
        booking_ref = "API-" + uuid.uuid4().hex[:8].upper()
        
        bid = db.create_booking(
            booking_ref=booking_ref,
            hall_id=data["hall_id"],
            user_id=data.get("user_id", 1),
            username=data.get("username", "api_user"),
            email=data.get("email", "api@communityhall.gov.in"),
            booking_date=data["booking_date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            purpose=data["purpose"],
            attendees=data["attendees"],
            special_req=data.get("special_requirements", ""),
            hours=hours,
            total_cost=total_cost
        )
        return jsonify({
            "success": True,
            "message": "Booking created successfully",
            "booking_id": bid,
            "booking_ref": booking_ref,
            "total_cost": total_cost,
            "status": "pending"
        }), 201

@app.route("/api/bookings/<int:booking_id>", methods=["GET", "PUT", "DELETE"])
def api_booking_detail(booking_id):
    booking = db.get_booking_by_id(booking_id)
    if not booking:
        return jsonify({"success": False, "error": "Booking not found"}), 404
        
    if request.method == "GET":
        return jsonify({"success": True, "data": booking}), 200
        
    elif request.method == "PUT":
        data = request.get_json() or {}
        new_status = data.get("status")
        if new_status not in ["pending", "approved", "rejected", "cancelled"]:
            return jsonify({"success": False, "error": "Invalid status value"}), 400
        reason = data.get("reason", "")
        db.update_booking_status(booking_id, new_status, reason)
        return jsonify({"success": True, "message": f"Booking status updated to {new_status}"}), 200
        
    elif request.method == "DELETE":
        db.delete_booking(booking_id)
        return jsonify({"success": True, "message": f"Booking {booking_id} deleted permanently"}), 200

@app.route("/api/analytics", methods=["GET"])
def api_analytics():
    metrics = db.get_dashboard_metrics()
    return jsonify({"success": True, "data": metrics}), 200

# Error Handlers
@app.errorhandler(404)
def not_found(e):
    return render_template("login.html", msg="404: The requested page was not found."), 404

if __name__ == "__main__":
    # Host on 0.0.0.0 so phone can connect via Wi-Fi IP address
    app.run(host="0.0.0.0", port=5000, debug=True)
