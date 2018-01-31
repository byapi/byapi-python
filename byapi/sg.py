# encoding: utf-8
from __future__ import print_function, unicode_literals, absolute_import, division

from byapi.client import Client


class SGClient(Client):
    def create(self, name, project_id=None):
        """Create a new Security Group.

        @param name(string): The name of SG.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        kwargs = {
            "Security_Group_Name": name
        }
        self.request("securityAdd", project_id=project_id, **kwargs)

    def select(self, name=None, offset=None, limit=None, order_by="Create_Time",
               order="asc", project_id=None):
        """Query the information of the security group.

        @param name(string): The name of SG.
        @param offset(string): The offset number.
        @param limit(string): The limit number.
        @param order_by(string): The order field, such as "Create_Time".
        @param order(string): The order method, such as "asc" or "desc".
        @param project_id(string): The project id. If not given, use the default.

        @return(dict):
            @key count(int): the total number.
            @key list(list): the SG list.
        """

        self._validate_order(order)

        kwargs = self._generate_page_kwargs(order_by, order, offset, limit)
        if name:
            kwargs["Security_Group_Name"] = name
        return self.request("securitySelect", project_id=project_id, **kwargs)

    def delete(self, sg_id, project_id=None):
        """Delete the security group by the ID.

        @param sg_id(string): The SG ID.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        self.request("securityDel", project_id=project_id, Security_Group_Id=sg_id)

    def bind(self, sg_id, vmid, project_id=None):
        """Bind the security rules of VM to a certain security group.

        @param sg_id(string): The SG ID.
        @param vmid(string): The VM ID.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        kwargs = {
            "Security_Group_Id": sg_id,
            "VM_Id": vmid,
        }
        self.request("securityBind", project_id=project_id, **kwargs)
