### Locust Demo Project - Part 1
![](https://cdn2.hubspot.net/hubfs/208250/Blog_Images/locustjava1.png)
##### To see the Locust demo with Docker and Kubernetes see [Part 2](https://github.com/savvagen/locust-poc) 

## Writing tasks
1. Write your custom tasks using `TaskSet` class:
```
from locust import TaskSet

class UserScenario(TaskSet):

    ### Standart way to define tasks 
    # In this task get_specific_post() method will be executed 
    # 2-times rarely than get_post() method
    
    @task(1)
    def get_posts(self):
        self.client.get("/posts")
        
    @task(2)
    def get_specific_post(self):
        self.client.get("/posts/1")
        

```
2. Write tasks using predefined methods:

``` 
from locust import TaskSet

def get_posts(l):
    l.client.get("/posts")
    
def get_post(l):
    l.client.get("/posts/1")


class UserScenario(TaskSet):

    ### Another way to define tasks 
    # In this task get_post() method will be executed 
    # 2-times rarely than get_post() method
    
    tasks = {get_posts: 1, get_post: 2}


```

3. Setting up Locust Tests

``` 

class LoadTests(HttpLocust):
    host = "http://example.com"
    task_set = UserScenario
    min_wait = 1000
    max_wait = 2000
    stop_timeout = 30

```


### Running locust
```
locust --host https://jsonplaceholder.typicode.com -f locust_file.py WebsiteUser --no-web -c 5 -r 3 --run-time 30


locust --host https://jsonplaceholder.typicode.com \      # Base URL
       -f locust_file.py WebsiteUser \                    # file with tasks and Test instance
       --no-web \                                         # without web console
       --csv=report                                       # will generate a report in csv format
       -c 5 \                                             # specifies the number of Locust users to spawn
       -r 3 \                                             # specifies the hatch rate (number of users to spawn per second).
       --run-time 30 \                                    # if you want to specify the run time for a test
       --print-stats                                      # print statistics in the console


```


### Run tests from slaves


#### Init master
``` 
 locust -f clients/api/api_client.py --master --master-host=localhost
```
#### Connect 2 slaves
```
locust -f clients/api/api_client.py --slave --master-host=localhost
locust -f clients/api/api_client.py --slave --master-host=localhost

```

