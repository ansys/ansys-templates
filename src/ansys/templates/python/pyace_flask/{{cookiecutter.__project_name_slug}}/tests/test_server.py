{%- if cookiecutter.copyright != "None" -%}
# Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. Unauthorised use, distribution or duplication is prohibited
{% endif %}

import json
import multiprocessing
import random

import requests

from src.server import create_app


class TestServer:
    def setup_class(self):
        port = random.randint(5000, 10000)
        self.base_url = "http://127.0.0.1:" + str(port)
        app = create_app()
        self.server_proc = multiprocessing.Process(target=app.run, args=["127.0.0.1", port, False])
        self.server_proc.start()

    def teardown_class(self):
        self.server_proc.terminate()
        self.server_proc.join()

    def test_get_version(self):
        response = requests.get(self.base_url + "/api/version", timeout=3)
        assert response.status_code == 200

    def test_get_health_status(self):
        response = requests.get(self.base_url + "/api/health", timeout=3)
        assert response.status_code == 200
        assert json.loads(response.content)["status"] == "ok"
