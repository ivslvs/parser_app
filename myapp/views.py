from collections import defaultdict
from bs4 import BeautifulSoup
from flask import request, abort, jsonify
from flask_restful import Resource
import requests
import re
from myapp import api
from myapp.worker import celery


@celery.task(name='__main__.get_tags')
def get_all_html_tags(html) -> dict:
    """Parsing html"""
    soup = BeautifulSoup(html, 'lxml')
    dict_tags = defaultdict(int)

    for child in soup.recursiveChildGenerator():
        if child.name:
            dict_tags[child.name] += 1
    return dict_tags


class UrlDetail(Resource):
    """Getting Celery task - all html tags"""
    def get(self, task_id):
        try:
            response = get_all_html_tags.AsyncResult(task_id)
            return jsonify(response.get())
        except Exception:
            abort(404)


class UrlCreate(Resource):
    def get_html_text(self, url: str) -> str:
        """Getting html text content"""
        req = requests.get(url)
        return req.text

    def check_url_regex(self, url: str) -> list:
        """Url regex"""
        url_check = re.findall(r'\bhttp[s]?://', url)
        return url_check

    def post(self):
        """ Url validation and sending task to Celery"""
        url = request.get_json()['url']

        if self.check_url_regex(url):
            response = get_all_html_tags.apply_async(args=[self.get_html_text(url)])
            return jsonify(response.id)

        return {"Error": "URL must start from \'http' or \'https'"}, 404


api.add_resource(UrlCreate, "/tags/")
api.add_resource(UrlDetail, "/tags/<task_id>")
