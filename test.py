from locust import User, HttpUser, task, between, tag
from subprocess import run, Popen, PIPE, STDOUT
import time


# class MyUser(User):
#
#     @tag('blah test')
#     @task
#     def my_task(self):
#         print("executing my_task")
#         time.sleep(1)
#         print("Completed executing my_task!")
#
#     @tag('podman_login')
#     @task
#     def podman_login_task(self):
#         username = "admin"
#         password = "password"
#         print("Running: Login with Podman username={}, password={}".format(username, password))
#
#         cmd = [
#             'podman',
#             'login',
#             '-u', username,
#             '-p', password,
#             '--tls-verify=false'
#         ]
#         p = Popen(cmd, stdout=PIPE)
#         p.communicate()
#         print("Return code is", p.returncode)
#         assert p.returncode == 0
#
#     @tag('podman_pull_image')
#     @task
#     def podman_pull_image(self):
#         print("Pulling image")
#         cmd = [
#             'podman',
#             'pull',
#             'quay.io/alecmerdler/bad-image:critical',
#             '--tls-verify=false'
#         ]
#         p = Popen(cmd, stdout=PIPE)
#         p.communicate()
#         print("Return code is", p.returncode)
#         assert p.returncode == 0
#
#     @tag('podman_tag_image')
#     @task
#     def podman_tag_image(self):
#         print("Taging image")
#         cmd = [
#             'podman',
#             'tag',
#             'quay.io/alecmerdler/bad-image:critical',
#             'localhost:8080/admin/bad-image:critical',
#         ]
#         p = Popen(cmd, stdout=PIPE)
#         p.communicate()
#         print("Return code is", p.returncode)
#         assert p.returncode == 0
#
#     @tag('podman_push_image')
#     @task
#     def podman_push_image(self):
#         print("Pushing image")
#         cmd = [
#             'podman',
#             'push',
#             '-u', 'admin',
#             '-p', 'password',
#             'localhost:8080/admin/bad-image:critical',
#             '--tls-verify', 'false'
#         ]
#         p = Popen(cmd, stdout=PIPE)
#         p.communicate()
#         print("Return code is", p.returncode)
#         assert p.returncode == 0
#
#     wait_time = between(0.5, 1)


class APIUser(HttpUser):

    def on_start(self):
        # print("Logging in")
        self.client.post('http://localhost:8080/', {'username': 'admin', 'password': 'password'})
        time.sleep(1)

    @tag('blah test')
    @task
    def my_task(self):
        # print("executing my_task")
        time.sleep(1)
        # print("Completed executing my_task!")


    @tag('repository')
    @task
    def login(self):
        # print("Calling Repository")
        self.client.get('http://localhost:8080/repository/')
        time.sleep(1)


    @tag('podman_tag_image')
    @task
    def podman_tag_image(self):
        username = "admin"
        password = "password"
        print("Running: Login with Podman username={}, password={}".format(username, password))

        cmd = [
            'podman',
            'login localhost:8080',
            '-u', username,
            '-p', password,
            '--tls-verify=false'
        ]
        p = Popen(cmd, stdout=PIPE)
        p.communicate()

        print("Pulling image")
        cmd = [
            'podman',
            'pull',
            'quay.io/alecmerdler/bad-image:critical',
            '--tls-verify=false'
        ]
        p = Popen(cmd, stdout=PIPE)
        p.communicate()

        print("Tagging image")
        cmd = [
            'podman',
            'tag',
            'quay.io/alecmerdler/bad-image:critical',
            'localhost:8080/admin/bad-image:critical',
        ]
        p = Popen(cmd, stdout=PIPE)
        p.communicate()

        print("Pushing image")
        cmd = [
            'podman',
            'push',
            'localhost:8080/admin/bad-image:critical',
            '--tls-verify=false',
            '--storage-opt', 'overlay.mount_program=/usr/bin/fuse-overlayfs',
            '--storage-driver', 'overlay'
        ]
        p = Popen(cmd, stdout=PIPE)
        p.communicate()
        print("Return code is", p.returncode)
        assert p.returncode == 0

    wait_time = between(0.5, 1)
