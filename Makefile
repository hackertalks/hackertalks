all: mydevenv deps
	echo done

mydevenv:
	python2.5 contrib/go-pylons.py mydevenv
deps: mydevenv
	sh -c 'source mydevenv/bin/activate; easy_install jinja2 SQLAlchemy'

