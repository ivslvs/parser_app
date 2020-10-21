from collections import defaultdict, Counter
from bs4 import BeautifulSoup
from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource
from celery import Celery
import requests
import re
import os


app = Flask(__name__)


class Configuration:
    DEBUG = True


app.config.from_object(Configuration)
api = Api(app)

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')

celery = Celery('task',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)


@celery.task(name='task.get_all_html_tags')
def get_all_html_tags(html) -> dict:
    """Parsing html"""
    soup = BeautifulSoup(html, 'lxml')
    dict_tags = Counter([child.name for child in soup.recursiveChildGenerator()])
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
        """ Url validation and sending task"""
        url = request.get_json()['url']

        if self.check_url_regex(url):
            response = get_all_html_tags.apply_async(args=[self.get_html_text(url)])
            return jsonify(response.id)

        return {"Error": "URL must start from \'http' or \'https'"}, 404


api.add_resource(UrlCreate, "/tags/")
api.add_resource(UrlDetail, "/tags/<task_id>")


if __name__ == '__main__':
    app.run()
