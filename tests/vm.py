#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function

from byapi import VMClient

image_id = "IMG1813d6af92b3e37be40242"
sg_id = "GRP48ea97049caa74ebad2f4"
vmid = "VM8baf5859582d1b6df91c3"

signature = "abcdefghijklmnopqrstuvwxyz1234567890"
user_id = "10000123456"
client = VMClient(user_id=user_id, signature_key=signature)


def create():
    name = "testcreatevm2"
    passwd = "TestCreateVM123"
    resp = client.create(name, passwd, sg_id, image_id, "Linux", cpu=1, memory=2,
                         count_type="hour")
    print(resp)


def select():
    info = client.select()
    print(info)


def update():
    cpu = 4
    memory = 4
    client.update(vmid, cpu, memory)


def change_status():
    status = "down"  # start, down, restart
    client.change_status(vmid, status)


def detail():
    resp = client.detail(vmid)
    print(resp)


def power_down():
    client.power_down(vmid)


def check_name():
    client.check_name("adgdgdaa")


def delete():
    client.delete(vmid)


def test():
    print("Start to test VM")

    # create()
    # select()
    # update()
    # change_status()
    # detail()
    # power_down()
    # check_name()
    # delete()


if __name__ == "__main__":
    test()
