from locust import HttpLocust, TaskSet, task
import faker
base_uri = "https://jsonplaceholder.typicode.com"




class UserPostsBehavior(TaskSet):


    def on_start(self):
        new_post = {
            "title": "foo",
            "body": "bar",
            "id": 2,
            "userId": 1
        }
        resp = self.client.post("/posts", new_post)
        resp.raise_for_status()


    @task(2)
    def get_posts(self):
        with self.client.get("/posts", catch_response=True, name="get_posts") as response:
            if response.status_code == 200:
                title = response.json()[0]['title']
                if title == "foo":
                    response.success()
                else:
                    response.failure(f'Got invalid post: {title}')
            else:
                response.failure(f'status code is {response.status_code}')

    @task(1)
    def get_post(self):
        with self.client.get("/posts/2", catch_response=True) as response:
            title = response.json()['title']
            if response.status_code == 200 & title == 'foo':
                response.success()
            else:
                response.failure(f'status code is {response.status_code}\n post title is {title}')


class WebUser(HttpLocust):
    host = base_uri
    task_set = UserPostsBehavior
    # wait_function = lambda self: random.expovariate(1) * 10
    # With the following locustfile, each user would wait between 0.5 and 1 second between tasks:
    min_wait = 100
    max_wait = 500

