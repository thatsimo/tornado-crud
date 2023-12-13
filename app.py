import tornado.web
import os
import tornado.ioloop
import tornado.escape
from tornado.gen import coroutine
import motor.motor_tornado
from dotenv import load_dotenv
from bson import ObjectId
import service.cats as cats

load_dotenv()
client = motor.motor_tornado.MotorClient(os.environ["MONGODB_URL"])
db = client.college

class StudentHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self, student_id=None):
        if student_id is not None:
            student = yield self.settings["db"]["students"].find_one({"_id": student_id})
            if student is not None:
                return self.write(student)
            else:
                raise tornado.web.HTTPError(404)
        else:
            students = yield self.settings["db"]["students"].find().to_list(1000)
            return self.write({"students": students})

    @coroutine
    def post(self):
        student = tornado.escape.json_decode(self.request.body)
        student["_id"] = str(ObjectId())
        fact = yield cats.get_cat_fact()
        student["fact"] = tornado.escape.json_decode(fact)["fact"]

        new_student = yield self.settings["db"]["students"].insert_one(student)
        created_student = yield self.settings["db"]["students"].find_one(
            {"_id": new_student.inserted_id}
        )

        self.set_status(201)
        return self.write(created_student)

    @coroutine
    def put(self, student_id):
        student = tornado.escape.json_decode(self.request.body)
        yield self.settings["db"]["students"].update_one(
            {"_id": student_id}, {"$set": student}
        )

        updated_student = yield self.settings["db"]["students"].find_one(
                {"_id": student_id}
            )
        
        if updated_student is not None:
            return self.write(updated_student)

        raise tornado.web.HTTPError(404)

    @coroutine
    def delete(self, student_id):
        delete_result = yield db["students"].delete_one({"_id": student_id})

        if delete_result.deleted_count == 1:
            self.set_status(204)
            return self.finish()

        raise tornado.web.HTTPError(404)

app = tornado.web.Application(
    [
        (r"/students/(?P<student_id>\w+)", StudentHandler),
        (r"/students", StudentHandler),
    ],
    db=db
)   

if __name__=="__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()