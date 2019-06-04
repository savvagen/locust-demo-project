###Run Load tests on the developer cluster without web console
```
locust --host http://l5d.k8s.us-west-2.dev.earnin.com -f locust_file.py WebsiteUser --no-web -c 5 -r 3 --run-time 30


locust --host http://l5d.k8s.us-west-2.dev.earnin.com \   # Base URL
       -f locust_file.py WebsiteUser \                    # file with tasks and Test instance
       --no-web \                                         # without web console
       --csv=report                                       # will generate a report in csv format
       -c 5 \                                             # specifies the number of Locust users to spawn
       -r 3 \                                             # specifies the hatch rate (number of users to spawn per second).
       -n 1000  \                                         # stop after 1000 requets
       --run-time 30 \                                    # if you want to specify the run time for a test
       --print-stats                                      # print statistics in the console


```


