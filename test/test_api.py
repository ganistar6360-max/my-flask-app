import unittest
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import db

class CommunityHallTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.init_db()

    def test_01_get_halls_api(self):
        response = self.app.get('/api/halls')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['count'], 4)
        print("[PASS] test_01_get_halls_api")

    def test_02_get_single_hall_api(self):
        response = self.app.get('/api/halls/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], 1)
        print("[PASS] test_02_get_single_hall_api")

    def test_03_create_and_conflict_booking_api(self):
        unique_date = f"2027-{uuid.uuid4().hex[:4]}-01"
        payload = {
            "hall_id": 1,
            "user_id": 1,
            "username": "tester",
            "email": "tester@example.com",
            "booking_date": unique_date,
            "start_time": "10:00",
            "end_time": "14:00",
            "purpose": "Unit Test Community Gathering",
            "attendees": 100
        }
        response = self.app.post('/api/bookings', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        bid = data['booking_id']
        print(f"[PASS] test_03_create_booking_api (Booking ID: {bid})")

        # Conflict test on same date and overlapping slot
        conflict_payload = {
            "hall_id": 1,
            "user_id": 2,
            "username": "conflict_user",
            "email": "conflict@example.com",
            "booking_date": unique_date,
            "start_time": "11:00",
            "end_time": "15:00",
            "purpose": "Conflicting event",
            "attendees": 50
        }
        c_res = self.app.post('/api/bookings', data=json.dumps(conflict_payload), content_type='application/json')
        self.assertEqual(c_res.status_code, 409)
        print("[PASS] test_04_booking_conflict_prevention")

        # Update status
        up_res = self.app.put(f'/api/bookings/{bid}', data=json.dumps({"status": "approved"}), content_type='application/json')
        self.assertEqual(up_res.status_code, 200)
        print("[PASS] test_05_update_booking_status_api")

    def test_06_analytics_api(self):
        response = self.app.get('/api/analytics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('total', data['data'])
        self.assertIn('revenue', data['data'])
        print("[PASS] test_06_analytics_api")

if __name__ == '__main__':
    unittest.main()
