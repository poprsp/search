# Installation

```sh
pip3 install -r requirements.txt
```

Note that python 3 is required.


# Run

```sh
./app.py
```


# GUI

Browse to http://127.0.0.1:5000


# REST

With [httpie](https://httpie.org/):

```sh
$ http 127.0.0.1:5000/api/search/nintendo/5
HTTP/1.0 200 OK
Content-Length: 931
Content-Type: application/json
Date: Wed, 12 Dec 2018 16:50:50 GMT
Server: Werkzeug/0.14.1 Python/3.5.3

[
    {
        "score": {
            "content": 1.0,
            "location": 0.8,
            "page_rank": 0.22362367292210505,
            "total": 2.0236236729221053
        },
        "url": "data/wikipedia/Words/Games/Nintendo"
    },
    {
        "score": {
            "content": 0.5081967213114754,
            "location": 0.8,
            "page_rank": 0.19207062922238075,
            "total": 1.5002673505338564
        },
        "url": "data/wikipedia/Words/Games/Nintendo_Switch"
    },
    {
        "score": {
            "content": 0.4459016393442623,
            "location": 0.8,
            "page_rank": 0.2034982889823662,
            "total": 1.4493999283266286
        },
        "url": "data/wikipedia/Words/Games/Nintendo_Entertainment_System"
    },
    {
        "score": {
            "content": 0.7213114754098361,
            "location": 0.002416918429003021,
            "page_rank": 0.18384249989698295,
            "total": 0.9075708937358221
        },
        "url": "data/wikipedia/Words/Games/List_of_Game_of_the_Year_awards"
    },
    {
        "score": {
            "content": 0.18360655737704917,
            "location": 0.4,
            "page_rank": 0.18917665610519044,
            "total": 0.7727832134822397
        },
        "url": "data/wikipedia/Words/Games/Super_Nintendo_Entertainment_System"
    }
]
```
