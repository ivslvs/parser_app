This parser is written in Python using the micro framework Flask (RESTful).

- Python 3.8

- Flask

- Docker

- Celery



Installing

docker-compose build

docker-compose up



The routes

/tags/ - POST request of random URL. Exp: {"url":"https://www.google.com"} in JSON. Response - id

/tags/id - GET request that parses received URL and counts all HTML tags. Response - Exp: {html: 1, head: 1, body: 1. p: 10, img: 2} in JSON
