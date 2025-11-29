# terminal tools

import sys
import json
import base64
import subprocess

##
## chafa interface
##

def readtext(path):
    with open(path, 'r') as fid:
        return fid.read()

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

GUM_PATH = '../gum.js/src/pipe.js'

class GumUnixPipe:
    def __init__(self):
        self.init()

    def __del__(self):
        self.close()

    def init(self):
        self.proc = subprocess.Popen(
            [ 'node', GUM_PATH ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stdout.fileno(),
            text=True,
            bufsize=1,
        )

    def post(self, **request):
        # ensure server
        if self.proc is None:
            self.init()

        # send request
        self.proc.stdin.write(json.dumps(request) + '\n')
        self.proc.stdin.flush()

        # read response
        response = json.loads(self.proc.stdout.readline())
        ok, result = response['ok'], response['result']

        # check for errors
        if not ok:
            raise ValueError(result)

        # return response
        return result

    def close(self):
        if self.proc is not None:
            self.proc.stdin.close()
            self.proc.wait()
            self.proc = None

    def evaluate(self, code, pixels=None, **kwargs):
        return self.post(task='evaluate', code=code, size=pixels, **kwargs)

    def render(self, code, pixels=None, **kwargs):
        data = self.post(task='render', code=code, size=pixels, **kwargs)
        return base64.b64decode(data)

##
## server instance
##

# singleton server instance
server = GumUnixPipe()

def evaluate(code, **kwargs):
    return server.evaluate(code, **kwargs)

def render(code, **kwargs):
    return server.render(code, **kwargs)

def display(code, size=75, theme='dark', format=None, method=None, **kwargs):
    # evaluate or render
    if format is None or format == 'svg':
        data = evaluate(str(code), theme=theme, **kwargs).encode()
    elif format == 'png':
        data = render(str(code), theme=theme, **kwargs)
    else:
        raise ValueError(f'Invalid format: {format}')

    # display on terminal
    chafa(data, size=size, format=method)

def display_file(path, **kwargs):
    code = readtext(path)
    display(code, **kwargs)
