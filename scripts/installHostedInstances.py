#!/usr/bin/python3

import click
import requests
import yaml
import os
import subprocess

def run_ansible(config, ansible_inventory_template, ansible_playbook, instance):
  # prepare the inventory.yml for this instance
  with open('tmp.inventory.yml', 'w') as f:
    f.write(ansible_inventory_template
      .replace('{{pac}}', instance['pacuser'])
      .replace('{{domain}}', instance['instance_url'].replace('https://', '').replace('http://', '').rstrip('/'))
      .replace('{{username}}', instance['prefix'] + instance['identifier'])
      .replace('{{password}}', instance['db_password'])
      .replace('{{SaasActivationPassword}}', instance['activation_token'])
      .replace('{{smtp_from}}', config['saasadmin']['smtp_from'])
      .replace('{{smtp_host}}', config['saasadmin']['smtp_host'])
      .replace('{{smtp_user}}', config['saasadmin']['smtp_user'])
      .replace('{{smtp_pwd}}', config['saasadmin']['smtp_pwd'])
      )

  # call ansible script to install/update instance
  process = subprocess.Popen(['ansible-playbook', '-i',
                  'tmp.inventory.yml', ansible_playbook],
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE)
  while True:
      output = process.stdout.readline()
      print(output.strip().decode())
      return_code = process.poll()
      if return_code is not None:
          print('RETURN CODE', return_code)
          # Process has finished, read rest of the output
          for output in process.stdout.readlines():
              print(output.strip().decode())
          for output in process.stderr.readlines():
              print(output.strip().decode())
          break

  # remove tmp.inventory.yml file
  os.remove('tmp.inventory.yml')

  return return_code


def setup_instances(config, url, admin_token, host_name, product_slug, ansible_path):
  params = dict(format='json', hostname=host_name, product=product_slug)
  resp = requests.get(url=url, params=params, headers={'Authorization': f'Token {admin_token}'})
  data = resp.json()

  if 'detail' in data:
    raise Exception(data['detail'])

  # print(data)

  with open(ansible_path + '/inventory-template.yml', 'r') as file:
    ansible_inventory_template = file.read()

  return_code = None
  for instance in data:
    if return_code:
      continue
    if instance['status'] == 'in_preparation':
      print(instance['identifier'])
      # print(instance)

      return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-install.yml', instance)

      # on success of ansible: change status to "new"
      if not return_code:
        return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-saas.yml', instance)
        if not return_code:
          params = dict(format='json', hostname=host_name, product=product_slug, instance_id=instance['identifier'], status='free')
          resp = requests.patch(url=url,
            params=params, headers={'Authorization': f'Token {admin_token}'})


@click.command()
@click.option('--product', default='randomapp', help='The shortname/slug of the product', prompt=True)
@click.option('--hostname', default='host0001.example.org', help='The hostname of the instances', prompt=True)
@click.option('--ansiblepath', default='../Hostsharing-Ansible-RandomApp', help='The path to the ansible playbooks', prompt=True)
@click.option('--admintoken', help='The token for access to the REST API of SaasAdmin')
@click.option('--url', help='The url for access to the REST API of SaasAdmin')
@click.option('--configfile', default='config.yaml', help='The config file to use')
def main(product, hostname, ansiblepath, admintoken, url, configfile):
    """run the ansible playbook for all specified instances"""

    # load from config.yml file
    with open(configfile, "r") as stream:
      try:
        config = yaml.safe_load(stream)
      except yaml.YAMLError as exc:
        print(exc)

    if admintoken is None:
      admintoken=config['saasadmin']['admin_token']
    if url is None:
      url=config['saasadmin']['url'] + '/api/v1/instances/'

    setup_instances(config, url, admintoken, hostname, product, ansiblepath)

if __name__ == '__main__':
    main()