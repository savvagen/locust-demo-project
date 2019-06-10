### Run Load tests without web console
```
locust --host https://jsonplaceholder.typicode.com -f locust_file.py WebsiteUser --no-web -c 5 -r 3 --run-time 30


locust --host https://jsonplaceholder.typicode.com \      # Base URL
       -f locust_file.py WebsiteUser \                    # file with tasks and Test instance
       --no-web \                                         # without web console
       --csv=report                                       # will generate a report in csv format
       -c 5 \                                             # specifies the number of Locust users to spawn
       -r 3 \                                             # specifies the hatch rate (number of users to spawn per second).
       -n 1000  \                                         # stop after 1000 requets
       --run-time 30 \                                    # if you want to specify the run time for a test
       --print-stats                                      # print statistics in the console


```


### Run tests from slaves


#### Init master
``` 
 locust -f clients/api/api_client.py --slave --master-host=localhost
```
#### Connect 2 slaves
```
locust -f clients/api/api_client.py --slave --master-host=localhost
locust -f clients/api/api_client.py --slave --master-host=localhost

```
Then start testing