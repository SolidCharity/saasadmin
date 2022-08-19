#!/usr/bin/python3

import click
import os
import random
import requests
import subprocess
import string
import socket
import yaml

# possible values for status; see core/model.py for the same constants
IN_PREPARATION, READY, AVAILABLE, RESERVED, ASSIGNED, EXPIRED, TO_BE_REMOVED, REMOVED = \
    ('IN_PREPARATION', 'READY', 'AVAILABLE', 'RESERVED', 'ASSIGNED', 'EXPIRED', 'TO_BE_REMOVED', 'REMOVED')

def random_password(length):
    # get random password with letters, and digits
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def run_ansible(config, ansible_inventory_template, ansible_playbook, instance):
    # prepare the inventory.yml for this instance
    with open('tmp.inventory.yml', 'w') as f:
        domain = (instance['instance_url']
            .replace('https://', '')
            .replace('http://', '')
            .rstrip('/')
            .replace('#Prefix', instance['prefix'])
            .replace('#Identifier', instance['identifier']))
        if not instance['custom_domain']:
            instance['custom_domain'] = domain
        template_content = (ansible_inventory_template
            .replace('{{identifier}}', instance['identifier'])
            .replace('{{hostname}}', instance['hostname'])
            .replace('{{hostname_ip}}', socket.gethostbyname(instance['hostname']))
            .replace('{{pac}}', instance['pacuser'])
            .replace('{{pac_ip}}', socket.gethostbyname(instance['pacuser'] + '.hostsharing.net'))
            .replace('{{port1}}', str(instance['first_port']))
            .replace('{{port2}}', str(instance['first_port'] + 1))
            .replace('{{port3}}', str(instance['first_port'] + 2))
            .replace('{{port4}}', str(instance['first_port'] + 3))
            .replace('{{initial_password}}', instance['initial_password'])
            .replace('{{password1}}', instance['password1'])
            .replace('{{password2}}', instance['password2'])
            .replace('{{django_secret_key}}', instance['django_secret_key'])
            .replace('{{domain}}', domain)
            .replace('{{custom_domain}}', instance['custom_domain'])
            .replace('{{dbms_type}}', instance['dbms_type'])
            .replace('{{username}}', instance['prefix'] + instance['identifier'])
            .replace('{{password}}', instance['db_password'])
            .replace('{{SaasActivationPassword}}', instance['activation_token'])
            .replace('{{SaasInstanceStatus}}', instance['status'])
            .replace('{{RandomPassword}}', random_password(16))
            .replace('{{RandomMinute}}', str(random.randint(5,55)))
            .replace('{{Random32DigitsLetters1}}', random_password(32))
            .replace('{{Random32DigitsLetters2}}', random_password(32))
            .replace('{{Random32DigitsLetters3}}', random_password(32))
            .replace('{{Random32DigitsLetters4}}', random_password(32))
            .replace('{{smtp_from}}', config['saasadmin']['smtp_from'])
            .replace('{{smtp_host}}', config['saasadmin']['smtp_host'])
            .replace('{{smtp_port}}', config['saasadmin']['smtp_port'])
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


def setup_instances(config, url, admin_token, host_name, product_slug, ansible_path, action, limit_to_status):

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

        if limit_to_status is not None and instance['status'] != limit_to_status:
            continue

        print(instance['identifier'] + ' ' + instance['status'])
        # print(instance)

        if action == "init" and instance['status'] == IN_PREPARATION:
            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-init.yml', instance)
            if return_code:
                continue

        if action == "install" and instance['status'] == IN_PREPARATION:
            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-install.yml', instance)
            if return_code:
                continue

            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-saas.yml', instance)
            if return_code:
                continue

            # on success of ansible: change status to "READY"
            params = dict(format='json', hostname=host_name, product=product_slug, instance_id=instance['identifier'], status=READY)
            resp = requests.patch(url=url,
                params=params, headers={'Authorization': f'Token {admin_token}'})

        elif action == "update" and instance['status'] != IN_PREPARATION and instance['status'] != REMOVED:
            return_code = run_ansible(config, ansible_inventory_template, ansible_path + '/playbook-update.yml', instance)
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

        elif action == "check":
            canRead = False
            try:
                resp = requests.get(url=instance['instance_url'])
                if resp.status_code != 200:
                    print(resp)
                else:
                    canRead = True
            except:
                print("Cannot read %s" % (instance['identifier'],))
                canRead = False

            if instance['status'] == READY and canRead:
                # on success of check: change status to "AVAILABLE"
                params = dict(format='json', hostname=host_name, product=product_slug, instance_id=instance['identifier'], status=AVAILABLE)
                resp = requests.patch(url=url,
                    params=params, headers={'Authorization': f'Token {admin_token}'})


@click.command()
@click.option('--product', default='randomapp', help='The shortname/slug of the product', prompt=True)
@click.option('--hostname', default='host0001.example.org', help='The hostname of the instances', prompt=True)
@click.option('--ansiblepath', default='../Hostsharing-Ansible-RandomApp', help='The path to the ansible playbooks', prompt=True)
@click.option('--admintoken', help='The token for access to the REST API of SaasAdmin')
@click.option('--url', help='The url for access to the REST API of SaasAdmin')
@click.option('--configfile', default='config.yaml', help='The config file to use')
@click.option('--action', default='install', help='The action: init, install, update, remove, check')
@click.option('--limit_to_status', default=None, help='Only consider instances with this status, eg. READY')
def main(product, hostname, ansiblepath, admintoken, url, configfile, action, limit_to_status):
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

    if action not in ['init', 'install', 'remove', 'update', 'check']:
        print('action must be one of these values: install, remove, update or check')
        exit(-1)

    setup_instances(config, url, admintoken, hostname, product, ansiblepath, action, limit_to_status)

if __name__ == '__main__':
    main()
