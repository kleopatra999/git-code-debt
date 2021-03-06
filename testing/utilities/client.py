from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib

import flask.testing
import mock

from testing.utilities.response import Response


class Client(flask.testing.FlaskClient):
    """A Client wraps the client given by flask to add other utilities."""

    @contextlib.contextmanager
    def patch_ip(self, ip_address):
        """Patches the ip address for the request."""
        with mock.patch.dict(self.__environ_base, {'REMOTE_ADDR': ip_address}):
            yield

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

        self.__environ_base = {}

    def _update_environment(self, kwargs):
        """Somewhat evil method which mutates kwargs to merge in the base
        environment.
        """
        kwargs['environ_base'] = dict(
            self.__environ_base, **kwargs.pop('environ_base', {})
        )

    def open(self, *args, **kwargs):
        self._update_environment(kwargs)
        return Response(super(Client, self).open(*args, **kwargs))
