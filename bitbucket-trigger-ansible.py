import os
import requests
import jmespath

BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0/repositories'
JSON_QUERY = 'values[].old.path'

def filter_ee(path):
  folder = path.split('/')[0]
  return folder.startswith('ee') or folder.startswith('de')

def map_ee(path):
  return path.split('/')[0]

def process_changes(config) -> set:
  url = f"{BITBUCKET_API_BASE_URL}/{config['workspace']}/{config['repo']}/diffstat/{config['commit']}"
  headers = {
    "Content-Type": "application/json"
  }
  resp = requests.get(url, auth=(config['user'], config['app_pw']), headers=headers)
  diff = resp.json()
  changed_files = jmespath.search(JSON_QUERY, diff)
  print("FILES CHANGED\n" + "\n".join(changed_files))
  return set(map(map_ee, filter(filter_ee, changed_files)))

def run(config):
  changed_ees = process_changes(config)
  print("EXECUTION ENVIRONMENTS CHANGED\n" + "\n".join(changed_ees))

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