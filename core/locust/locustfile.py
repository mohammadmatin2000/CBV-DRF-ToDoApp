from locust import HttpUser, task, between

# ======================================================================================================================
class QuickstartUser(HttpUser):
    def on_start(self):
        response=self.client.post("/accounts/api/v1/jwt/token/create/",data={
          "email": "mohammadmatin13872008@gmail.com",
          "password": "m1387m2008m"
        }).json()
        self.client.headers = {"Authorization": f"Bearer {response['accessToken']}"}

    @task
    def task_list(self):
        self.client.get("/api/v1/tasks/")

# ======================================================================================================================