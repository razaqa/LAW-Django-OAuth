import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    def __init__(self, parent):
        super(QuickstartUser, self).__init__(parent)
        self.token = 'd806ce6701589615f0b702546b05fa0b1fbf94a350a0c6bfc5437b1ef577aa64a4a2df4e4b51bf85'

    wait_time = between(1, 2.5)
    
    @task(1)
    def token(self):
        with self.client.post('/oauth/token', data=
            {
                'client_id': '9f615230-b039-4997-8cc4-4b610e1e7a8b',
                'client_secret': 'c3b41fbc-129b-4f12-8e33-8ff4dcd65d24',
                'username': 'razaqa',
                'password': 'lawsukses',
                'grant_type': 'password'
            }
        ) as response:
            if response != None:
                self.token = response.json()['access_token']
    
    @task(15)
    def resource(self):
        self.client.post('/oauth/resource', headers={'authorization': 'Bearer ' + self.token})
