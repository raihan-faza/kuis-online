from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    @task(1)
    def get_quiz(self):
        self.client.get("http://localhost:8080/Quiz")

    @task(1)
    def post_quiz(self):
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiVXNlcklkIjoiMTIzNCIsImlhdCI6MTUxNjIzOTAyMn0.u44ulqf1Wl1qCbs5KB5xialRuQ_JM1spwr5UJfM8MxM"
            }

        payload = {
            "Name": "LoadTest",
            "Desc": "LoadTest"
        }

        self.client.post("http://localhost:8080/Quiz", json=payload, headers=headers)

    

    @task(1)
    def post_user(self):
        payload = {
            "name": "String",
            "password": "String",
            "email": "String",
        }
        
        self.client.post("http://localhost:3000/users/signup", json=payload)

    @task(1)
    def post_lgoin(self):
        payload = {
            "email": "demian020277@gmail.com",
            "password": "123456",
        }
        
        self.client.post("http://localhost:3000/users/login", json=payload)

    @task(1)
    def notification(self):
        self.client.post("/notif/quiz/created")

    @task(1)
    def grading_1(self):
        self.client.post("http://localhost:8000/simulation")

    @task(1)
    def grading_2(self):
        self.client.post("http://localhost:8000/grade")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
