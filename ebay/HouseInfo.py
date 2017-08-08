# -*- coding: utf-8 -*-


class BaseInfo:

    def __init__(self, title, description, image_list):
        self.title = title
        self.description = description
        self.image_list = image_list

    def gatherAttrs(self):
        return ",".join("{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())

class ContactInfo:
    def __init__(self, publisher_type, publisher_name, publisher_contact):
        self.publisher_type = publisher_type
        self.publisher_name = publisher_name
        self.publisher_contact = publisher_contact

    def gatherAttrs(self):
        return ",".join("{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())

class WebInfo:
    def __init__(self, source_view_count, source_link):
        self.source_view_count = source_view_count
        self.source_link = source_link

    def gatherAttrs(self):
        return ",".join("{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())


class AdditionalInfo:
    def __init__(self):
        self.subtitle = '0'
        self.subtitle_de = '0'
        self.subtitle_en = '0'
        self.rent_method = '0'
        self.room_amount = '0'
        self.usable_area = '0'
        self.floor_current = '0'
        self.rent_fee_hot = '0'
        self.rent_fee_cold = '0'
        self.rent_fee_addon = '0'
        self.rent_fee_other = '0'
        self.rent_fee_deposit = '0'
        self.attribute_heating = '0'
        self.attribute_furniture = '0'
        self.attribute_balcony = '0'
        self.attribute_terrace = '0'
        self.layout_kitchen = '0'
        self.attribute_bathtub = '0'
        self.attribute_bathroom = '0'
        self.layout_lavatory = '0'
        self.attribute_disability = '0'
        self.other_old_building = '0'
        self.other_new_building = '0'
        self.feature_elevator = '0'
        self.feature_basement = '0'
        self.feature_loft = '0'
        self.attention_welfare_in = '0'
        self.feature_parking_space = '0'
        self.feature_garden = '0'
        self.attention_allow_pet = '0'
        self.attention_joint_rent = '0'
        self.source_publish_time = '0'
        self.zip_code = '0'
        self.city = '0'
        self.state = 'on_rent'
        self.time_insert = '0'
        self.time_update = '0'
        self.status = '2'

    def gatherAttrs(self):
        return ",".join("{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())


class HouseInfo:
    def __init__(self, baseInfo, contactInfo, webInfo, additionalInfo):
        self.baseInfo = baseInfo
        self.contactInfo = contactInfo
        self.webInfo = webInfo
        self.additionalInfo = additionalInfo

    def gatherAttrs(self):
        return ",".join("{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gatherAttrs())
