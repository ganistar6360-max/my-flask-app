import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'community_hall.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='halls'")
    exists = cursor.fetchone()
    
    if not exists:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()

    # Migration: Ensure latitude, longitude, address, image_url exist
    cursor.execute("PRAGMA table_info(halls)")
    cols = [row[1] for row in cursor.fetchall()]
    
    if "latitude" not in cols:
        cursor.execute("ALTER TABLE halls ADD COLUMN latitude REAL DEFAULT 12.9716")
    if "longitude" not in cols:
        cursor.execute("ALTER TABLE halls ADD COLUMN longitude REAL DEFAULT 77.5946")
    if "address" not in cols:
        cursor.execute("ALTER TABLE halls ADD COLUMN address TEXT DEFAULT ''")
    if "image_url" not in cols:
        cursor.execute("ALTER TABLE halls ADD COLUMN image_url TEXT DEFAULT ''")
    
    # Update real coordinates, addresses, and authentic photos
    hall_updates = [
        (
            12.9716, 77.5946, 
            "Town Hall Circle, J.C. Road, Central Civic Ward No. 4",
            "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?auto=format&fit=crop&w=800&q=80",
            1
        ),
        (
            12.9299, 77.5824, 
            "11th Main Road, 4th T Block, Jayanagar Civic Complex",
            "https://images.unsplash.com/photo-1431540015161-0bf868a2d407?auto=format&fit=crop&w=800&q=80",
            2
        ),
        (
            12.9912, 77.5872, 
            "Palace Cross Road, Near High Court Annexe, Vasanth Nagar",
            "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80",
            3
        ),
        (
            13.0031, 77.5644, 
            "8th Main, 15th Cross, Near Public Library, Malleshwaram",
            "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=800&q=80",
            4
        ),
    ]
    for lat, lng, addr, img, hid in hall_updates:
        cursor.execute(
            "UPDATE halls SET latitude = ?, longitude = ?, address = ?, image_url = ? WHERE id = ?",
            (lat, lng, addr, img, hid)
        )

    conn.commit()
    conn.close()

# ----------------- USERS CRUD -----------------
def get_user_by_credentials(username, password):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_username_or_email(username, email):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_email(email):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(user) if user else None

def create_user(username, password, email, phone="", is_admin=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, email, phone, is_admin) VALUES (?, ?, ?, ?, ?)",
        (username, password, email, phone, is_admin)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def set_reset_token(email, token):
    conn = get_connection()
    conn.execute("UPDATE users SET reset_token = ? WHERE email = ?", (token, email))
    conn.commit()
    conn.close()

def get_user_by_reset_token(token):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE reset_token = ?", (token,)).fetchone()
    conn.close()
    return dict(user) if user else None

def update_password_with_token(token, new_password):
    conn = get_connection()
    conn.execute("UPDATE users SET password = ?, reset_token = NULL WHERE reset_token = ?", (new_password, token))
    conn.commit()
    conn.close()

def update_user_profile(user_id, phone, email):
    conn = get_connection()
    conn.execute("UPDATE users SET phone = ?, email = ? WHERE id = ?", (phone, email, user_id))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    users = conn.execute("SELECT id, username, email, phone, is_admin, created_at FROM users ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(u) for u in users]

# ----------------- HALLS CRUD -----------------
def get_all_halls():
    conn = get_connection()
    halls = conn.execute("SELECT * FROM halls ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(h) for h in halls]

def get_hall_by_id(hall_id):
    conn = get_connection()
    hall = conn.execute("SELECT * FROM halls WHERE id = ?", (hall_id,)).fetchone()
    conn.close()
    return dict(hall) if hall else None

def update_hall_status(hall_id, status):
    conn = get_connection()
    conn.execute("UPDATE halls SET status = ? WHERE id = ?", (status, hall_id))
    conn.commit()
    conn.close()

# ----------------- BOOKINGS CRUD & CONFLICT CHECK -----------------
def check_booking_conflict(hall_id, booking_date, start_time, end_time, exclude_id=None):
    conn = get_connection()
    query = """
        SELECT * FROM bookings 
        WHERE hall_id = ? 
          AND booking_date = ? 
          AND status IN ('approved', 'pending')
          AND NOT (end_time <= ? OR start_time >= ?)
    """
    params = [hall_id, booking_date, start_time, end_time]
    if exclude_id:
        query += " AND id != ?"
        params.append(exclude_id)
        
    conflict = conn.execute(query, params).fetchone()
    conn.close()
    return dict(conflict) if conflict else None

def create_booking(booking_ref, hall_id, user_id, username, email, booking_date, start_time, end_time, purpose, attendees, special_req, hours, total_cost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (
            booking_ref, hall_id, user_id, username, email, booking_date, 
            start_time, end_time, purpose, attendees, special_requirements, 
            hours, total_cost, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (booking_ref, hall_id, user_id, username, email, booking_date, start_time, end_time, purpose, attendees, special_req, hours, total_cost))
    booking_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return booking_id

def get_bookings_by_user(user_id):
    conn = get_connection()
    bookings = conn.execute("""
        SELECT b.*, h.name as hall_name, h.location as hall_location, h.address as hall_address, h.latitude, h.longitude 
        FROM bookings b
        JOIN halls h ON b.hall_id = h.id
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(b) for b in bookings]

def get_all_bookings():
    conn = get_connection()
    bookings = conn.execute("""
        SELECT b.*, h.name as hall_name, h.location as hall_location, h.latitude, h.longitude 
        FROM bookings b
        JOIN halls h ON b.hall_id = h.id
        ORDER BY b.created_at DESC
    """, ()).fetchall()
    conn.close()
    return [dict(b) for b in bookings]

def get_booking_by_id(booking_id):
    conn = get_connection()
    booking = conn.execute("""
        SELECT b.*, h.name as hall_name, h.location as hall_location, h.address as hall_address, h.latitude, h.longitude 
        FROM bookings b
        JOIN halls h ON b.hall_id = h.id
        WHERE b.id = ?
    """, (booking_id,)).fetchone()
    conn.close()
    return dict(booking) if booking else None

def update_booking_status(booking_id, status, reject_reason=None):
    conn = get_connection()
    conn.execute("UPDATE bookings SET status = ?, reject_reason = ? WHERE id = ?", (status, reject_reason, booking_id))
    conn.commit()
    conn.close()

def delete_booking(booking_id):
    conn = get_connection()
    conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

# ----------------- MAINTENANCE CRUD -----------------
def create_maintenance(hall_id, hall_name, maintenance_type, scheduled_date, end_date, reason):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO maintenance (hall_id, hall_name, maintenance_type, scheduled_date, end_date, reason, status)
        VALUES (?, ?, ?, ?, ?, ?, 'scheduled')
    """, (hall_id, hall_name, maintenance_type, scheduled_date, end_date, reason))
    mid = cursor.lastrowid
    conn.execute("UPDATE halls SET status = 'maintenance' WHERE id = ?", (hall_id,))
    conn.commit()
    conn.close()
    return mid

def get_all_maintenance():
    conn = get_connection()
    records = conn.execute("SELECT * FROM maintenance ORDER BY scheduled_date DESC").fetchall()
    conn.close()
    return [dict(r) for r in records]

def complete_maintenance(mid, hall_id):
    conn = get_connection()
    conn.execute("UPDATE maintenance SET status = 'completed' WHERE id = ?", (mid,))
    conn.execute("UPDATE halls SET status = 'available' WHERE id = ?", (hall_id,))
    conn.commit()
    conn.close()

# ----------------- ANALYTICS & DASHBOARD METRICS -----------------
def get_dashboard_metrics():
    conn = get_connection()
    total_bookings = conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    pending_bookings = conn.execute("SELECT COUNT(*) FROM bookings WHERE status = 'pending'").fetchone()[0]
    approved_bookings = conn.execute("SELECT COUNT(*) FROM bookings WHERE status = 'approved'").fetchone()[0]
    rejected_bookings = conn.execute("SELECT COUNT(*) FROM bookings WHERE status = 'rejected'").fetchone()[0]
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_revenue = conn.execute("SELECT SUM(total_cost) FROM bookings WHERE status = 'approved'").fetchone()[0] or 0.0
    
    hall_stats = conn.execute("""
        SELECT h.name, COUNT(b.id) as count 
        FROM halls h 
        LEFT JOIN bookings b ON h.id = b.hall_id 
        GROUP BY h.id
    """).fetchall()
    
    status_stats = conn.execute("""
        SELECT status, COUNT(*) as count FROM bookings GROUP BY status
    """).fetchall()
    
    conn.close()
    return {
        'total': total_bookings,
        'pending': pending_bookings,
        'approved': approved_bookings,
        'rejected': rejected_bookings,
        'users': total_users,
        'revenue': total_revenue,
        'hall_stats': [dict(h) for h in hall_stats],
        'status_stats': [dict(s) for s in status_stats]
    }
