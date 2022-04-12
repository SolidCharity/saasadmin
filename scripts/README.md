Scripts for maintaining instances for SaasAdmin
-----------------------------------------------

Sample calls:

    make quickstart
    . .venv/bin/activate

    export ACTION=install
    export PRODUCT_SLUG=kanboard
    export PRODUCT=Kanboard
    export CONFIG=test
    export HOSTNAME=hxy.hostsharing.net

    python3 maintain_instances.py --hostname $HOSTNAME \
        --product $PRODUCT_SLUG \
        --ansiblepath ../../hostsharing/ansible/Hostsharing-Ansible-$PRODUCT \
        --configfile config-$CONFIG.yaml \
        --action $ACTION

    python3 maintain_quota.py --hostname $HOSTNAME --product $PRODUCT_SLUG --configfile config-$CONFIG.yaml