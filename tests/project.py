#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from byapi import ProjectClient

signature = "abcdefghijklmnopqrstuvwxyz1234567890"
user_id = "10000123456"
client = ProjectClient(user_id=user_id, signature_key=signature)


def select():
    resp = client.select()
    print(resp)


def test():
    print("Start to test Project")

    select()


if __name__ == "__main__":
    test()
