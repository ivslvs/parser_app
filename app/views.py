from collections import defaultdict
from bs4 import BeautifulSoup
from flask import request, abort, jsonify
from flask_restful import Resource
import requests
import re

from . import api
from .models import Url, db
from .worker import celery


class UrlCreate(Resource):
    """Endpoint for adding url to the database"""

    def post_re(self, url):
        url_check = re.findall(r'\bhttp[s]?://', url)
        return url_check

    def post(self):
        """Post request"""
        get_url = request.get_json()['url']

        if self.post_re(get_url):  # post_re(get_url) вынесни в отдельную переменную?
            url = Url(url=get_url)
            db.session.add(url)
            db.session.commit()

            post_url_pk = Url.query.filter_by(url=get_url)[-1]
            return jsonify(id=post_url_pk.id)

        return jsonify({'Error': "URL must start from \'http' or \'https'"})  # status 200, нужно поменять на 404?


class UrlDetail(Resource):
    """Endpoint for getting list of all HTML tags"""

    def get_html(self, url):
        req = requests.get(url)
        return req.text

    @celery.task(name='__main__.get_tags')
    def get_tags(self, html):
        soup = BeautifulSoup(html, 'lxml')
        dict_tags = defaultdict(int)

        for child in soup.recursiveChildGenerator():
            if child.name:
                dict_tags[child.name] += 1

        return dict_tags

    def get(self, pk):
        """GET request"""
        try:
            get_url = Url.query.filter_by(id=pk).first()
            response = self.get_tags.delay(self.get_html(get_url.url))
            return jsonify({"Response": "Is being processed"})

        except Exception:
            abort(404)


api.add_resource(UrlCreate, "/tags/")
api.add_resource(UrlDetail, "/tags/<int:pk>")
