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


class ReadPosts(TaskSet):

    @task(20)
    def get_all_posts(self):
        get_posts(self)

    @task(1)
    class ReadPostSubtask(TaskSet):

       @task(1)
       def open_post(self):
           get_post(self, 1)

       @task(5)
       def watch_post_comments(self):
           get_post_comments(self, 1)


    @task(5)
    def stop(self):
        self.interrupt()



class EditPosts(TaskSet):

    @task(1)
    def patch_post(self):
        title = {"title": "Post Title Changed"}
        patch_post(self, 1, title)

    @task(10)
    def update_post(self):
        post = Post(id=1, userId=1, title="Post Title Updated", body=fake.text())
        update_post(self, post)


    @task(5)
    def stop(self):
        self.interrupt()



class MainUserBehavior(TaskSet):
    tasks = {
        ReadPosts: 1,
        EditPosts: 3
    }

    @task(5)
    def delete_posts(self):
        delete_post(self, 1)


class LocustFile(HttpLocust):
    host = base_uri
    stop_timeout = 120
    task_set = MainUserBehavior
    min_wait = 100
    max_wait = 500

