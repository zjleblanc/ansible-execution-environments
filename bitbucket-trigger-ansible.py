import os
import requests
import jmespath

BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0/repositories'
API_HEADERS = {"Content-Type": "application/json"}
JSON_QUERY = 'values[].new.path'

def filter_ee(path: str) -> bool:
  folder = path.split('/')[0]
  return folder.startswith('ee') or folder.startswith('de')

def map_ee(path: str) -> str:
  return path.split('/')[0]

def process_changes(config: dict) -> set:
  url = f"{BITBUCKET_API_BASE_URL}/{config['workspace']}/{config['repo']}/diffstat/{config['commit']}"
  resp = requests.get(url, auth=(config['user'], config['app_pw']), headers=API_HEADERS)
  diff = resp.json()
  changed_files = jmespath.search(JSON_QUERY, diff)
  print("FILES CHANGED\n" + "\n".join(changed_files))
  return set(map(map_ee, filter(filter_ee, changed_files)))

def launch_ansible_jobs(ee, config) -> None:
  body = {
    "extra_vars": {
      "ee_name": ee,
      "commit_hash": config['commit']
    }
  }
  headers = {
    "Authorization": "Bearer " + config['aap_token'],
    **API_HEADERS
  }
  url = f"{config['aap_host']}/api/v2/job_templates/{config['aap_jt_id']}/launch/"
  r = requests.post(url=url, json=body,headers=headers)
  print("Launched Ansible Job to build " + ee)
  print("View job -> " + config['aap_host'] + '#/jobs/playbook/' + r.json().get('job', 'oops'))

def run(config):
  changed_ees = process_changes(config)
  for ee in changed_ees:
    launch_ansible_jobs(ee, config)
  if not len(changed_ees):
    print("No execution environment definitions require a new build, exiting...")

if __name__ == "__main__":
  config = {
    "workspace": os.environ.get('BITBUCKET_WORKSPACE'),
    "repo": os.environ.get('BITBUCKET_REPO_SLUG'),
    "commit": os.environ.get('BITBUCKET_COMMIT'),
    "user": os.environ.get('APP_USER'),
    "app_pw": os.environ.get('APP_PASSWORD'),
    "aap_host": os.environ.get('AAP_HOST'),
    "aap_token": os.environ.get('AAP_TOKEN'),
    "aap_jt_id": os.environ.get('AAP_JOB_TEMPLATE_ID')
  }
  run(config)