# terminal tools

import json
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

class GumUnixPipe:
    def __init__(self, path='../gum.js/src/pipe.js'):
        self.proc = subprocess.Popen(
            [ 'node', path ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def __del__(self):
        self.close()

    def post(self, **request):
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
        self.proc.stdin.close()
        self.proc.wait()

    def evaluate(self, code, pixels=None, **kwargs):
        return self.post(task='evaluate', code=code, size=pixels, **kwargs)

    def render(self, code, pixels=None, **kwargs):
        return self.post(task='render', code=code, size=pixels, **kwargs)

##
## server instance
##

# singleton server instance
server = GumUnixPipe()

def restart():
    global server
    del server
    server = GumUnixPipe()

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
