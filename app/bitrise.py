import json
import time
import threading
import urllib.request
import yaml
from app.status import Status


class BitriseMonitor(threading.Thread):
    def __init__(self, callbacks):
        super(BitriseMonitor, self).__init__()
        with open('config.yml', 'r') as f:
            cfg = yaml.load(f)
            self.token = cfg['bitrise']['token']
            self.build_urls = cfg['bitrise']['build_urls']
            self.delay = cfg['bitrise']['delay']
        self.daemon = True
        self.callbacks = callbacks
    
    def _get_build_json(self, url):
        req = urllib.request.Request(url=url)
        req.add_header('Authorization', 'token %s' % self.token)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    
    def _get_build_status(self, build):
        results = self._get_build_json(build)
        first = results['data'][0]
        return Status(
            name='Android' if 'android' in first['stack_identifier'] else 'iOS',
            status='success' if 'success' in first['status_text'] else 'unknown' if 'error' not in first['status_text'] else 'error',
            in_progress=True if 'in-progress' in first['status_text'] else False
        )

    def update(self):
        try:
            statuses = [self._get_build_status(build_url) for build_url in self.build_urls]
            for callback in self.callbacks:
                callback(statuses)
        except RuntimeError as e:
            print('An error occurred while monitoring Bitrise...')
            print(e)
    
    def run(self):
        while(True):
            self.update()
            time.sleep(self.delay)
