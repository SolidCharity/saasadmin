SolidCharity SaasAdmin
======================

This is a tool to provide the administration for publishing your Software as a Service.

This software is brought to you by SolidCharity. We use it to publish OpenPetra as a Service.

WARNING: this is work in progress! We have just started. Stay tuned for the first version ready for production!


Feature Description
-------------------

- This is a light weight tool.
- Customers can sign up themselves, and get a free testing period first
- You can create instances of your software beforehand, and have them available for new customers
- We will integrate with one or multiple payment providers to manage recurring subscriptions.


Technology used
---------------

- This project is written in Python, using the Django Framework.
- We are using the Django REST framework (https://www.django-rest-framework.org/) to provide an API.
- We are using Skeleton (http://getskeleton.com/) for the CSS of the UI.


License
-------

See the LICENSE file in this directory.
We are using the BSD 3-Clause "New" or "Revised" License.


Development
-----------

- We recommend Debian or Ubuntu LTS or Fedora for development.

To get started:

```
apt-get install git make
git clone https://github.com/SolidCharity/saasadmin.git
cd saasadmin
make install
make runserver
```


What we still need to do
------------------------

- Still a lot todo. This is not ready for use yet.
