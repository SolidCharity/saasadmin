VENV := . .venv/bin/activate &&

all:
	@echo "help:"
	@echo "  make quickstart"


quickstart: create_venv pip_packages
	@echo 
	@echo =====================================================================================
	@echo Installation has finished successfully

pip_packages:
	${VENV} pip install --upgrade pip
	${VENV} pip install -r requirements.txt

create_venv:
	python3 -m venv .venv
