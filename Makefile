all: syntax test

syntax:
	# Syntax check python
	find python -iname '*.py'|grep -v '/env/'|xargs pep8 --ignore E501
	# Syntax check nodejs
	find nodejs -iname "*.js"|grep -v '/node_modules/'|xargs jshint
	# Syntax check MD files
	mdl --rules ~MD036 etc
test:
	cd python/ctx-defense && nosetests
	cd python/django-ctx && nosetests
	cd python/flask-ctx && nosetests
	cd nodejs/ctx-defense && npm run test
