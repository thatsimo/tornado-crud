# Basic CRUD Microservice in Python with Tornado

This is a basic CRUD microservice in Python with Tornado. It uses MongoDB as the database and Docker for local development.

## 1. Project Setup

Get the source code:

```bash
$ git clone https://github.com/thatsimo/tornado-crud
$ cd tornado-crud

$ tree .
.
├── README.md
├── app.py
├── docker-compose.yml
├── requirements.txt
├── run.py
├── tornado-crud.postman_collection.json
├── service
│   └── cats.py
└── test
    └── student_test.py
```

The directory `service` is for the source code of the service, and the directory `test` is for keeping the tests.

Setup Virtual Environment:

```bash
$ python3 -m venv .venv
$ source ./.venv/bin/activate
$ pip install --upgrade pip
$ pip3 install -r ./requirements.txt
```

Setup Local MongoDB:

```bash
$ docker-compose up -d
```

Setup Env Variables:

```bash
$ cp .env.example .env
```

You can run app and unit tests by either executing the tool directly or through `run.py` script. In each of the following, you can use either of the commands.

Server:

```bash
$ ./run.py server
```

Unit Tests:

```bash
$ ./run.py test
```

If you are able to run all these commands, your project setup has no error and you are all set for coding.

---

## 2. App

File `app.py` has business logic for CRUD operations for the students collection, it exposes routes to to serve various API endpoints, implemented through one Request Handler:

`StudentHandler`:

- `GET /students`: gets all students
- `POST /students`: create an entry in the students collection
- `GET /students/{id}`: get the student entry with given id
- `PUT /students/{id}`: update the student entry with given id
- `DELETE /students/{id}`: delete the student entry with given id

You cant test the API endpoints using the Postman collection `tornado-crud.postman_collection.json` in the root directory.
