# encoding: utf-8
from __future__ import print_function, unicode_literals, absolute_import, division

from byapi.client import Client
from byapi.utils import datetime2str


class VMClient(Client):
    def create(self, vm_name, password, security_group_id, image_id, os_type,
               cpu=2, memory=4, vm_num=1, bandwidth=None, data_disk_size=None,
               count_type="month", number=1, auto_renew=False, application="vm",
               note="", shbw_id=None, execute_time=None, project_id=None):
        """Create a new VM.

        @param vm_name(string): The name of VM.
        @param password(string): The password of VM.
        @param security_group_id(string): The SG ID.
        @param image_id(string): The image ID.
        @param os_type(string): The type of VM, such as "Linux" or "Windows".
        @param cpu(int): The number of CPU Core.
        @param memory(int): The size of the memory. The unit is GB.
        @param vm_num(int): The number of VM to create.
        @param bandwidth(int): The size of the bandwidth of the public ip.
                               If not given, don't allocate the public ip.
        @param data_disk_size(int): The size of the data disk. The unit is GB.
                                    If not given, don't allocate the data disk.
        @param count_type(string): The type of the charging account,
                                   such as "year", "month", "hour".
        @param number(int): The duration of the account.
        @param note(string): The note of VM.
        @param auto_renew(bool): if true, renew the account automatically.
        @param shbw_id(string): the id of the shared bandwidth.
        @param execute_time(datetime): The datetime to delete automatically.
        @param project_id(string): The project id. If not given, use the default.
        @param application(string): The vm type, such as vm,general_vm,io_vm,hpc_vm,hpc_uvm,bd_vm,hz_vm

        @retrun(dict):
            @key(string): The VM ID.
            @key(string): The id of the charging account if the vm has the public ip.
        """

        if not vm_name:
            raise ValueError("missing the name of VM")
        if not password:
            raise ValueError("missing the password of VM")

        self._validate_cpu_memory(cpu, memory)
        self._validate_data_disk(data_disk_size)

        kwargs = {
            "Image_Id": image_id,
            "Os_Type": os_type,
            "ECU": cpu,
            "Memory_Size": memory,
            "Security_Group_Id": security_group_id,
            "VM_Name": vm_name,
            "Note": note,
            "Password": password,
            "Count_Type": count_type,
            "Number": number,
            "VM_Num": vm_num,
            "Auto_Renew": auto_renew,
            "Application": application,
        }

        if bandwidth:
            kwargs["Bandwidth"] = bandwidth
        if data_disk_size:
            kwargs["Data_Disk_Size"] = data_disk_size
        if shbw_id:
            kwargs["Shbw_Id"] = shbw_id
        if execute_time:
            kwargs["Execute_Time"] = datetime2str(execute_time)

        data = self.request("vmAdd", project_id=project_id, **kwargs)
        results = {}
        vms = [vm for vm in data["VG_Id"].strip().split(",") if vm]
        for vm in vms:
            vs = vm.split("|")
            results[vs[0]] = "" if len(vs) == 1 else vs[1]
        return results

    def select(self, outer_ip=None, vm_name=None, offset=None, limit=None,
               order_by="NAME", order="asc", project_id=None):
        """Query the information of the VM.

        @param outer_ip(string): The outer public ip.
        @param vm_name(string): The name of VM.
        @param offset(string): The offset number.
        @param limit(string): The limit number.
        @param order_by(string): The order field, such as "NAME", "Outer_Ip", etc.
        @param order(string): The order method, such as "asc" or "desc".
        @param project_id(string): The project id. If not given, use the default.

        @return(dict):
            @key count(int): the total number.
            @key list(list): the VM list.
        """

        self._validate_order(order)

        if order_by not in ("OS_VERSION", "NAME", "Outer_Ip", "Bandwidth", "RI_END_TIME"):
            raise ValueError("order_by does not support {}".format(order_by))

        kwargs = self._generate_page_kwargs(order_by, order, offset, limit)
        if outer_ip:
            kwargs["Outer_Ip"] = outer_ip
        if vm_name:
            kwargs["VM_Name"] = vm_name
        return self.request("vmSelect", project_id=project_id, **kwargs)

    def update(self, vmid, cpu, memory, data_disk_size=None, hot=False,
               project_id=None):
        """Update the configuration of the VM.

        @param vmid(string): The VM ID.
        @param cpu(int): The number of CPU Core.
        @param memory(int): The size of the memory. The unit is GB.
        @param data_disk_size(int): The size of the data disk. The unit is GB.
        @param hot(bool): If true, execute the hot upgrade. Or the VM must be shutdowned.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        kwargs = {
            "VM_Id": vmid,
            "ECU": cpu,
            "Memory_Size": memory,
            "Hot": hot,
        }

        if data_disk_size is not None:
            kwargs["Data_Disk_Size"] = data_disk_size

        self.request("vmUpdate", project_id=project_id, **kwargs)

    def change_status(self, vmid, status, project_id=None):
        """Change the status of VM.

        @param vmid(string): The VM ID.
        @param status(string): the status action, such as start, down, restart.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        if status not in ("start", "down", "restart"):
            raise ValueError("status must be one of start, down and restart")

        kwargs = {
            "VM_Id": vmid,
            "Status": status,
        }
        self.request("vmChangeStatus", project_id=project_id, **kwargs)

    def detail(self, vmid, project_id=None):
        """Query the detail information of the VM by ID.

        @param vmid(string): The VM ID.
        @param project_id(string): The project id. If not given, use the default.

        @return(dict): The VM information.
        """

        return self.request("vmDetail", project_id=project_id, VM_Id=vmid)

    def power_down(self, vmid, project_id=None):
        """Power off the VM.

        @param vmid(string): The VM ID.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        self.request("vmPowerDown", project_id=project_id, VM_Id=vmid)

    def check_name(self, name, project_id=None):
        """Check whether the VM name is valid.

        @param name(string): The name of SG.
        @param project_id(string): The project id. If not given, use the default.

        @return: None. If the name is invalid, raise an exception with an reason.
        """

        self.request("vmCheckName", project_id=project_id, VM_Name=name)

    def delete(self, vmid, project_id=None):
        """Delete the VM.

        @param vmid(string): The VM ID.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        self.request("vmDel", project_id=project_id, VM_Id=vmid)
