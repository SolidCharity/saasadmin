#!/usr/bin/python3

import click
import requests
import yaml
import os
import subprocess

# possible values for status; see core/model.py for the same constants
IN_PREPARATION, AVAILABLE, RESERVED, ASSIGNED, EXPIRED, TO_BE_REMOVED, REMOVED = \
    ('IN_PREPARATION', 'AVAILABLE', 'RESERVED', 'ASSIGNED', 'EXPIRED', 'TO_BE_REMOVED', 'REMOVED')


def run_ansible(config, ansible_inventory_template, ansible_playbook, instance):
    # prepare the inventory.yml for this instance
    with open('tmp.inventory.yml', 'w') as f:
        domain = (instance['instance_url']
            .replace('https://', '')
            .replace('http://', '')
            .rstrip('/')
            .replace('#Prefix', instance['prefix'])
            .replace('#Identifier', instance['identifier']))
        template_content = (ansible_inventory_template
            .replace('{{pac}}', instance['pacuser'])
            .replace('{{domain}}', domain)
            .replace('{{username}}', instance['prefix'] + instance['identifier'])
            .replace('{{password}}', instance['db_password'])
            .replace('{{SaasActivationPassword}}', instance['activation_token'])
            .replace('{{SaasInstanceStatus}}', instance['status'])
            .replace('{{smtp_from}}', config['saasadmin']['smtp_from'])
            .replace('{{smtp_host}}', config['saasadmin']['smtp_host'])
            .replace('{{smtp_user}}', config['saasadmin']['smtp_user'])
            .replace('{{smtp_pwd}}', config['saasadmin']['smtp_pwd']))
        f.write(template_content)

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
            if return_code:
                print(template_content)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip().decode())
            for output in process.stderr.readlines():
                print(output.strip().decode())
            break

    # remove tmp.inventory.yml file
    os.remove('tmp.inventory.yml')

    return return_code


def setup_instances(config, url, admin_token, host_name, product_slug, ansible_path, action):
    params = dict(format='json', hostname=host_name, product=product_slug, action=action)
    url += '/api/v1/instances/'
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

        print(instance['identifier'] + ' ' + instance['status'])
        # print(instance)

        if action == "install" and instance['status'] == IN_PREPARATION:
            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-install.yml', instance)
            if return_code:
                continue

            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-saas.yml', instance)
            if return_code:
                continue

            # on success of ansible: change status to "AVAILABLE"
            params = dict(format='json', hostname=host_name, product=product_slug, instance_id=instance['identifier'], status=AVAILABLE)
            resp = requests.patch(url=url,
                params=params, headers={'Authorization': f'Token {admin_token}'})

        elif action == "update" and instance['status'] != IN_PREPARATION and instance['status'] != REMOVED:
            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-install.yml', instance)
            if return_code:
                continue

            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-saas.yml', instance)
            if return_code:
                continue

        elif action == "remove" and instance['status'] == TO_BE_REMOVED:
            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-uninstall.yml', instance)
            if return_code:
                continue

            # on success of ansible: change status to "REMOVED"
            params = dict(format='json', hostname=host_name, product=product_slug, instance_id=instance['identifier'], status=REMOVED)
            resp = requests.patch(url=url,
                params=params, headers={'Authorization': f'Token {admin_token}'})


@click.command()
@click.option('--product', default='randomapp', help='The shortname/slug of the product', prompt=True)
@click.option('--hostname', default='host0001.example.org', help='The hostname of the instances', prompt=True)
@click.option('--ansiblepath', default='../Hostsharing-Ansible-RandomApp', help='The path to the ansible playbooks', prompt=True)
@click.option('--admintoken', help='The token for access to the REST API of SaasAdmin')
@click.option('--url', help='The url for access to the REST API of SaasAdmin')
@click.option('--configfile', default='config.yaml', help='The config file to use')
@click.option('--action', default='install', help='The action: install, update, remove')
def main(product, hostname, ansiblepath, admintoken, url, configfile, action):
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
        url=config['saasadmin']['url']

    if action not in ['install', 'remove', 'update']:
        print('action must be one of these values: install, remove, or update')
        exit(-1)

    setup_instances(config, url, admintoken, hostname, product, ansiblepath, action)

if __name__ == '__main__':
    main()
