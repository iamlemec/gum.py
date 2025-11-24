# terminal tools

import requests
import subprocess

##
## chafa interface
##

def readbin(path):
    with open(path, 'rb') as fid:
        return fid.read()

def chafa(data, **kwargs):
    data = readbin(data) if isinstance(data, str) else data
    sargs = sum([
        [ f'--{k}', f'{v}' ] for k, v in kwargs.items() if v is not None
    ], [])
    subprocess.run([ 'chafa', *sargs, '-' ], input=data, stderr=subprocess.DEVNULL)

##
## server interface
##

class GumServer:
    def __init__(self, host='localhost', port=3602, path='../gum.js/src/server.js'):
        args = [ 'node', path, '--host', host, '--port', str(port) ]
        self.server = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.url = f'http://{host}:{port}'

    def evaluate(self, code, pixels=None):
        args = '?size={pixels}' if pixels is not None else ''
        url = f'{self.url}/evaluate{args}'
        headers = { 'Content-Type': 'text/plain' }
        response = requests.post(url, data=code, headers=headers)
        return response.text

    def render(self, code, pixels=None):
        args = '?size={pixels}' if pixels is not None else ''
        url = f'{self.url}/render{args}'
        headers = { 'Content-Type': 'text/plain' }
        response = requests.post(url, data=code, headers=headers)
        return response.content

##
## server instance
##

# singleton server instance
server = GumServer()

def restart():
    global server
    del server
    server = GumServer()

def evaluate(code, **kwargs):
    return server.evaluate(code, **kwargs)

def render(code, **kwargs):
    return server.render(code, **kwargs)

def display(code, size=None, format=None, **kwargs):
    # evaluate or render
    if format is None or format == 'svg':
        data = evaluate(code, **kwargs).encode()
    elif format == 'png':
        data = render(code, **kwargs)
    else:
        raise ValueError(f'Invalid format: {format}')

    # display on terminal
    chafa(data, size=size)

def display_file(path, **kwargs):
    with open(path, 'r') as fid:
        code = fid.read()
    display(code, **kwargs)
