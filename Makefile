VENV := . .venv/bin/activate &&

all:
	@echo "help:"
	@echo "  make quickstart_debian"
	@echo "  make quickstart_fedora"
	@echo "  make runserver"
	@echo "  make clean"

clean:
	rm -Rf .venv
	rm -f db.sqlite3
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

install:
	if [ -f /etc/lsb-release ]; then make quickstart_debian; else make quickstart_fedora; fi

quickstart_debian: debian_packages quickstart

debian_packages:
	(dpkg -l | grep python3-dev) || (sudo apt update && sudo apt install python3-venv python3-dev gettext -y)
	
quickstart_fedora: fedora_packages quickstart

fedora_packages:
	(rpm -qa | grep python3-devel) || sudo dnf install python3-devel

quickstart_without_demodb: create_venv pip_packages create_db create_superuser
	@echo 
	@echo =====================================================================================
	@echo Installation has finished successfully
	@echo Run '"'make runserver'"' in order to start the server and access it through one of the following IP addresses
	@ip addr | sed 's/\/[0-9]*//' | awk '/inet / {print "http://" $$2 ":8000/"}'
	@echo For the first login, the user is '"'admin'"', and the password is '"'admin'"'

quickstart: quickstart_without_demodb demo_db

create_superuser:
	${VENV} echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

pip_packages:
	${VENV} pip install -r requirements.txt

create_venv:
	python3 -m venv .venv

create_db:
	if [ ! -f saasadmin/settings_local.py ]; then cp saasadmin/settings_local.py.example saasadmin/settings_local.py; fi
	${VENV} python manage.py migrate
	${VENV} python manage.py compilemessages

collectstatic:
	${VENV} (echo "yes" | python manage.py collectstatic)

runserver: collectstatic
	${VENV} python manage.py runserver localhost:8000

token:
	${VENV} python manage.py drf_create_token -r admin

translate:
	${VENV} cd apps/core && django-admin compilemessages
	${VENV} cd apps/backend && django-admin compilemessages
	${VENV} cd apps/frontend && django-admin compilemessages

demo_db:
	${VENV} cat demodata/insertdemo.sql | python manage.py dbshell
	(${VENV} cat demodata/insertdemo.psql.sql | python manage.py dbshell) || echo "ignore errors for sqlite"

messages:
	${VENV} django-admin makemessages -l de
	${VENV} django-admin compilemessages

update:
	git pull || exit -1
	${VENV} python manage.py migrate || exit -1
	make messages || exit -1