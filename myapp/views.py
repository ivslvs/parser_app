from collections import defaultdict
from bs4 import BeautifulSoup
from flask import request, abort, jsonify
from flask_restful import Resource
import requests
import re

from parser_app.myapp import api
from parser_app.myapp.worker import celery


def get_html(url):
    req = requests.get(url)
    return req.text


@celery.task(name='__main__.get_tags')
def get_tags(html):
    soup = BeautifulSoup(html, 'lxml')
    dict_tags = defaultdict(int)

    for child in soup.recursiveChildGenerator():
        if child.name:
            dict_tags[child.name] += 1
    return dict_tags


class UrlDetail(Resource):
    def get(self, task_id):
        try:
            response = get_tags.AsyncResult(task_id)
            return jsonify(response.get())

        except Exception:
            abort(404)


def post_re(url):
    url_check = re.findall(r'\bhttp[s]?://', url)
    return url_check


class UrlCreate(Resource):
    def post(self):
        url = request.get_json()['url']

        if post_re(url):
            response = get_tags.apply_async(args=[get_html(url)])

            return jsonify(response.id)

        return {"Error": "URL must start from \'http' or \'https'"}, 404


api.add_resource(UrlCreate, "/tags/")
api.add_resource(UrlDetail, "/tags/<task_id>")
