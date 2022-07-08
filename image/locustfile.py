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
        tasks.append(i)

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
        {"duration": 300, "users": 2, "spawn_rate": 2},
        {"duration": 600, "users": 7, "spawn_rate": 3},
        {"duration": 900, "users": 20, "spawn_rate": 5},
        {"duration": 1200, "users": 55, "spawn_rate": 5},
        {"duration": 1500, "users": 150, "spawn_rate": 8},
        {"duration": 1800, "users": 400, "spawn_rate": 15},
        {"duration": 2100, "users": 1100, "spawn_rate": 40},
        {"duration": 2400, "users": 3000, "spawn_rate": 80},
        {"duration": 2700, "users": 8100, "spawn_rate": 90},
        {"duration": 3000, "users": 22026, "spawn_rate": 180}
    ]
    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None
