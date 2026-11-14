from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColorRGB(0.3, 0.3, 0.3)
        # Header
        self.drawString(54, letter[1] - 36, "Community Hall Booking & Management System – Project Report")
        self.drawRightString(letter[0] - 54, letter[1] - 36, "Academic Project Report | 2026–2027")
        self.setStrokeColorRGB(0.7, 0.7, 0.7)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_str)
        self.drawString(54, 36, "Municipal Civic Infrastructure & Community Welfare Department")
        self.line(54, 48, letter[0] - 54, 48)
        self.restoreState()

def build_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), 'Community_Hall_Booking_System_Report.pdf')
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Community_Hall_Booking_System_Report.pdf")

    c = NumberedCanvas(pdf_path, pagesize=letter)
    width, height = letter

    def write_paragraph(c, text, x, y, max_width, font_name="Helvetica", font_size=10, leading=14):
        c.setFont(font_name, font_size)
        words = text.split()
        line = ""
        current_y = y
        for word in words:
            test_line = line + word + " "
            if c.stringWidth(test_line, font_name, font_size) > max_width:
                c.drawString(x, current_y, line.strip())
                line = word + " "
                current_y -= leading
                if current_y < 60:
                    c.showPage()
                    current_y = height - 70
            else:
                line = test_line
        if line:
            c.drawString(x, current_y, line.strip())
            current_y -= leading
        return current_y

    # --- PAGE 1: TITLE PAGE ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 100, "COMMUNITY HALL BOOKING & MANAGEMENT SYSTEM")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 125, "A Complete Software Development Life Cycle (SDLC) Project Report")
    c.drawCentredString(width / 2, height - 145, "Submitted in partial fulfillment of the requirements for the award of B.E. / B.Tech")

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 200, "ACADEMIC COMMUNITY PROJECT REPORT")

    c.setFont("Helvetica", 10)
    box_y = height - 420
    c.rect(100, box_y, width - 200, 180)
    c.drawString(120, box_y + 145, "Student Name: ____________________________________")
    c.drawString(120, box_y + 115, "USN / Register No.: ________________________________")
    c.drawString(120, box_y + 85, "Department: Information Science / Computer Engineering")
    c.drawString(120, box_y + 55, "Institution: Municipal Engineering Faculty")
    c.drawString(120, box_y + 25, "Academic Year: 2026–2027")

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, height - 480, "Technology Stack:")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 500, "Python • Flask • SQLite • HTML • CSS • Bootstrap 5 • Chart.js")

    c.showPage()

    # --- PAGE 2: CERTIFICATE ---
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 80, "CERTIFICATE")
    c.setFont("Helvetica", 10)

    cert_text = (
        "This is to certify that the project report entitled “Community Hall Booking & Management System” "
        "is a bonafide work carried out by student developer, bearing USN/Register No. _______________, "
        "in partial fulfillment of the academic requirements for the award of the degree of B.E. / B.Tech "
        "in Computer Science and Engineering during the academic year 2026–2027."
    )
    y = write_paragraph(c, cert_text, 54, height - 140, width - 108, "Helvetica", 11, 18)

    y -= 40
    c.drawString(54, y, "Role")
    c.drawString(220, y, "Name")
    c.drawString(420, y, "Signature")
    c.line(54, y - 5, width - 54, y - 5)

    y -= 40
    c.drawString(54, y, "Project Guide")
    c.drawString(220, y, "_______________________")
    c.drawString(420, y, "____________")

    y -= 50
    c.drawString(54, y, "Head of Department")
    c.drawString(220, y, "_______________________")
    c.drawString(420, y, "____________")

    y -= 50
    c.drawString(54, y, "External Examiner")
    c.drawString(220, y, "_______________________")
    c.drawString(420, y, "____________")

    c.showPage()

    # --- PAGE 3: ABSTRACT & TABLE OF CONTENTS ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, height - 80, "ABSTRACT")
    c.setFont("Helvetica", 10)
    abstract_text = (
        "The Community Hall Booking & Management System is a web-based application designed to automate "
        "municipal auditorium reservations, scheduling, approval workflows, facility maintenance, and payments. "
        "It replaces manual paper ledgers with a centralized SQLite database and role-based access control. "
        "Built using Python Flask and Bootstrap 5, the system features automated slot-overlap prevention (409 Conflict), "
        "an administrator control panel, a demo payment gateway (Card, UPI, Net Banking), and interactive Chart.js analytics."
    )
    y = write_paragraph(c, abstract_text, 54, height - 110, width - 108, "Helvetica", 10, 16)

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, y, "TABLE OF CONTENTS")
    c.setFont("Helvetica", 10)
    y -= 25

    toc_items = [
        "1. Introduction", "2. Problem Statement", "3. Objectives", "4. Scope",
        "5. Existing and Proposed System", "6. Software Development Life Cycle",
        "7. Feasibility Study", "8. Requirements Analysis", "9. System Analysis",
        "10. System Design", "11. Database Design", "12. System Architecture",
        "13. Implementation", "14. Source Code Overview", "15. Testing & Validation",
        "16. Security & Access Control", "17. Deployment", "18. Maintenance",
        "19. Limitations & Future Enhancements", "20. Conclusion & Viva-Voce Q&A"
    ]
    for item in toc_items:
        c.drawString(70, y, item)
        c.drawString(width - 100, y, "..." * 8)
        y -= 16
        if y < 60:
            c.showPage()
            y = height - 70

    c.showPage()

    # --- PAGE 4: INTRODUCTION & PROBLEM STATEMENT ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, height - 80, "1. INTRODUCTION")
    c.setFont("Helvetica", 10)
    intro = (
        "Municipal community halls and civic auditoriums serve as vital public infrastructure for cultural "
        "gatherings, citizen welfare meetings, educational workshops, weddings, and social assemblies. Traditionally, "
        "reserving these public assets required citizens to visit municipal offices in person, inspect physical ledger "
        "books, and undergo opaque approval processes vulnerable to scheduling conflicts."
    )
    y = write_paragraph(c, intro, 54, height - 110, width - 108, "Helvetica", 10, 16)

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, y, "2. PROBLEM STATEMENT")
    c.setFont("Helvetica", 10)
    prob = (
        "The conventional manual management of community halls presents severe challenges: scheduling conflicts "
        "and double-bookings on paper ledgers, lack of transparency in approval workflows, inconvenient physical "
        "visit requirements for reservation, unannounced facility maintenance closures, and the absence of centralized "
        "financial audit trails."
    )
    y = write_paragraph(c, prob, 54, y - 30, width - 108, "Helvetica", 10, 16)

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, y, "3. OBJECTIVES")
    c.setFont("Helvetica", 10)
    objs = [
        "• Centralize catalogue of municipal community facilities and tariffs.",
        "• Implement role-based access control (Citizen self-service vs. Municipal Officer admin).",
        "• Provide real-time schedule calendars with algorithmic slot-collision prevention (409 Conflict).",
        "• Enable citizens to submit booking applications and estimate tariffs dynamically.",
        "• Integrate a secure demo payment gateway simulating Card, UPI, and Net Banking.",
        "• Empower municipal administrators with approval/rejection workflows and maintenance scheduling."
    ]
    y -= 20
    for obj in objs:
        c.drawString(70, y, obj)
        y -= 18

    c.showPage()

    # --- PAGE 5: SYSTEM ARCHITECTURE & DATABASE DESIGN ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, height - 80, "4. SYSTEM ARCHITECTURE & DATABASE")
    c.setFont("Helvetica", 10)
    arch = (
        "The system follows a Model-View-Controller (MVC) architecture. Python Flask handles routing and business "
        "logic, SQLite provides robust relational data persistence, and Bootstrap 5 ensures responsive UI presentation."
    )
    y = write_paragraph(c, arch, 54, height - 110, width - 108, "Helvetica", 10, 16)

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(54, y, "Database Relational Schema:")
    y -= 20
    db_desc = [
        "• USERS: id (PK), username, password, email, phone, is_admin, reset_token, created_at",
        "• HALLS: id (PK), name, capacity, amenities, price_per_hour, description, location, address, lat, lng, image_url, status",
        "• BOOKINGS: id (PK), booking_ref (UK), hall_id (FK), user_id (FK), username, email, date, start_time, end_time, purpose, attendees, hours, total_cost, status, payment_status, transaction_id, reject_reason, created_at",
        "• MAINTENANCE: id (PK), hall_id (FK), hall_name, maintenance_type, scheduled_date, end_date, reason, status, created_at"
    ]
    for d in db_desc:
        c.drawString(70, y, d)
        y -= 18

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, y, "5. TESTING & VALIDATION")
    c.setFont("Helvetica", 10)
    test_text = (
        "Automated unit and integration test suites (test/test_api.py) were executed successfully, verifying "
        "hall APIs, booking creation, slot conflict prevention (409 Conflict), status updates, and telemetry analytics."
    )
    y = write_paragraph(c, test_text, 54, y - 30, width - 108, "Helvetica", 10, 16)

    c.showPage()

    # --- PAGE 6: CONCLUSION & VIVA VOCE ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, height - 80, "6. CONCLUSION & FUTURE ENHANCEMENTS")
    c.setFont("Helvetica", 10)
    conc = (
        "The Community Hall Booking & Management System successfully achieves its engineering objectives by digitizing "
        "public asset reservation workflows. By introducing algorithmic conflict prevention, role-based separation of "
        "portals, and a secure demo payment gateway, the system eliminates traditional bottlenecks and serves as an "
        "exemplary model of digital municipal governance."
    )
    y = write_paragraph(c, conc, 54, height - 110, width - 108, "Helvetica", 10, 16)

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, y, "7. VIVA-VOCE SAMPLE Q&A")
    c.setFont("Helvetica", 10)
    y -= 20

    qas = [
        "Q1: How does the system prevent booking overlaps?",
        "A1: Through check_booking_conflict in db.py, checking time interval intersections for approved/pending bookings.",
        "Q2: How are admin routes protected?",
        "A2: Using the @admin_required decorator verifying session.get('is_admin').",
        "Q3: What database does the project use?",
        "A3: SQLite3 for zero-configuration local execution, with schema support for MySQL 8.0.",
        "Q4: How does the demo payment gateway operate?",
        "A4: Simulates Card, UPI, and Net Banking, generating transaction IDs (TXN...) and marking status as paid."
    ]
    for qa in qas:
        c.drawString(70, y, qa)
        y -= 16

    c.save()

    # Copy to Desktop as well
    if os.path.exists(pdf_path):
        import shutil
        shutil.copy(pdf_path, desktop_path)
    print("PDF generated successfully at:", pdf_path, "and copied to Desktop.")

if __name__ == '__main__':
    build_pdf()
