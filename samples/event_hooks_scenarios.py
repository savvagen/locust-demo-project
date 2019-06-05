import sys
import os

import locust

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, "../..")))

import json
import random
from locust import Locust, HttpLocust, TaskSet, task, events, web
from locust.events import EventHook
from faker import Faker
from clients.services.posts_service import *
from models.post import Post

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
                    title=fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
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


    request_success_stats = [list()]
    request_fail_stats = [list()]

    def __init__(self):
        locust.events.request_success += self.hook_request_success
        locust.events.request_failure += self.hook_request_fail
        locust.events.quitting += self.hook_locust_quit

    def hook_request_success(self, request_type, name, response_time, response_length):
        self.request_success_stats.append([name, request_type, response_time])

    def hook_request_fail(self, request_type, name, response_time, exception):
        self.request_fail_stats.append([name, request_type, response_time, exception])

    def hook_locust_quit(self):
        self.save_success_stats()

    def save_success_stats(self):
        import csv
        with open('success_req_stats.csv', 'wb') as csv_file:
            writer = csv.writer(csv_file)
            for value in self.request_success_stats:
                writer.writerow(value)




"""
Adding Web Resource with content-length statistics.
"""

"""
We need somewhere to store the stats.
On the master node stats will contain the aggregated sum of all content-lengths,
while on the slave nodes this will be the sum of the content-lengths since the
last stats report was sent to the master
"""
stats = {"content-length": 0}


def on_request_success(request_type, name, response_time, response_length):
    """
    Event handler that get triggered on every successful request
    """
    stats["content-length"] += response_length


def on_report_to_master(client_id, data):
    """
    This event is triggered on the slave instances every time a stats report is
    to be sent to the locust master. It will allow us to add our extra content-length
    data to the dict that is being sent, and then we clear the local stats in the slave.
    """
    data["content-length"] = stats["content-length"]
    stats["content-length"] = 0


def on_slave_report(client_id, data):
    """
    This event is triggered on the master instance when a new stats report arrives
    from a slave. Here we just add the content-length to the master's aggregated
    stats dict.
    """
    stats["content-length"] += data["content-length"]


# Hook up the event listeners
events.request_success += on_request_success
events.report_to_master += on_report_to_master
events.slave_report += on_slave_report


@web.app.route("/content-length")
def total_content_length():
    """
    Add a route to the Locust web app, where we can see the total content-length
    """
    return "Total content-length recieved: %i" % stats["content-length"]
