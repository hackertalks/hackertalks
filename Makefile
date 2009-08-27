PYTHON = /usr/bin/env python

all: mydevenv deps
	echo done

mydevenv:
	$(PYTHON) contrib/go-pylons.py --no-site-packages  mydevenv
deps: mydevenv
	bash -c 'source mydevenv/bin/activate; python setup.py develop'

develop:
	$(PYTHON) setup.py develop
build:
	$(PYTHON) setup.py build
install: build
	$(PYTHON) setup.py install
test:
	$(PYTHON) setup.py nosetests

clean:
	rm -rf mydevenv build dist *.egg-info *.egg
	find -name "*.pyc" -delete 
	find -name "*.pyo" -delete 
