# Blockchain

[![Build Status](https://travis-ci.org/Wyvarn/blockchain.svg?branch=master)](https://travis-ci.org/Wyvarn/blockchain)
[![codecov](https://codecov.io/gh/Wyvarn/blockchain/branch/master/graph/badge.svg)](https://codecov.io/gh/Wyvarn/blockchain)
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

## Running the application

First you will need to create a `.env` file at the root of the project and set the following:

```dotenv
SECRET_KEY=<SECRET_KEY>
CSRF_SESSION_KEY=<SESSION_KEY>
SECURITY_PASSWORD_SALT=<SECURITY_PASSWORD_SALT>
FLASK_CONFIG=develop
```

The application can be run with:

```bash
python manage.py runserver
```

This will start up the application on address [http://127.0.0.1:5000](http://127.0.0.1:5000)

In the case that this is running in a virtual machine, say, with [Vagrant](https://www.vagrantup.com/), then use the
`publicserver` command:

```bash
python manage.py publicserver
```

This will start up the application on address [http://0.0.0.0:5000](http://0.0.0.0:5000) which will expose this address
making it accessible publicly to the host. There is a [Vagrantfile](./Vagrantfile) present in the root of the project. 
[Vagrant](https://www.vagrantup.com/) will need to be installed as well as [VirtualBox](https://www.virtualbox.org/). 
However, this setup is not necessary to have.

Once the application is up and running, you can interact with the various endpoints that exist with either 
[curl](https://curl.haxx.se/), [httpie](https://httpie.org/) or any REST client.

### Available endpoints

| Endpoint | Description |
| ---- | ------------- |
| [POST /api/block/transaction/new](#) | Creates a new transaction
| [POST /api/block/mine](#) | Mines a block
| [GET /api/block/chain](#) | Gets the blockchain
| [POST /api/block/nodes/register](#) | Register a node
| [POST /api/block/nodes/resolve](#) | Resolve nodes


### Example requests

___Create a new transaction___

Creates a new transaction

```bash
curl --request POST \                                             
  --url http://127.0.0.1:5000/api/block/transactions/new \
  --header 'content-type: application/json' \
  --data '{
 "sender": "onluncd",
 "recipient": "bouncda",
 "amount": 100
}'
{
  "message": "Transaction will be added to block 2"
}
```
> Note that sender and recipient are the addresses 

___Mine a block___

Mines a block


```bash
$ curl --request POST --url http://127.0.0.1:5000/api/block/mine --header 'content-type: application/json'
{
  "index": 4, 
  "message": "New block forged", 
  "previous_hash": "5b4829f6824ac142fd006c88a4740cd58f3eb831a8d6ae852277e28d19e337bf", 
  "proof": 119678, 
  "transactions": [
    {
      "amount": 1, 
      "recipient": "0cc5349eba584f3484b0b3fe0d12bd60", 
      "sender": "0"
    }
  ]
}
```
> mines a block

This mines a block in the chain and _awards_ the miner with 1 coin.

___Get the chain___

Gets the chain.

```bash
$ curl --request GET --url http://127.0.0.1:5000/api/block/chain
{
	"chain": [
		{
			"index": 1,
			"previous_hash": "1",
			"proof": 100,
			"timestamp": 1530568221.2421486,
			"transactions": []
		},
		{
			"index": 2,
			"previous_hash": "991474378466aecb0439af5db42fb4488397a171b75867c104031da20ca0ee29",
			"proof": 35293,
			"timestamp": 1530568876.0994635,
			"transactions": [
				{
					"amount": 90,
					"recipient": "wsedrftgyuhijokp",
					"sender": "rctvybiunoimpl"
				},
				{
					"amount": 90,
					"recipient": "wsedrftgyuhijokp",
					"sender": "rctvybiunoimpl"
				},
				{
					"amount": 90,
					"recipient": "wsedrftgyuhijokp",
					"sender": "rctvybiunoimpl"
				},
				{
					"amount": 100,
					"recipient": "bouncda",
					"sender": "onluncd"
				},
				{
					"amount": 100,
					"recipient": "bouncda",
					"sender": "onluncd"
				},
				{
					"amount": 1,
					"recipient": "0cc5349eba584f3484b0b3fe0d12bd60",
					"sender": "0"
				}
			]
		},
		{
			"index": 3,
			"previous_hash": "53f4b2d8f3c90eaed36ef8c78d1a35a637d3f8b24aae44b5de5686143dea0a0f",
			"proof": 35089,
			"timestamp": 1530568887.5306444,
			"transactions": [
				{
					"amount": 1,
					"recipient": "0cc5349eba584f3484b0b3fe0d12bd60",
					"sender": "0"
				}
			]
		},
		{
			"index": 4,
			"previous_hash": "5b4829f6824ac142fd006c88a4740cd58f3eb831a8d6ae852277e28d19e337bf",
			"proof": 119678,
			"timestamp": 1530568947.0732439,
			"transactions": [
				{
					"amount": 1,
					"recipient": "0cc5349eba584f3484b0b3fe0d12bd60",
					"sender": "0"
				}
			]
		}
	],
	"length": 4
}
```
> This will get the whole block chain


___Resolve nodes___


```bash
$ curl --request GET --url http://127.0.0.1:5000/api/block/nodes/resolve
{
	"chain": [
		{
			"index": 1,
			"previous_hash": "1",
			"proof": 100,
			"timestamp": 1530568221.2421486,
			"transactions": []
		},
		{
			"index": 2,
			"previous_hash": "991474378466aecb0439af5db42fb4488397a171b75867c104031da20ca0ee29",
			"proof": 35293,
			"timestamp": 1530568876.0994635,
			"transactions": [
				{
					"amount": 90,
					"recipient": "wsedrftgyuhijokp",
					"sender": "rctvybiunoimpl"
				},
				{
					"amount": 90,
					"recipient": "wsedrftgyuhijokp",
					"sender": "rctvybiunoimpl"
				},
				{
					"amount": 90,
					"recipient": "wsedrftgyuhijokp",
					"sender": "rctvybiunoimpl"
				},
				{
					"amount": 100,
					"recipient": "bouncda",
					"sender": "onluncd"
				},
				{
					"amount": 100,
					"recipient": "bouncda",
					"sender": "onluncd"
				},
				{
					"amount": 1,
					"recipient": "0cc5349eba584f3484b0b3fe0d12bd60",
					"sender": "0"
				}
			]
		},
		{
			"index": 3,
			"previous_hash": "53f4b2d8f3c90eaed36ef8c78d1a35a637d3f8b24aae44b5de5686143dea0a0f",
			"proof": 35089,
			"timestamp": 1530568887.5306444,
			"transactions": [
				{
					"amount": 1,
					"recipient": "0cc5349eba584f3484b0b3fe0d12bd60",
					"sender": "0"
				}
			]
		},
		{
			"index": 4,
			"previous_hash": "5b4829f6824ac142fd006c88a4740cd58f3eb831a8d6ae852277e28d19e337bf",
			"proof": 119678,
			"timestamp": 1530568947.0732439,
			"transactions": [
				{
					"amount": 1,
					"recipient": "0cc5349eba584f3484b0b3fe0d12bd60",
					"sender": "0"
				}
			]
		}
	],
	"message": "Our chain is authoritative"
}
```
> Resolves the nodes in the chain

___Register nodes___

```bash
$ curl --request POST --url http://127.0.0.1:5000/api/block/nodes/register \
  --header 'content-type: application/json' \
  --data '{
	"nodes":["http://192.168.1.0:8000"]
}'
{
	"message": "New nodes have been added",
	"total_nodes": [
		"192.168.1.0:8000"
	]
}
```
> registers nodes in the chain

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
6. [Flask Testing](https://pypi.org/project/Flask-Testing/) for testing flask application

## License:

This project is licensed under the MIT License - see the [License](./LICENSE) for more details

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)