# encoding: utf-8
from __future__ import print_function, unicode_literals, absolute_import, division

from byapi.client import Client


class ImageClient(Client):
    def create(self, vmid, name, note="", shutdown=False, project_id=None):
        """Create a new customized image.

        @param vmid(string): The VM ID.
        @param name(string): The image name.
        @param note(string): the image note.
        @param shutdown(bool): If true, shutdown the VM before creating the image.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        kwargs = {
            "VM_Id": vmid,
            "Image_Name": name,
            "Image_Note": note,
            "Auto_Shutdown": 1 if shutdown else 0,
        }
        self.request("imageAdd", project_id=project_id, **kwargs)

    def select(self, name=None, type=None, offset=None, limit=None,
               order_by="NAME", order="asc", project_id=None):
        """Query the information of the official or customized images.

        If giving the argument type, query the official or customized images.

        @param name(string): The image name. If not given, query all images.
        @param type(string): the type name of the official images, such as "Base"
                             or "Integration". If not given, query the customized
                             images.
        @param offset(string): the offset number.
        @param limit(string): The limit number.
        @param order_by(string): The order field, such as "NAME".
        @param order(string): The order method, such as "asc" or "desc".
        @param project_id(string): The project id. If not given, use the default.

        @return(dict):
            @key count(int): the total number.
            @key list(list): the image list.
        """

        self._validate_order(order)

        kwargs = self._generate_page_kwargs(order_by, order, offset, limit)

        if name:
            kwargs["Image_Name"] = name

        if type:
            kwargs["Image_Type"] = type
            return self.request("imageBaseSelect", project_id=project_id, **kwargs)

        return self.request("imageSelect", project_id=project_id, **kwargs)

    def update(self, image_id, image_name, image_note, project_id=None):
        """Update the name and the note of the customized image.

        @param image_id(string): The image id.
        @param image_name(string): The image name.
        @param image_note(string): The image note.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        kwargs = {
            "Image_Id": image_id,
            "Image_Name": image_name,
            "Image_Note": image_note,
        }
        self.request("imageUpdate", project_id=project_id, **kwargs)

    def delete(self, image_id, project_id=None):
        """Delete the customized image by the image ID.

        @param image_id(string): The image id.
        @param project_id(string): The project id. If not given, use the default.

        @return: None.
        """

        self.request("imageDel", project_id=project_id, Image_Id=image_id)
