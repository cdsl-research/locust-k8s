from locust import events, LoadTestShape
from locust.runners import MasterRunner
import time
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("I'm on master node")
    else:
        print("I'm on a worker or standalone node")
from locust import HttpUser, task, constant
import csv
import random
tasks = []
with open(f"/mnt/sinario10.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for i in reader:
        tasks.append(i[1:])

class MyUser(HttpUser):

    @task
    def task(self):
        k = random.choice(tasks)
        l =  [x[2:-2].split("', '") for x in k if not x == '']
        for i in l:
            time.sleep(1)
            if i[0] == "GET":
                self.client.get(i[1])
            elif i[0] == "POST":
                self.client.post(i[1])
            elif i[0] == "HEAD":
                self.client.get(i[1])
            else:
                continue

class StagesShape(LoadTestShape):
    stages = [
        {"duration": 300, "users": 50, "spawn_rate": 50},
        {"duration": 600, "users": 100, "spawn_rate": 100},
        {"duration": 900, "users": 150, "spawn_rate": 150},
        {"duration": 1200, "users": 200, "spawn_rate": 200},
        {"duration": 1500, "users": 250, "spawn_rate": 250},
        {"duration": 1800, "users": 300, "spawn_rate": 300},
        {"duration": 2100, "users": 350, "spawn_rate": 350},
        {"duration": 2400, "users": 400, "spawn_rate": 400}
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None
