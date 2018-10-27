import base64
import json
import time
import threading
import untangle
import urllib.request
import yaml
from app.status import Status


class BambooMonitor(threading.Thread):
    def __init__(self, callbacks):
        super(BambooMonitor, self).__init__()
        with open('config.yml', 'r') as f:
            cfg = yaml.load(f)
            self.username = cfg['bamboo']['username']
            self.password = cfg['bamboo']['password']
            self.build_urls = cfg['bamboo']['build_urls']
            self.delay = cfg['bamboo']['delay']
        self.daemon = True
        self.callbacks = callbacks
    
    def _http_req(self, url):
        req = urllib.request.Request(url)
        encoded_credentials = base64.b64encode(('%s:%s' % (self.username, self.password)).encode('utf-8'))
        req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode('utf-8'))
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    
    def _get_build_xml(self, url):
        text = self._http_req(url)
        return untangle.parse(text)
    
    def _get_deployment_json(self, url):
        text = self._http_req(url)
        return json.loads(text)
    
    def _get_build_status(self, build):
        results = self._get_build_xml(build)
        first = results.children[0].results.children[0]
        return Status(
            name=first.plan['shortName'],
            status='success' if 'Successful' in first['state'] else 'error',
            in_progress=False if 'Finished' in first['lifeCycleState'] else True
        )
    
    def _get_deployment_status(self, deployment):
        results = self._get_deployment_json(deployment)
        first = results[0]['environmentStatuses'][0]
        return Status(
            name='Deploy %s' % (first['environment']['name']),
            status='success' if 'SUCCESS' in first['deploymentResult']['deploymentState'] else 'unknown',
            in_progress=False if 'FINISHED' in first['deploymentResult']['lifeCycleState'] else True
        )

    def update(self):
        try:
            build_urls = [url for url in self.build_urls if 'deploy' not in url]
            build_statuses = [self._get_build_status(build_url) for build_url in build_urls]
            deployment_urls = [url for url in self.build_urls if 'deploy' in url]
            deployment_statuses = [self._get_deployment_status(deployment_url) for deployment_url in deployment_urls]
            statuses = build_statuses + deployment_statuses
            for callback in self.callbacks:
                callback(statuses)
        except RuntimeError as e:
            print('An error occurred while monitoring Bamboo...')
            print(e)
    
    def run(self):
        while(True):
            self.update()
            time.sleep(self.delay)
