import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import json
from locust import Locust, HttpLocust, TaskSet, task, TaskSequence, seq_task
from faker import Faker
from clients.services.posts_service import *
from models.post import Post

base_uri = "https://jsonplaceholder.typicode.com"


cwd = os.getcwd()
json_path = "{}/samples/json".format(cwd)
fake = Faker()


class PostsUserBehavior(TaskSequence):

    def setup(self):
        print("Test Sequence Started!")
        # Create all system objects - users / posts / comments etc.
        ## self.client.post("/users", {"id": 1, "userName": "tester"})
        ## self.login()

    def on_start(self):
        print("Scenario started!")
        self.client.post("/posts", json.dumps(Post(userId=1, id=1, title=fake.sentence(nb_words=5), body=fake.text())))

    @seq_task(1)
    @task(2)
    def get_all_posts(self):
        get_posts(self)

    @seq_task(2)
    @task(1)
    def open_post(self):
        get_post(self, 1)

    @seq_task(3)
    @task(2)
    def watch_post_comments(self):
        get_post_comments(self, 1)

    @seq_task(4)
    def patch_post(self):
        title = {"title": "Post Title Changed"}
        patch_post(self, 1, title)

    @seq_task(5)
    def update_post(self):
        post = Post(id=1, userId=1, title="Post Title Updated", body=fake.text())
        update_post(self, post)

    @seq_task(6)
    def delete_post(self):
        delete_post(self, 1)


    def on_stop(self):
        print("Scenario finished!")

    def teardown(self):
        print("Test Sequence Finished!")
        # Clear all system objects - users / posts / comments etc.
        ## self.client.delete("/users/1")
        ## self.logout()


class PostsLocustTests(HttpLocust):
    host = base_uri
    weight = 1
    stop_timeout = 30
    task_set = PostsUserBehavior
    min_wait = 100
    max_wait = 500

