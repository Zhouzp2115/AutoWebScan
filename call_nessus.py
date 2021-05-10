import requests
import json
import sys
from getDomain import *


class Nessus:

    def __init__(self):
        self.accessKey = 'your nessus accessKey'
        self.secretKey = 'your nessus secretKey'
        self.ip = 'nessus server ip'
        self.port = nessus server ip port(8834 default)
        self.header = {
            'X-ApiKeys': 'accessKey={accesskey};secretKey={secretkey}'.format(accesskey=self.accessKey,
                                                                              secretkey=self.secretKey),
            "Content-Type": "application/json"}

    def get_scan_list(self):
        url = "https://{}:{}/scans".format(self.ip, self.port)
        response = requests.get(url, headers=self.header, verify=False)
        if response.status_code == 200:
            result = json.loads(response.text)
            result = result['scans']
            return result

    def get_nessus_template_uuid(self, template_name):
        url = "https://{}:{}/editor/scan/templates".format(self.ip, self.port)
        response = requests.get(url, headers=self.header, verify=False)
        templates = json.loads(response.text)['templates']

        for template in templates:
            if template['name'] == template_name:
                return template['uuid']

        print('do not find ' + template_name + ' in follow templates')
        for template in templates:
            print(template['name'])
            print(template['uuid'])
        exit(1)

    def creat_task(self, ip):
        uuid = self.get_nessus_template_uuid('advanced')
        data = {"uuid": uuid, "settings": {"name": 'scan_' + str(ip),
                                           "enabled": True,
                                           "text_targets": ip,
                                           "agent_group_id": []}}

        url = "https://{ip}:{port}/scans".format(ip=self.ip, port=self.port)
        response = requests.post(url, headers=self.header, data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
                                 verify=False)
        if response.status_code == 200:
            tasks = json.loads(response.text)
            # the server return current created task id
            return tasks['scan']['id']
        else:
            print('create scan task failed')
            tasks = json.loads(response.text)
            print(tasks)
            exit(1)

    def launch(self, id):
        url = "https://{ip}:{port}/scans/{scan_id}/launch".format(ip=self.ip, port=self.port, scan_id=id)
        response = requests.post(url, verify=False, headers=self.header)
        if response.status_code != 200:
            print('launch task ' + str(id) + ' failed')
            exit(1)


if __name__ == '__main__':
    file_name = sys.argv[1]
    domains, ips = getIpDomain(file_name)

    nessus = Nessus()
    for ip in ips:
        id = nessus.creat_task(ip)
        nessus.launch(id)
        print('create task ' + str(ip))
