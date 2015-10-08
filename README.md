Semantic Food
=============

Semantic Food is a web-platform to store, search and share cooking recipes semantically.


Get Started
===========

### Pre-requirements:
You will need the following software installed:
- [Python 3](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)

### Installation:

#### - Development
```
git clone https://github.com/g-div/semanticfood
cd semanticfood
python setup.py install

python semanticfood/app.py
```

#### - Deployment
```
pip install git+https://github.com/g-div/semanticfood

semanticfood
```

This will start the [Flask](http://flask.pocoo.org/)-based server on port 8000.

Documentation
=============

The source is located in the [docs](https://github.com/g-div/semanticfood/tree/master/docs) folder and can be built using [Sphinx](http://sphinx-doc.org/):

	cd docs
	pip install -r requirements.txt
	make html

Or ```make latexpdf``` to render a PDF.

