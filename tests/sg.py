#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from byapi import SGClient

vmid = "VM8a3755d6952f16ba03d0eb"
sg_id = "GRP48ea97046c555a163818a9"

signature = "abcdefghijklmnopqrstuvwxyz1234567890"
user_id = "10000123456"
client = SGClient(user_id=user_id, signature_key=signature, local_id="wuxi")


def create():
    name = "testsgcreate"
    client.create(name)


def select():
    resp = client.select()
    print(resp)


def bind():
    client.bind(sg_id, vmid)


def delete():
    client.delete(sg_id)


def test():
    print("Start to test SG")

    # print("Create SG")
    # create()

    # print("Select SG")
    # select()

    # # print("Bind SG")
    # bind()

    # print("Delete image")
    # delete()


if __name__ == "__main__":
    test()
