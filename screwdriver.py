import httpx
import sys
import os
from bs4 import BeautifulSoup


def print_playlist():
    server = httpx.get('http://127.0.0.1:8888/')
    assert server.status_code == 200, "Error on server"

    html = server.text
    parsed_html = BeautifulSoup(html, 'html.parser')
    print(parsed_html.body.find('ul').text)


def upload_audio():
    assert os.path.isfile(sys.argv[2]), "The file does not exist"
    assert sys.argv[2].endswith(".mp3") or \
        sys.argv[2].endswith(".ogg") or \
        sys.argv[2].endswith(".wav"), "Invalid extension"

    name = os.path.basename(sys.argv[2])
    place = sys.argv[2]

    files = {'file': (name, open(place, 'rb+'), 'multipart/form-data')}
    response = httpx.post('http://127.0.0.1:8888', files=files)
    print(response)


if len(sys.argv) == 2 and sys.argv[1] == 'list':
    print_playlist()
elif len(sys.argv) == 3 and sys.argv[1] == 'upload':
    upload_audio()
else:
    print("Invalid arguments.")
