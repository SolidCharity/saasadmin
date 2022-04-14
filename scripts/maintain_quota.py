#!/usr/bin/python3

import click
import os
import random
import requests
import subprocess
import string
import socket
import yaml
from hs.admin.api import API

def convert_to_mb(value):
    if not value:
        return None
    if value.endswith('M'):
        return value[:-1]
    elif value.endswith('G'):
        return value[:-1] + '000'
    return value

def maintain_quota(config, url, admin_token, host_name, product_slug, pac_user, pac_pwd):
    params = dict(format='json', hostname=host_name, product=product_slug, action="quota")
    url += '/api/v1/instances/'
    resp = requests.get(url=url, params=params, headers={'Authorization': f'Token {admin_token}'})

    if resp.status_code != 200:
        print(resp)
        print(resp.text)
        return

    data = resp.json()

    if 'detail' in data:
        raise Exception(data['detail'])

    # print(data)

    api = API(cas=dict(uri='https://login.hostsharing.net/cas/v1/tickets',
                       service='https://config.hostsharing.net:443/hsar/backend'),
              credentials=dict(username=pac_user,
                               password=pac_pwd),
              backends=['https://config.hostsharing.net:443/hsar/xmlrpc/hsadmin',
                        'https://config2.hostsharing.net:443/hsar/xmlrpc/hsadmin'])

    return_code = None
    for instance in data:
        if return_code:
            continue

        print(instance['identifier'] + ' ' + instance['status'])
        #print(instance)


        # compare current quota with quota from saasadmin
        new_quota_softlimit = convert_to_mb(instance['quota_app'])
        new_storage_softlimit = convert_to_mb(instance['quota_storage'])
        if not new_quota_softlimit or not new_storage_softlimit:
            continue
        username = pac_user + '-' + instance['prefix'] + instance['identifier']
        current_hsuser = api.user.search(where={'name': username})[0]
        need_change = False
        if current_hsuser['quota_softlimit'] != new_quota_softlimit:
            need_change = True
        if current_hsuser['storage_softlimit'] != new_storage_softlimit:
            need_change = True
        new_quota_hardlimit = int(new_quota_softlimit) + 100
        new_storage_hardlimit = int(new_storage_softlimit) + 100

        # update quota if different
        if need_change:
            print(f"previously: {current_hsuser['quota_softlimit']} {current_hsuser['storage_softlimit']}")
            print(f"new: {new_quota_softlimit} {new_storage_softlimit}")
            api.user.update(where={'name': username}, set={'quota_softlimit': str(new_quota_softlimit),
                                                           'quota_hardlimit': str(new_quota_hardlimit),
                                                           'storage_softlimit': str(new_storage_softlimit),
                                                           'storage_hardlimit': str(new_storage_hardlimit),
                                                           })

        # TODO: check current usage
        # TODO: tell the customer if quota is full



@click.command()
@click.option('--product', default='randomapp', help='The shortname/slug of the product', prompt=True)
@click.option('--hostname', default='host0001.example.org', help='The hostname of the instances', prompt=True)
@click.option('--configfile', default='config.yaml', help='The config file to use')
def main(product, hostname, configfile):
    """check and maintain the quota for all specified instances"""

    # load from config.yml file
    with open(configfile, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    admintoken=config['saasadmin']['admin_token']
    url=config['saasadmin']['url']

    maintain_quota(config, url, admintoken, hostname, product, config['saasadmin']['pacuser'], config['saasadmin']['pacpwd'])

if __name__ == '__main__':
    main()
