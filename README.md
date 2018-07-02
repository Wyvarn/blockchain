# Blockchain

[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

This is a simple blockchain implementation. Flask is used as a micro-framework to allow making http requests to the
blockchain.

## Pre-requisites

You will need [Python 3.6](https://www.python.org/downloads/release/python-366/) installed on your development machine.
And further install [virtualenv](https://virtualenv.pypa.io/en/latest/), [pip](https://pip.pypa.io/en/stable/) or 
[pipenv](https://github.com/pypa/pipenv).

Optional download is [Docker](https://www.docker.com/) if you want to run the application in a container

## Setup

Setup is simple.

Install required dependencies with (if using pip):

```bash
virtualenv -p python3 venv
source venv/bin/activate
# ensure you are running in your virtual environment
(venv) $ pip install -r requirements
``` 
> this will install the required dependencies in the environment

If using `pipenv` you can optionally do the following:

```bash
pipenv install
```
> This will setup a virtual environment and install the dependencies from the [Pipfile](./Pipfile)

Note that this will set up a virtual environment in your home directory under `.virtualenvs`, if you want pipenv to 
setup the virtuelenv in the project root, create a .envrc file and add the following to it

```dotenv
export PIPENV_VENV_IN_PROJECT=true
export PIPENV_DEFAULT_PYTHON_VERSION=3.6
```

Then run

```bash
pipenv install
```

This will setup a virtualenv in the root of the project

## Running Tests

Run tests with :

```bash
python manage.py test
```

This will run unit tests on utilities used and on the flask application by creating a 
[flask test client](http://flask.pocoo.org/docs/1.0/testing/).

## Coding style

[Black](https://github.com/ambv/black) is used for code formatting. Run black with:

```bash
black .
```

This will automatically format all python files in the specified directory

## Deployment

Deployment has been left up to the developer to decide on how to deploy the project. This has been structure in a way
that deployment can be to any platform. If using [Docker](https://www.docker.com/) for deployment you can create an 
image and deploy to a given registry:

```bash
# build the image
docker build -t <YOUR_DOCKER_USERNAME>/blockchain .
export DOCKER_PASSWORD=<YOUR_DOCKER_PASSWORD>

# this will log you in to the Docker hub registry (If you have an account) 
echo $DOCKER_PASSWORD | docker login -u <YOUR_DOCKER_USERNAME> --password-stdin

# push the created image to docker hub registry
docker push <YOUR_DOCKER_USERNAME>/blockchain
```

After which you can then deploy the image to services that support container orchestration.

## Build with

1. [Python 3.6](https://www.python.org/downloads/) Programming language used
2. [Flask](http://flask.pocoo.org/) Micro-web server
3. [Flask Script](https://flask-script.readthedocs.io/en/latest/) Used for script commands
4. [Black](https://github.com/ambv/black) Code formatter
5. [Pytest](https://docs.pytest.org/en/latest/) for running tests

## License:

This project is licensed under the MIT License - see the [License](./LICENSE) for more details

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)