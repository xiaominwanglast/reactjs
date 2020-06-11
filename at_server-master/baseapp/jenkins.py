import json, re, requests, time

from django.conf import settings

host = settings.TEST_JENKINS_HOST
username = settings.TEST_JENKINS_USERNAME
api_token = settings.TEST_JENKINS_API_TOKEN


pmd_host = settings.ONLINE_JENKINS_HOST
pmd_username = settings.ONLINE_JENKINS_USERNAME
pmd_api_token = settings.ONLINE_JENKINS_API_TOKEN

class Jenkins:
    @classmethod
    def get_views(cls):
        response = requests.get(f'{host}/api/json', auth=(username, api_token))
        return [view.get('name') for view in response.json().get('views')]

    @classmethod
    def get_jobs_by_views(cls, view_name):
        response = requests.get(f'{host}/view/{view_name}/api/json', auth=(username, api_token))
        return [view.get('name') for view in response.json().get('jobs')]

    @classmethod
    def get_jobs(cls):
        jobs = []
        for view_name in Jenkins.get_views():
            if view_name == 'all' or view_name == '代码质量扫描':
                continue
            jobs += ([[job, view_name] for job in Jenkins.get_jobs_by_views(view_name)])
        return jobs

    @classmethod
    def get_service_branch(cls, job_name):
        response = requests.get(
            f'{host}/job/{job_name}/descriptorByName/net.uaznia.lukanus.hudson.plugins.gitparameter.GitParameterDefinition/fillValueItems?param=BRANCH_NAME',
            auth=(username, api_token))
        return [view.get('value') for view in response.json().get('values')]

    @classmethod
    def get_jobs_by_views(cls, view_name):
        response = requests.get(f'{host}/view/{view_name}/api/json', auth=(username, api_token))
        return [view.get('name') for view in response.json().get('jobs')]

    @classmethod
    def get_pmd_result(cls, job_name):
        response = requests.get(f'{pmd_host}/job/{job_name}/lastSuccessfulBuild/pmdResult/api/json',
                                auth=(pmd_username, pmd_api_token))
        return {"numberOfHighPriorityWarnings": response.json().get('numberOfHighPriorityWarnings'),
                "numberOfNormalPriorityWarnings": response.json().get('numberOfNormalPriorityWarnings')}

    @classmethod
    def get_pmd_result_test(cls, job_name):
        response = requests.get(f'{host}/job/{job_name}/lastSuccessfulBuild/pmdResult/api/json',
                                auth=(username, api_token))
        return {"numberOfHighPriorityWarnings": response.json().get('numberOfHighPriorityWarnings'),
                "numberOfNormalPriorityWarnings": response.json().get('numberOfNormalPriorityWarnings')}

    @classmethod
    def get_pmd_last_result_test(cls, job_name):
        response = requests.get(f'{host}/job/{job_name}/lastBuild/pmdResult/api/json',
                                auth=(username, api_token))
        return {"numberOfHighPriorityWarnings": response.json().get('numberOfHighPriorityWarnings'),
                "numberOfNormalPriorityWarnings": response.json().get('numberOfNormalPriorityWarnings')}

    @classmethod
    def get_pmd_jobnum_result_test(cls, num, job_name):
        response = requests.get(f'{host}/job/{job_name}/{num}/pmdResult/api/json',
                                auth=(username, api_token))
        print(response.json())
        return {"numberOfHighPriorityWarnings": response.json().get('numberOfHighPriorityWarnings'),
                "numberOfNormalPriorityWarnings": response.json().get('numberOfNormalPriorityWarnings')}

    @classmethod
    def get_pmd_jobnum_status_test(cls, num, job_name):
        response = requests.get(f'{host}/job/{job_name}/{num}/api/json',
                                auth=(username, api_token))
        return response.json().get('result'),response.json().get('building')


if __name__ == '__main__':
    print(time.time())
    Jenkins.get_service_branch("platform_customerservice")
    print(time.time())
