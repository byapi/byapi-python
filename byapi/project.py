# encoding: utf-8
from __future__ import print_function, unicode_literals, absolute_import, division

from byapi.client import Client


class ProjectClient(Client):
    def select(self, offset=None, limit=None, order_by="create_time", order="asc"):
        """Get the project lists.

        @param offset(string): the offset number.
        @param limit(string): The limit number.
        @param order_by(string): The order field, such as "create_time".
        @param order(string): The order method, such as "asc" or "desc".

        @return(dict):
            @key count(int): the total number.
            @key list(list): the project list.
        """

        self._validate_order(order)

        kwargs = self._generate_page_kwargs(order_by, order, offset, limit)
        return self.request("projectSelect", **kwargs)
