import unittest
from tornado.testing import AsyncHTTPTestCase, gen_test
import tornado.escape
from app import app

class TestStudentHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app

    @gen_test
    def test_get_students(self):
        response = yield self.http_client.fetch(self.get_url('/students'))
        self.assertEqual(response.code, 200)

    @gen_test
    def test_get_student_by_id(self):
        # Assuming you have a student ID in your database
        student_id = "6578a99fe5b7172f828ac94c"
        response = yield self.http_client.fetch(self.get_url(f'/students/{student_id}'))
        self.assertEqual(response.code, 200)

    @gen_test
    def test_post_student(self):
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
        self.assertTrue(res["fact"] != "")

    @gen_test
    def test_put_student(self):
        # Assuming you have a student ID in your database
        student_id = "6578a99fe5b7172f828ac94c"
        updated_data = {"name": "Updated Student", "age": 21}
        response = yield self.http_client.fetch(
            self.get_url(f'/students/{student_id}'),
            method='PUT',
            body=tornado.escape.json_encode(updated_data)
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body["name"], updated_data["name"])

    @gen_test
    async def test_delete_student(self):
        # Assuming you have a student ID in your database
        student_id = "6578a99fe5b7172f828ac94c"
        response = yield self.http_client.fetch(self.get_url(f'/students/{student_id}'), method='DELETE')
        self.assertEqual(response.code, 204)

if __name__ == '__main__':
    unittest.main()
