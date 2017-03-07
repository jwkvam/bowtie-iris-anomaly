#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
from functools import wraps

from builtins import bytes
import click
import msgpack
from flask import Flask, render_template, copy_current_request_context
from flask import request, Response
from flask_socketio import SocketIO, emit
import eventlet


class GetterNotDefined(AttributeError):
    pass


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'username' and password == 'password'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# import the user created module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import example

app = Flask(__name__)
app.debug = False
socketio = SocketIO(app, binary=True)
# not sure if this is secure or how much it matters
app.secret_key = os.urandom(256)

def context(func):
    def foo():
        with app.app_context():
            func()
    return foo


class Scheduler(object):

    def __init__(self, seconds, func):
        self.seconds = seconds
        self.func = func
        self.thread = None

    def start(self):
        self.thread = eventlet.spawn(self.run)

    def run(self):
        ret = eventlet.spawn(context(self.func))
        eventlet.sleep(self.seconds)
        try:
            ret.wait()
        except:
            traceback.print_exc()
        self.thread = eventlet.spawn(self.run)

    def stop(self):
        if self.thread:
            self.thread.cancel()


@app.route('/')
def index():
    return render_template('index.html')







@socketio.on('9#hover')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('9#hover', 'anomplot', 'get')])
        uniq_events.remove(('9#hover', 'anomplot', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['9#hover'] = example.anomplot._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['9#hover'])
        example.anom_click_point(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('11#select')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('11#select', 'attrplot', 'get')])
        uniq_events.remove(('11#select', 'attrplot', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['11#select'] = example.attrplot._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['11#select'])
        example.attr_select_points(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('9#click')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('9#click', 'anomplot', 'get')])
        uniq_events.remove(('9#click', 'anomplot', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['9#click'] = example.anomplot._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['9#click'])
        example.anom_click_point(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('6#change')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('1#change', 'algo_select', 'get'), ('3#switch', 'normalize_switch', 'get'), ('5#change', 'neighbor_slider', 'get'), ('2#change', 'species_select', 'get'), ('6#change', 'perplex_slider', 'get')])
        uniq_events.remove(('6#change', 'perplex_slider', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['6#change'] = example.perplex_slider._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['1#change'])
        user_args.append(event_data['3#switch'])
        user_args.append(event_data['5#change'])
        user_args.append(event_data['2#change'])
        user_args.append(event_data['6#change'])
        example.baseviz(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('11#hover')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('11#hover', 'attrplot', 'get')])
        uniq_events.remove(('11#hover', 'attrplot', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['11#hover'] = example.attrplot._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['11#hover'])
        example.attr_click_point(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('1#change')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('1#change', 'algo_select', 'get'), ('3#switch', 'normalize_switch', 'get'), ('5#change', 'neighbor_slider', 'get'), ('2#change', 'species_select', 'get'), ('6#change', 'perplex_slider', 'get')])
        uniq_events.remove(('1#change', 'algo_select', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['1#change'] = example.algo_select._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['1#change'])
        user_args.append(event_data['3#switch'])
        user_args.append(event_data['5#change'])
        user_args.append(event_data['2#change'])
        user_args.append(event_data['6#change'])
        example.baseviz(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('11#click')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('11#click', 'attrplot', 'get')])
        uniq_events.remove(('11#click', 'attrplot', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['11#click'] = example.attrplot._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['11#click'])
        example.attr_click_point(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('5#change')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('1#change', 'algo_select', 'get'), ('3#switch', 'normalize_switch', 'get'), ('5#change', 'neighbor_slider', 'get'), ('2#change', 'species_select', 'get'), ('6#change', 'perplex_slider', 'get')])
        uniq_events.remove(('5#change', 'neighbor_slider', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['5#change'] = example.neighbor_slider._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['1#change'])
        user_args.append(event_data['3#switch'])
        user_args.append(event_data['5#change'])
        user_args.append(event_data['2#change'])
        user_args.append(event_data['6#change'])
        example.baseviz(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('3#switch')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('1#change', 'algo_select', 'get'), ('3#switch', 'normalize_switch', 'get'), ('5#change', 'neighbor_slider', 'get'), ('2#change', 'species_select', 'get'), ('6#change', 'perplex_slider', 'get')])
        uniq_events.remove(('3#switch', 'normalize_switch', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['3#switch'] = example.normalize_switch._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['1#change'])
        user_args.append(event_data['3#switch'])
        user_args.append(event_data['5#change'])
        user_args.append(event_data['2#change'])
        user_args.append(event_data['6#change'])
        example.baseviz(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('7#click')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('7#click', 'replot_button', None)])
        uniq_events.remove(('7#click', 'replot_button', None))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()


        user_args = []
        example.replot(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('9#select')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('9#select', 'anomplot', 'get')])
        uniq_events.remove(('9#select', 'anomplot', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['9#select'] = example.anomplot._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['9#select'])
        example.anom_select_points(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)

@socketio.on('2#change')
def _(*args):
    def wrapuser():
        uniq_events = set()
        uniq_events.update([('1#change', 'algo_select', 'get'), ('3#switch', 'normalize_switch', 'get'), ('5#change', 'neighbor_slider', 'get'), ('2#change', 'species_select', 'get'), ('6#change', 'perplex_slider', 'get')])
        uniq_events.remove(('2#change', 'species_select', 'get'))
        event_data = {}
        for ev in uniq_events:
            comp = getattr(example, ev[1])
            if ev[2] is None:
                ename = ev[0]
                raise GetterNotDefined('{ctype} has no getter associated with event "on_{ename}"'
                                       .format(ctype=type(comp), ename=ename[ename.find('#') + 1:]))
            getter = getattr(comp, ev[2])
            event_data[ev[0]] = getter()

        event_data['2#change'] = example.species_select._get(
            msgpack.unpackb(bytes(args[0]['data']), encoding='utf8')
        )

        user_args = []
        user_args.append(event_data['1#change'])
        user_args.append(event_data['3#switch'])
        user_args.append(event_data['5#change'])
        user_args.append(event_data['2#change'])
        user_args.append(event_data['6#change'])
        example.baseviz(*user_args)

    foo = copy_current_request_context(wrapuser)
    eventlet.spawn(foo)


@click.command()
@click.option('--host', '-h', default='0.0.0.0', help='Host IP')
@click.option('--port', '-p', default=9991, help='port number')
def main(host, port):
    scheds = []

    for sched in scheds:
        sched.start()
    socketio.run(app, host=host, port=port)
    for sched in scheds:
        sched.stop()

if __name__ == '__main__':
    main()