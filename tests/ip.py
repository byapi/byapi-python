#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from byapi import IPClient

vmid = "VM3a39d3f81922286ee475a9"
group_id = "BWRIGROUP93a5605f19257321af3cec"

signature = "abcdefghijklmnopqrstuvwxyz1234567890"
user_id = "10000123456"
client = IPClient(user_id=user_id, signature_key=signature, local_id="wuxi")


def create():
    resp = client.create(count_type="hour")
    print(resp)


def select():
    resp = client.select()
    print(resp)


def update():
    client.update(group_id, 3)


def bind():
    client.bind(group_id, vmid)


def unbind():
    client.unbind(group_id)


def delete():
    client.delete(group_id)


def renew():
    client.renew(group_id)


def change_renew():
    client.change_renew(group_id)


def test():
    print("Start to test IP")

    # print("Create IP")
    # create()

    # print("Select IP")
    # select()

    # print("Update IP")
    # update()

    # print("Bind IP")
    # bind()

    # print("Unbind IP")
    # unbind()

    # print("Renew IP")
    # renew()

    # print("Change_Renew IP")
    # change_renew()

    # print("Delete image")
    # delete()


if __name__ == "__main__":
    test()
