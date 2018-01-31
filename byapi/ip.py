# encoding: utf-8
from __future__ import print_function, unicode_literals, absolute_import, division

from byapi.client import Client


class IPClient(Client):
    def create(self, bandwidth=2, count_type="month", number=1, num=1,
               net_type="BGP", auto_renew=True, shbw_id=None, project_id=None):
        """Apply for a new public ip.

        @param bandwidth(int): The size of the bandwidth.
        @param count_type(string): The type of the charging account,
                                   such as "year", "month", "hour".
        @param number(int): The duration of the account.
        @param num(int): The number of the VM.
        @param net_type(string): The type of the network, such as "BGP".
        @param auto_renew(bool): if true, renew the account automatically.
        @param shbw_id(string): the id of the shared bandwidth.
        @param project_id(string): The project id. If not given, use the default.

        @return(list): The list of the ids of the charging account to create.
        """

        self._validate_bandwidth(bandwidth)
        self._validate_count_type(count_type, number)

        kwargs = {
            "Bandwidth": bandwidth,
            "Count_Type": count_type,
            "Number": number,
            "Net_Type": net_type,
            "Num": num,
            "Auto_Renew": auto_renew,
        }

        if shbw_id:
            kwargs["Shbw_Id"] = shbw_id

        data = self.request("netAdd", project_id=project_id, **kwargs)
        return [i for i in data["Group_Id"].strip().split(",") if i]

    def select(self, group_id=None, status=None, outer_ip=None, vm_name=None,
               offset=None, limit=None, order_by="RI_GROUP_IP", order="asc",
               project_id=None):
        """Query the information of the public ips.

        @param group_id(string): The id of the charging account.
        @param status(string): The status of the ip, such as "bind", "unbind".
        @param outer_ip(string): The outer public ip.
        @param vm_name(string): The vm name.
        @param offset(string): The offset number.
        @param limit(string): The limit number.
        @param order_by(string): The order field, such as "RI_GROUP_IP".
        @param order(string): The order method, such as "asc" or "desc".
        @param project_id(string): The project id. If not given, use the default.

        @return(dict):
            @key count(int): the total number.
            @key list(list): the ip list.
        """

        self._validate_order(order)

        kwargs = self._generate_page_kwargs(order_by, order, offset, limit)

        if group_id:
            kwargs["Group_Id"] = group_id
        if status:
            kwargs["Status"] = status
        if outer_ip:
            kwargs["Outer_Ip"] = outer_ip
        if vm_name:
            kwargs["VM_Name"] = vm_name

        return self.request("netSelect", project_id=project_id, **kwargs)

    def update(self, group_id, bandwidth, project_id=None):
        """Modify the bandwidth of the public ip.

        @param group_id(string): The id of the charging account.
        @param bandwidth(int): The size of the bandwidth, between 2 and 200.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        self._validate_bandwidth(bandwidth)

        kwargs = {
            "Group_Id": group_id,
            "Bandwidth": bandwidth,
        }
        self.request("netUpdate", project_id=project_id, **kwargs)

    def delete(self, group_id, project_id=None):
        """Delete and release the public ip.

        @param group_id(string): The id of the charging account.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        self.request("netDel", project_id=project_id, Group_Id=group_id)

    def bind(self, group_id, vm_id, project_id=None):
        """Bind the public ip to a certain VM or shared bandwidth.

        @param group_id(string): The id of the charging account.
        @param vm_id(string): the VM ID.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        kwargs = {
            "Group_Id": group_id,
            "Resource_Id": vm_id,
        }
        self.request("netBind", project_id=project_id, **kwargs)

    def unbind(self, group_id, project_id=None):
        """Unbind the public ip from a certain VM or shared bandwidth.

        @param group_id(string): The id of the charging account.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        self.request("netUnbind", project_id=project_id, Group_Id=group_id)

    def renew(self, group_id, count_type="month", number=1, auto_renew=None,
              project_id=None):
        """Renew for the public ip.

        @param group_id(string): The id of the charging account.
        @param count_type(string): The type of the charging account,
                                   such as "year", "month", "hour".
        @param number(int): The duration of the account.
        @param auto_renew(bool): if true, renew the account automatically.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        self._validate_count_type(count_type, number)

        kwargs = {
            "Group_Id": group_id,
            "Count_Type": count_type,
            "Number": number,
        }
        if auto_renew is not None:
            kwargs["Auto_Renew"] = auto_renew

        self.request("netRenew", project_id=project_id, **kwargs)

    def change_renew(self, group_id, auto_renew=True, project_id=None):
        """Change whether to renew for the public ip.

        @param group_id(string): The id of the charging account.
        @param auto_renew(bool): if true, renew the account automatically.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        kwargs = {
            "Group_Id": group_id,
            "Auto_Renew": auto_renew,
        }
        self.request("netChangeRenew", project_id=project_id, **kwargs)
