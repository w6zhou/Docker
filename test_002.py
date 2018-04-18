from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

    @task(1)
    def profile(self):
        self.client.get("/\?name\=caodi\&name2\=haha")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0