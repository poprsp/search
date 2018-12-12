#!/usr/bin/env python3

import sys
from typing import Dict, List

import flask
import flask_restful

import search

app = flask.Flask(__name__)
api = flask_restful.Api(app)
dataset = search.Dataset("data/wikipedia/Words", "data/wikipedia/Links")


class Search(flask_restful.Resource):  # type: ignore
    @staticmethod
    def get(query: str, limit: int) -> List[Dict[str, Dict[str, float]]]:
        return [{
            "url": r.url,
            "score": r.score._asdict()
        } for r in dataset.search(query)[:limit]]


api.add_resource(Search, "/api/search/<string:query>/<int:limit>")


@app.route("/", defaults={"filename": None})
@app.route("/<filename>")
def ui(filename: str) -> flask.Response:
    if not filename:
        filename = "index.html"
    return flask.send_from_directory("ui", filename, cache_timeout=1)


@app.route("/data/<path:path>")
def data(path: str) -> flask.Response:
    return flask.send_from_directory("data", path, mimetype="text/plain")


def main() -> int:
    app.run(host=len(sys.argv) > 1 and sys.argv[1] or "127.0.0.1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
