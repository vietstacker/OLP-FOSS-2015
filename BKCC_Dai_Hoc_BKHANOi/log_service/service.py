# -*- coding: utf-8 -*-
#
# Copyright 2014 - StackStorm, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# from aiohttp import MultiDict
# from urlhandler import Url_handler

import asyncio
from aiohttp import web
import json
import loghandler
import config

__author__ = 'techbk'


class UrlHandler(object):
    def __init__(self, _loop):
        """

        :param _loop: object
        """
        self._loop = _loop
        self._loghandler = loghandler.LogHandler()

    @asyncio.coroutine
    def test(self, request):
        """

        :param request:
        :return: web.Response
        """
        print(request.path_qs)

        print(request.GET['project'])
        # text = yield from request.text()
        # print(text)
        # text = "{'test':'ok'}"
        text = json.dumps({'test': 'ok'})
        #print(text)
        return web.Response(body=text.encode('utf-8'))


    @asyncio.coroutine
    def project_log(self, request):
        
        project = request.GET['project']
        print(project)
        level = request.GET['level']
        start = request.GET['start']
        end = request.GET['end']

        jsonlog = self._loghandler.project_log(project,level,start,end)
        #print(jsonlog)
        jsonlog = jsonlog.encode('utf-8')

        return web.Response(body=jsonlog)

    @asyncio.coroutine
    def tong_hop(self, request):
        
        project = request.GET['project']
        level = request.GET['level']
        start = request.GET['start']
        end = request.GET['end']

        jsonlog = self._loghandler.tong_hop(project,level,start,end)
        #print(jsonlog)
        jsonlog = jsonlog.encode('utf-8')

        return web.Response(body=jsonlog)


@asyncio.coroutine
def init(_loop):
    """
    asyncio.async()
    :param _loop:
    :return:
    """
    url_handler = UrlHandler(_loop)

    app = web.Application(loop=_loop)

    app.router.add_route('GET', '/test', url_handler.test)
    app.router.add_route('GET', '/projectlog', url_handler.project_log)
    app.router.add_route('GET', '/tonghop', url_handler.tong_hop)

    handler = app.make_handler()
    srv = yield from _loop.create_server(handler, config.SERVICE_IP, config.SERVICE_PORT)
    print("Server started at http://0.0.0.0:8080")
    return srv, handler


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    srv, handler = loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
