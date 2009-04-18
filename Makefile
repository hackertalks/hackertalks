all: mydevenv deps
	echo done

mydevenv:
	python contrib/go-pylons.py mydevenv
deps: mydevenv
	sh -c 'source mydevenv/bin/activate; cd hackertalks; python setup.py develop'

