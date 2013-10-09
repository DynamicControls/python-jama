
# python-jama

This module offers a light-weight wrapper to the `Jama` api[1] interaction in Python.

It provides programmatic access to the jama

## Basic Usage

In order to use this API you will need to have access to a Jama instance and an
authenticated account.

Create a file `~/.jama` containing the following:

    [soap]
    url = http://jama.example.com/contour/ws/v3/soap/ContourSoapService?wsdl
    account = <username>
    password = <password>

Here is an example to use the api to get an item from jama.
The Jama Soap API documentation looks like this:

    getItem(WsAuth token, java.lang.Long itemId)

The Python looks like:

    from jama import API
    api = API()
    api('getItem', 1234)


## Installation

    pip install python-jama

or download the source package from the project page on [github][2] and run

    python setup.py install

## Development

Development is on the [github project page][2], patches and pull requests welcome!

[1]: http://ws.jamasoftware.com//latest/com/jamasoftware/contour/ws/v3/ContourSoapServiceImpl.html
[2]: https://github.com/dynamiccontrols/python-jama/