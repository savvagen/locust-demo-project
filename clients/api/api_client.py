import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, "../..")))


import requests
from requests import Session, Response
import time
from locust import Locust, TaskSet, events, task



def request(func):
    def request_wrapper(*args, **kwargs):
        r = None
        start_time = time.time()
        try:
            r = func(*args, **kwargs)
            assert r.status_code == 200
        except Exception as e:
            print(e)
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="api_call", name="GET {}".format(r.url),
                                        response_time=total_time,
                                        exception="Request failed. Response code matches: {}".format(r.status_code))
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="api_call", name="GET {}".format(r.url),
                                        response_time=total_time, response_length=0)
    return request_wrapper



def wrapped_command(func):
    def request_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="command", name=func.__name__,
                                        response_time=total_time,
                                        exception="Test failed.")
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="command", name=func.__name__,
                                        response_time=total_time, response_length=0)
    return request_wrapper



class APIClient:

    def __init__(self, base_uri):
        self.client = Session()
        self.base_uri = base_uri
        self.client.headers = {'Content-Type': 'application/json; charset=utf-8'}


    def GET(self, path):
        start_time = time.time()
        try:
            r = self.client.get("{}{}".format(self.base_uri, path))
            assert r.status_code == 200
        except Exception as e:
            print(e)
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="api_call", name="GET {}".format(path), response_time=total_time,
                                        exception="Request failed. Response code matches: {}".format(r.status_code))
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="api_call", name="GET {}".format(path), response_time=total_time,
                                        response_length=0)
        return r



    def get_posts(self):
        resp = self.GET("/posts")
        print(f"Request: {resp.url} | Status Code: {resp.status_code}")
        return resp

    def get_post(self, id=1):
        resp = self.GET("/posts/{}".format(id))
        print(f"Request: {resp.url} | Status Code: {resp.status_code}")
        return resp

    @request
    def get_posts_wrapped(self):
        resp = requests.get("{}/posts".format(self.base_uri))
        print(f"Request: {resp.url} | Status Code: {resp.status_code}")
        return resp

    @wrapped_command
    def create_post(self):
        resp = requests.post("{}/posts".format(self.base_uri), {"id": 1, "title": "foo", "body": "bar", "userId": 1})
        print(f"Request: {resp.url} | Status Code: {resp.status_code} | Response Body: {resp.text}")
        assert resp.status_code == 201
        assert resp.json()['title'] == "foo"
        return resp



class LocustRequests(Locust):

    def __init__(self):
        super(LocustRequests, self).__init__()
        self.client = APIClient(self.host)


class MyClientTest(LocustRequests):
    host = "https://jsonplaceholder.typicode.com"
    min_wait = 500
    max_wait = 1000

    class task_set(TaskSet):

        @task(1)
        def get_posts(self):
            self.client.get_posts_wrapped()

        @task(1)
        def open_post(self):
            self.client.get_post(1)

        @task(1)
        def create_post_record(self):
            self.client.create_post()

