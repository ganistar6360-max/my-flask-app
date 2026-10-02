-- ==============================================================
-- Community Hall Booking & Management System
-- Database Schema (Compatible with MySQL 8.0 & SQLite3)
-- SDG 11: Sustainable Cities & Communities | PO: 6
-- ==============================================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    is_admin INTEGER DEFAULT 0,
    reset_token VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS halls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL,
    amenities TEXT,
    price_per_hour REAL NOT NULL,
    description TEXT,
    location VARCHAR(100) DEFAULT 'Civic Center, Block 4',
    image_tag VARCHAR(50) DEFAULT 'auditorium',
    status VARCHAR(20) DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_ref VARCHAR(20) NOT NULL UNIQUE,
    hall_id INTEGER NOT NULL,
    user_id INTEGER,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    booking_date VARCHAR(20) NOT NULL,
    start_time VARCHAR(10) NOT NULL,
    end_time VARCHAR(10) NOT NULL,
    purpose TEXT NOT NULL,
    attendees INTEGER NOT NULL,
    special_requirements TEXT,
    hours REAL NOT NULL,
    total_cost REAL NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    reject_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hall_id) REFERENCES halls(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hall_id INTEGER NOT NULL,
    hall_name VARCHAR(100) NOT NULL,
    maintenance_type VARCHAR(50) NOT NULL,
    scheduled_date VARCHAR(20) NOT NULL,
    end_date VARCHAR(20) NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hall_id) REFERENCES halls(id)
);

-- Seed Initial Community Halls
INSERT INTO halls (id, name, capacity, amenities, price_per_hour, description, location, image_tag, status) VALUES
(1, 'Gandhi Memorial Auditorium', 500, 'Central AC, High-Def Projector, 7.1 Surround Sound, Green Rooms, Grand Stage, VIP Lounge', 2500.0, 'Premier community auditorium for cultural ceremonies, annual townhalls, public assemblies, and theatrical programs.', 'Civic Center, North Wing', 'auditorium', 'available'),
(2, 'Dr. APJ Abdul Kalam Conference Center', 120, 'Smart Board, Video Conferencing, High-Speed Wi-Fi, Podiums, Ergonomic Seating', 1000.0, 'Technologically advanced conference hall optimal for NGO seminars, community training, and youth workshops.', 'Technology Block, 2nd Floor', 'conference', 'available'),
(3, 'Heritage Banquet & Cultural Pavilion', 300, 'Air Conditioned, Commercial Catering Kitchen, Buffet Area, Ambient Lighting, Open Lawn Access', 1800.0, 'Versatile social and banquet hall designed for family weddings, festival celebrations, and community feasts.', 'Cultural Complex, East Wing', 'banquet', 'available'),
(4, 'Saraswati Community Reading & Seminar Room', 45, 'AC, Projector Screen, Whiteboard, Flexible Tables, Quiet Zone Setup', 500.0, 'Affordable micro-hall dedicated to local club meetings, student study groups, self-help group discussions.', 'Library Block, Ground Floor', 'mini', 'available');

-- Seed Default Admin User (username: admin, password: admin123, email: admin@communityhall.gov.in)
INSERT INTO users (id, username, password, email, phone, is_admin) VALUES
(1, 'admin', 'admin123', 'admin@communityhall.gov.in', '9876543210', 1);
