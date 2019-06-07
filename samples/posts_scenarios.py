import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import locust
from locust import Locust, HttpLocust, TaskSet, task
import random
from random import randint
import faker
from faker import Faker
from faker.providers import internet
from models.post import Post
import json



base_uri = "https://jsonplaceholder.typicode.com"
fake = Faker()


def get_posts(l):
    l.client.get("/posts")

def get_post(l, id):
    l.client.get("/posts/{}".format(id))

def create_post(l, payload):
    l.client.post("/posts", payload)

def update_post(l):
    l.client.post("/posts", {"id": 1, "title": "foo", "body": "bar", "userId": 1})

def patch_resource(l, id, payload):
    l.client.patch("/posts/{}".format(id), payload)

def delete_resource(l, id):
    l.client.delete("/posts/{}".format(id))






class UserPostsBehavior(TaskSet):

    tasks = {get_posts: 3, update_post: 2}

    @task(2)
    def get_post(self):
        get_post(self, random.randint(1, 7))

    @task(1)
    def create_post(self):
        create_post(self, {"title": "foo", "body": "bar", "userId": 1})

    @task(1)
    def create_fake_post(self):
        post = Post(userId=fake.random.randint(1, 10),
                    id=fake.random.randint(1, 100),
                    title=fake.sentence(nb_words=6,
                    variable_nb_words=True, ext_word_list=None),
                    body=fake.text())
        print("Post: " + json.dumps(post.__dict__))
        create_post(self, json.dumps(post.__dict__))



class WebUser(HttpLocust):
    host = base_uri
    task_set = UserPostsBehavior
    # wait_function = lambda self: random.expovariate(1) * 10
    # With the following locustfile, each user would wait between 0.5 and 1 second between tasks:
    min_wait = 100
    max_wait = 500


# Run different Users with: locust -f locust_file.py WebUserLocust MobileUserLocust
class WebUserLocust(HttpLocust):
    """Base hostname to swarm. i.e: http://127.0.0.1:1234"""
    host = base_uri
    """Probability of locust being chosen. The higher the weight, the greater is the chance of it being chosen."""
    weight = 3
    """Number of seconds after which the Locust will die. If None it won't timeout."""
    stop_timeout = 30
    task_set = UserPostsBehavior
    min_wait = 1000
    max_wait = 5000


class MobileUserLocust(HttpLocust):
    host = base_uri
    weight = 1
    task_set = UserPostsBehavior
    min_wait = 500
    max_wait = 1000
