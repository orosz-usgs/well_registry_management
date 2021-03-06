PYTHON := env/bin/python
PIP := env/bin/pip
PYLINT := env/bin/pylint

.PHONY: cleanenv devenv prodenv test watch runmigrations runlint

.IGNORE: runlint

cleanenv:
	@echo 'Cleaning environment....'
	rm -rf env/ && rm -rf wellregistry/wellregistry/staticfiles

watch:
	$(PYTHON) wellregistry/manage.py runserver

devenv: env common-env-requirements local-dev-requirements wellregistry/.env

prodenv: env common-env-requirements prod-requirements wellregistry/.env

test:
	cd wellregistry && ../$(PYTHON) manage.py test

runmigrations:
	$(PYTHON) wellregistry/manage.py migrate admin
	$(PYTHON) wellregistry/manage.py migrate auth
	$(PYTHON) wellregistry/manage.py migrate contenttypes
	$(PYTHON) wellregistry/manage.py migrate sessions
	$(PYTHON) wellregistry/manage.py migrate social_django
	$(PYTHON) wellregistry/manage.py migrate registry

runlint:
	$(PYLINT) wellregistry/registry
	$(PYLINT) wellregistry/registry/migrations/0001_registry_table.py
	$(PYLINT) wellregistry/registry/migrations/0002_add_agency_groups.py.py
	$(PYLINT) wellregistry/registry/migrations/0003_country_lookups.py
	$(PYLINT) wellregistry/registry/migrations/0004_lookup_tables.py
	$(PYLINT) wellregistry/wellregistry/

env:
	@echo 'Creating local environment....'
	virtualenv --python=python3.8 --no-download env

common-env-requirements:
	$(PIP) install -r requirements.txt

wellregistry/.env:
	@echo 'Creating environment variables file'
	cp wellregistry/.env.sample wellregistry/.env

local-dev-requirements:
	$(PIP) install -r requirements-dev.txt

prod-requirements:
	$(PIP) install -r requirements-prod.txt