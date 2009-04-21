all: mydevenv deps
	echo done

mydevenv:
	python contrib/go-pylons.py mydevenv
deps: mydevenv
	sh -c 'source mydevenv/bin/activate; python setup.py develop'

clean:
	rm -rf mydevenv
	rm -rf hackertalks.egg-info
	find -name "*.pyc" -delete 
	find -name "*.pyo" -delete 
