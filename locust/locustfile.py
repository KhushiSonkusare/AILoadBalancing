from locust import HttpUser, task, between
import random
import string
import json

class LoadBalancerUser(HttpUser):
    wait_time = between(0.5, 3)

    def on_start(self):
        print("New user session started.")

    @task(3)
    def visit_home(self):
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed home page! Status: {response.status_code}")

    @task(6)
    def process_request(self):
        delay = random.choice([0.1, 0.5, 1, 2])
        request_type = random.choice(["standard", "heavy", "light"])
        
        params = {
            "delay": delay,
            "type": request_type
        }

        with self.client.get("/process", params=params, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Processing failed! Status: {response.status_code}")

    @task(1)
    def send_random_post_request(self):
        endpoint = "/submit"
        data = {
            "username": self.random_string(8),
            "email": f"{self.random_string(5)}@example.com",
            "amount": random.randint(1, 1000)
        }

        headers = {'Content-Type': 'application/json'}

        with self.client.post(endpoint, data=json.dumps(data), headers=headers, catch_response=True) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"POST failed! Status: {response.status_code}")

    @task(1)
    def simulate_invalid_request(self):
        endpoints = ["/process", "/non-existent"]
        endpoint = random.choice(endpoints)
        
        with self.client.get(endpoint + "?badparam=###", catch_response=True) as response:
            if response.status_code in [400, 404]:
                response.success()  # Expected failure
            else:
                response.failure(f"Expected 400/404 but got {response.status_code}")

    @staticmethod
    def random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))
