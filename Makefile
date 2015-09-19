.PHONY: docs

init:
	pip install -r requirements.txt

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload

docs-init:
	pip install -r docs/requirements.txt

docs:
	cd docs && make html
	@echo "Build successful! View the docs homepage at docs/_build/html/index.html."
