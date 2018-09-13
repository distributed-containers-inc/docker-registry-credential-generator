import hashlib
import os
import secrets
import string
import subprocess

import sys

import time
from kubernetes import client, config
from kubernetes.client.rest import ApiException


def _err_write(msg):
  sys.stderr.write(str(msg))
  sys.stderr.write(os.linesep)
  sys.stderr.flush()

def main():
  pod_namespace = os.getenv('MY_POD_NAMESPACE')
  if pod_namespace is None:
    _err_write('MY_POD_NAMESPACE is not set, see example/deploy.yaml')
    exit(1)

  htpasswd_secret_name = os.getenv('HTPASSWD_SECRET_NAME')
  if htpasswd_secret_name is None:
    _err_write('HTPASSWD_SECRET_NAME is not set, see example/deploy.yaml')
    exit(1)

  password_secret_name = os.getenv('PASSWORD_SECRET_NAME')
  if password_secret_name is None:
    _err_write('PASSWORD_SECRET_NAME is not set, see example/deploy.yaml')
    exit(1)

  registry_username = os.getenv('REGISTRY_USERNAME')
  if registry_username is None:
    _err_write('REGISTRY_USERNAME is not set, see example/deploy.yaml')
    exit(1)

  config.load_incluster_config()

  alphabet = string.ascii_letters + string.digits
  password = ''.join(secrets.choice(alphabet) for i in range(20))

  out = subprocess.check_output(['htpasswd', '-bn', registry_username, password]).decode('utf-8')

  v1 = client.CoreV1Api()

  try:
    v1.create_namespaced_secret(
      namespace=pod_namespace,
      body=client.V1Secret(
        string_data= {'auth': out},
        metadata={
          'name': htpasswd_secret_name,
        }
      )
    )

    v1.create_namespaced_secret(
      namespace=pod_namespace,
      body=client.V1Secret(
        string_data={'password': password},
        metadata={
          'name': password_secret_name
        }
      )
    )
    print('Successfully created {} and {} secrets.'.format(
        htpasswd_secret_name, password_secret_name
    ))
  except ApiException as e:
    if e.reason == 'Conflict':
      print('Secret(s) already exist. Will not do anything.')
    else:
      raise
  while True:
    time.sleep(1000000)