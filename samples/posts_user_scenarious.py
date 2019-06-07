import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import json
from locust import Locust, HttpLocust, TaskSet, task
from faker import Faker
from clients.services.posts_service import *
from models.post import Post

base_uri = "https://jsonplaceholder.typicode.com"


cwd = os.getcwd()
json_path = "{}/samples/json".format(cwd)
fake = Faker()



class PostsWatcherBehavior(TaskSet):

    tasks = {get_posts: 1, get_post: 2}

    @task(3)
    def get_posts_comments(self):
        get_post_comments(self, 1)




class PostsEditorBehavior(TaskSet):
    tasks = {update_post: 1, get_post: 4, delete_post: 3}

    @task(3)
    def create_post(self):
        post = Post(userId=fake.random.randint(1, 10), id=fake.random.randint(1, 100), title=fake.sentence(nb_words=5), body=fake.text())
        resp = create_post(self, json.dumps(post.__dict__))
        assert resp.status_code == 200

    @task(2)
    def update_post(self):
        post = open("{}/updated_post.json".format(json_path))
        update_post(self, post)

    @task(2)
    def patch_post(self):
        title = {"title": "Hello There!"}
        patch_post(self, 1, title)



class PostsWatcher(HttpLocust):
    host = base_uri
    weight = 1
    stop_timeout = 30
    task_set = PostsWatcherBehavior
    min_wait = 100
    max_wait = 500


class PostsEditor(HttpLocust):
    host = base_uri
    weight = 3
    stop_timeout = 30
    task_set = PostsEditorBehavior
    min_wait = 500
    max_wait = 1000
