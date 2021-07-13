Wordpress plugin for SaasAdmin
==============================

This plugin displays the pricing table, in multiple languages.

It offers authentication with the SaasAdmin website, and allows the customer to manage his/her account.

Installation
============

# create symbol links:

```
ln -s ~/saasadmin/wordpress_plugin wp-content/plugins/saasadmin
ln -s ~/saasadmin/apps/api api
ln -s ~/saasadmin/apps/frontend app
ln -s ~/saasadmin/static static
```

Configuration
=============

In Wordpress, create the following pages, with this content: `[saasadmin]`

These are the perma links for the pages:
* register
* confirm
* sign-in
* pwd_reset
* account
* pricing
* payment
* product
* logout
