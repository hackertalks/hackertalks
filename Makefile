all: mydevenv deps
	echo done

mydevenv:
	python contrib/go-pylons.py mydevenv
deps: mydevenv
	sh -c 'source mydevenv/bin/activate; python setup.py develop'

