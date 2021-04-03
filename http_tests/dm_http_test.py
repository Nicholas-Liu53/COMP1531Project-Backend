import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

# Simple sanity test to check that your server is set up properly
def test_url(url):
    assert url.startswith("http")

def test_dm_details(url):
    pass

def test_dm_list(url):
    pass

def test_dm_create(url):
    pass

def test_dm_remove(url):
    pass

def test_dm_invite(url):
    pass

def test_dm_leave(url):
    pass

def test_dm_messages(url):
    pass