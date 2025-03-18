from locust import HttpUser, task, between
import random
import string
import json

class LoadBalancerUser(HttpUser):
    # Think time between actions (seconds)
    wait_time = between(0.5, 3)

    def on_start(self):
        """
        Called when a simulated user starts.
        Can be used to authenticate/login, etc.
        """
        print("New user session started.")

    @task(3)
    def visit_home(self):
        """
        Simulates visiting the home page.
        """
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed home page! Status: {response.status_code}")

    @task(6)
    def process_request(self):
        """
        Simulates processing requests with various delays and query params.
        """
        # Simulate query parameters for variety
        delay = random.choice([0.1, 0.5, 1, 2])  # Simulated processing time on server
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
        """
        Simulates sending data via POST (optional endpoint, for variety).
        """
        endpoint = "/submit"  # Assume you have a POST endpoint or use process if not
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
        """
        Sends invalid/malformed requests to test resilience.
        """
        endpoints = ["/process", "/non-existent"]
        endpoint = random.choice(endpoints)
        
        with self.client.get(endpoint + "?badparam=###", catch_response=True) as response:
            if response.status_code == 400 or response.status_code == 404:
                response.success()  # Expected failure
            else:
                response.failure(f"Expected 400/404 but got {response.status_code}")

    @staticmethod
    def random_string(length):
        """
        Generate random string for testing payloads.
        """
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))
