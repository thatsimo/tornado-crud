import unittest
from tornado.testing import AsyncHTTPTestCase, gen_test
import tornado.escape
from app import app

class StudentTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return app

    @gen_test
    def test_crud_students(self):
        # Creating a student POST /students, expect to get the created student back
        student_data ={"name": "Test Student", "age": 20} 
        response = yield self.http_client.fetch(
            self.get_url('/students'),
            method='POST',
            body=tornado.escape.json_encode(student_data)
        )
        self.assertEqual(response.code, 201)
        res = tornado.escape.json_decode(response.body)
        self.assertEqual(res["name"], student_data["name"])
        self.assertEqual(res["age"], student_data["age"])
        self.assertTrue(res["_id"] != "")
        self.assertTrue(res["fact"] != "")

        student_id = res["_id"]

        # Getting student by _id GET /students/{_id}, expect to get the created student back
        response = yield self.http_client.fetch(self.get_url(f'/students/{student_id}'))
        self.assertEqual(response.code, 200)

        # Getting all students GET /students, expect to get a list of students and the created student in the list
        response = yield self.http_client.fetch(self.get_url('/students'))
        self.assertEqual(response.code, 200)
        res = tornado.escape.json_decode(response.body)
        filteredRes = list(filter(lambda student: student["_id"] == student_id, res["students"]))
        self.assertTrue(len(filteredRes) > 0)

        # Updating student PUT /students/{_id}, expect to get the updated student back
        updated_data = {"name": "Updated Student", "age": 21}
        response = yield self.http_client.fetch(
            self.get_url(f'/students/{student_id}'),
            method='PUT',
            body=tornado.escape.json_encode(updated_data)
        )
        self.assertEqual(response.code, 200)
        res = tornado.escape.json_decode(response.body)
        self.assertEqual(res["name"], updated_data["name"])

        # Deleting student DELETE /students/{_id}, expect to get a 204 response
        response = yield self.http_client.fetch(self.get_url(f'/students/{student_id}'), method='DELETE')
        self.assertEqual(response.code, 204)

        # Getting all students GET /students, expect to get a list of students without the created student in the list
        response = yield self.http_client.fetch(self.get_url('/students'))
        self.assertEqual(response.code, 200)
        res = tornado.escape.json_decode(response.body)
        filteredRes = list(filter(lambda student: student["_id"] == student_id, res["students"]))
        self.assertTrue(len(filteredRes) == 0)

if __name__ == '__main__':
    unittest.main()
