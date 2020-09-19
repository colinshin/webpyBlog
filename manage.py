# -*- coding: utf-8 -*-

import web
import actions
import redis
# from util.init import init

SESSION = 'SESSION:'


class RedisStore(web.session.Store):
    def __init__(self, ip='localhost', port=6379, db=0, initial_flush=False):
        self.redis_server = redis.Redis(ip, port, db)
        if initial_flush:
            self.redis_server.flushdb()

    def __contains__(self, key):
        # test if session exists for given key
        return bool(self.redis_server.get(SESSION + key))

    def __getitem__(self, key):
        # attempt to get session data from redis store for given key
        data = self.redis_server.get(SESSION + key)
        # if the session existed for the given key
        if data:
            # update the expiration time
            self.redis_server.expire(SESSION + key,
                                     web.webapi.config.session_parameters.timeout)
            return self.decode(data)
        else:
            raise KeyError

    def __setitem__(self, key, value):
        # set the redis value for given key to the encoded value, and reset the
        # expiration time
        self.redis_server.set(SESSION + key,
                              self.encode(value))
        self.redis_server.expire(SESSION + key,
                                 web.webapi.config.session_parameters.timeout)

    def __delitem__(self, key):
        self.redis_server.delete(SESSION + key)

    def cleanup(self, timeout):
        # since redis takes care of expiration for us, we don't need to do any
        # clean up
        pass


if __name__ == "__main__":
    # init() 数据库表创建和初始化使用
    theApp = web.application(actions.urls, globals())
    web.config.session_parameters['cookie_name'] = 'web_cms_sid'
    web.config.session_parameters['cookie_domain'] = None
    web.config.session_parameters['timeout'] = 86400
    web.config.session_parameters['ignore_expiry'] = True
    web.config.session_parameters['ignore_change_ip'] = True
    web.config.session_parameters['secret_key'] = 'JJIEhi323rioes34hafwaj2'
    web.config.session_parameters['expired_message'] = 'Session expired'
    session = web.session.Session(theApp, RedisStore(),
                                  initializer={'username': '', 'user_id': ''})


    def session_hook():
        web.ctx.session = session


    theApp.add_processor(web.loadhook(session_hook))
    theApp.run()
