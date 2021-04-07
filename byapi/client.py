# encoding: utf-8
from __future__ import print_function, unicode_literals, absolute_import, division

import requests

from hashlib import md5
from threading import Lock
from byapi.utils import to_bytes, to_unicode, is_string


class Client(object):
    """Client is the client to access the API of BiggerYun."""

    def __init__(self, signature_key, user_id, local_id="wuxi", project_id="0",
                 host="https://api2.biggeryun.com", thread_safe=True,
                 encoding="utf-8", timeout=None, version="v1"):
        """Create a new BiggerYun client.

        @param signature_key(string): The user signature key.
        @param user_id(string): The user id, which must be given if using signature_key.
        @param local_id(string): The local ID, such as "wuxi", "beijing", etc.
        @param project_id(string): The project ID, such as "0", "1", etc,
                                   which is the default project by default.
        @param host(string): The host or ip of the BiggerYun API.
        @param thread_safe(bool): If true, the apis will use the thread lock to
                                  ensure the api call is thread-safe.
        @param encoding(string): the encoding of the request content.
        """
        self._host = host.strip("/")
        self._version = version
        self._local_id = local_id
        self._project_id = project_id
        self._thread_safe = thread_safe
        self._encoding = encoding
        self._timeout = timeout

        self._authorization = signature_key
        self._user_id = user_id

        self._request_url = self._host + "/" + self._version
        self._lock = Lock()

        if signature_key and not user_id:
            raise ValueError("must give user_id when using signature")

    def _send_request(self, url, data):
        return requests.get(url, params=data)

    def _get_lock(self):
        if self._thread_safe:
            self._lock.acquire()

    def _put_lock(self):
        if self._thread_safe:
            self._lock.release()

    def request(self, action, must_authorization=True, project_id=None, **kwargs):
        """Send a request, then read the response.

        Notice: the method only need to be used by the API implementation, such
        as vmAdd, vmSelect, etc.

        @param action(string): The API name, such as vmAdd, vmSelect, etc.
        @param must_authorization(bool): If true, check whether the authorization is valid.
        @param project_id(string): The project id. If not given, use the default.
        @param kwargs(dict): The rest arguments that the API needs.

        @result(dict): a json response result. The common keys have "code",
                       "msg", "time", and "data".
        """
        if must_authorization and not self._authorization:
            raise RuntimeError("No authorization")

        self._get_lock()
        kwargs["Local_Id"] = self._local_id
        kwargs["User_Id"] = self._user_id
        kwargs["Project_Id"] = self._project_id if project_id is None else project_id
        signature_key = self._authorization
        self._put_lock()

        _kwargs = {}
        for key, value in kwargs.items():
            if value is None:
                continue
            elif is_string(value):
                _kwargs[key] = to_unicode(value, self._encoding)
            elif isinstance(value, bool):
                _kwargs[key] = "true" if value else "false"
            elif isinstance(value, (list, tuple)):
                _kwargs[key] = to_unicode(json.dumps(value), self._encoding)
            else:
                _kwargs[key] = value

        _kwargs["Signature"] = self._get_signature(_kwargs, signature_key)
        url = self._request_url + "/" + action

        return self._get_result(self._send_request(url, _kwargs))

    def _get_result(self, resp):
        if resp.content:
            v = resp.json()
            if v["code"] != 200:
                raise Exception("code={}, error={}".format(v["code"], v["msg"]))
            return v["data"]
        return None

    def reset_local_id(self, local_id):
        """Reset the default local id.

        @param local_id(string): the new local id, such as "wuxi", "beijing".
        """

        self._get_lock()
        self._local_id = local_id
        self._put_lock()

    def get_local_id(self):
        """Return the default local id."""

        self._get_lock()
        local_id = self._local_id
        self._put_lock()
        return local_id

    def reset_default_project_id(self, project_id):
        """Reset the default project id.

        @param project_id(string): the new project id.
        """

        self._get_lock()
        self._project_id = project_id
        self._put_lock()

    def get_default_project_id(self):
        """Return the default project id."""

        self._get_lock()
        project_id = self._project_id
        self._put_lock()
        return project_id

    def set_signature_key(self, key, user_id=None):
        """Reset the signature key.

        @param key(string): the signature key.
        @param user_id(string:optional): the user ID. If None, it will use the
                                         previous user ID.
        """
        if not key:
            raise ValueError("key is empty")

        self._get_lock()
        self._authorization = key
        if user_id:
            self._user_id = user_id
        elif not self._user_id:
            self._put_lock()
            raise ValueError("user_id is missing")
        self._put_lock()

    def _get_signature(self, params, signature_key):
        kvs = sorted(params.items(), key=lambda v: v[0])
        kvs.append((signature_key, ""))
        results = ("{0}{1}".format(key, value) for key, value in kvs)
        data = to_bytes("".join(results))
        return md5(data).hexdigest()

    def _generate_page_kwargs(self, order_by, order, offset=None, limit=None):
        kwargs = {
            "Order_By": order_by,
            "Order": order,
        }

        if offset is not None:
            kwargs["Offset"] = offset

        if limit is not None:
            kwargs["Limit"] = limit

        return kwargs

    def _validate_order(self, order):
        if order not in ("asc", "desc"):
            raise ValueError("order must be either asc or desc")

    def _validate_bandwidth(self, bandwidth):
        if not 2 <= bandwidth <= 200:
            raise ValueError("the bandwidth size must be between 2 and 200")

    def _validate_count_type(self, count_type, number):
        if count_type == "year":
            if not 1 <= number <= 3:
                raise ValueError('number must be between 1 and 3 when count_type is "year"')
        elif count_type == "month":
            if not 1 <= 1 <= 9:
                raise ValueError('number must be between 1 and 9 when count_type is "month"')
        elif count_type != "hour":
            raise ValueError('count_type must be "year", "month" or "hour"')

    def _validate_cpu_memory(self, cpu, memory):
        if cpu == 1:
            if memory not in (1, 2, 4):
                raise ValueError("memory must be one of 1, 2 and 4")
        elif cpu == 2:
            if memory not in (2, 4, 6, 8):
                raise ValueError("memory must be one of 1, 2, 4, 6 and 8")
        elif cpu == 4:
            if memory not in (4, 8, 12, 16):
                raise ValueError("memory must be one of 4, 8, 12, 16")
        elif cpu == 8:
            if memory not in (8, 16, 32, 64):
                raise ValueError("memory must be one of 8, 16, 32 and 64")
        elif cpu == 16:
            if memory not in (32, 64):
                raise ValueError("memory must be either 32 or 64")
        elif cpu == 32:
            if memory != 64:
                raise ValueError("memory must be 64")
        else:
            raise ValueError("cpu core must be one of 1, 2, 4, 8, 16 and 32")

    def _validate_data_disk(self, disk_size):
        if disk_size:
            quot, remainder = divmod(disk_size, 10)
            if remainder or not 1 <= quot <= 102:
                raise ValueError("the size of data disk must be the multiple of 10 between 0 and 1020")
