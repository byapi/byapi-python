#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from byapi import ImageClient

vmid = "VM8a3755d6952f16ba03d0eb"
image_id = "IMG82e56a15957dbe89692af5"

signature = "abcdefghijklmnopqrstuvwxyz1234567890"
user_id = "10000123456"
client = ImageClient(user_id=user_id, signature_key=signature)


def create():
    name = "testimagecreate"
    client.create(vmid, name)


def select():
    resp = client.select()
    print(resp)

    resp = client.select(type="Base")
    print(resp)

    resp = client.select(type="Integration")
    print(resp)


def update():
    image_name = "testimageupdate"
    image_note = "update"
    client.update(image_id, image_name, image_note)


def delete():
    client.delete(image_id)


def test():
    print("Start to test Image")

    # print("Create image")
    # create()

    # print("Select image")
    # select()

    # print("Update image")
    # update()

    # print("Delete image")
    # delete()


if __name__ == "__main__":
    test()
