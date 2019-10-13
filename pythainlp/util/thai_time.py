# -*- coding: utf-8 -*-
"""
Thai Time
by Wannaphong Phatthiyaphaibun
"""
from .numtoword import num_to_thaiword


class thai_time(object):
    def __init__(self, time: str, types: str = "24-hour"):
        """
        Convert time to Thai words.

        :param str time: time (H:m)
        :param str types: Thai time type
            * *24-hour* - 24-hour clock (default)
            * *6-hour* - 6-hour clock
            * *modified-6-hour* - Modified 6-hour clock
        :return: Thai time
        :rtype: str

        :Example:

            thai_time("8:17").get_time()
            # output:
            # แปดนาฬิกาสิบเจ็ดนาที

            thai_time("8:17",types="6-hour").get_time()
            # output:
            # สองโมงเช้าสิบเจ็ดนาที

            thai_time("8:17",types="modified-6-hour").get_time()
            # output:
            # แปดโมงสิบเจ็ดนาที
        """
        self.time = time
        if not isinstance(self.time, str):
            raise TypeError("please input string (H:m)")
        if ":" not in self.time:
            raise TypeError("please input string (H:m)")

        self.types = types
        self.temp = self.time.split(":")
        self.h = int(self.temp[0])
        self.m = int(self.temp[1])

        self.sent = ""
        if self.types == "6-hour":
            self._type_6hr()
        elif self.types == "modified-6-hour":
            self._type_m6hr()
        elif self.types == "24-hour":
            self._type_24hr()
        else:
            raise NotImplementedError(self.types)

    def get_time(self):
        return self.sent

    def _type_6hr(self):
        """
        Thai time (6-hour clock)
        """
        self.sent = ""
        if self.h == 0:
            self.sent += "เที่ยงคืน"
        elif self.h < 7:
            self.sent += "ตี" + num_to_thaiword(self.h)
        elif self.h < 12:
            self.sent += num_to_thaiword(self.h - 6) + "โมงเช้า"
        elif self.h == 12:
            self.sent += "เที่ยง"
        elif self.h < 18:
            self.sent += "บ่าย" + num_to_thaiword(self.h - 12) + "โมง"
        elif self.h == 18:
            self.sent += "หกโมงเย็น"
        else:
            self.sent += num_to_thaiword(self.h - 18) + "ทุ่ม"
        if self.m == 30:
            self.sent += "ครึ่ง"
        elif self.m != 0:
            self.sent += num_to_thaiword(self.m) + "นาที"

    def _type_m6hr(self):
        """
        Thai time (modified 6-hour clock)
        """
        self.sent = ""
        if self.h == 0:
            self.sent += "เที่ยงคืน"
        elif self.h < 6:
            self.sent += "ตี" + num_to_thaiword(self.h)
        elif self.h < 12:
            self.sent += num_to_thaiword(self.h) + "โมง"
        elif self.h == 12:
            self.sent += "เที่ยง"
        elif self.h < 19:
            self.sent += num_to_thaiword(self.h - 12) + "โมง"
        else:
            self.sent += num_to_thaiword(self.h - 18) + "ทุ่ม"
        if self.m == 30:
            self.sent += "ครึ่ง"  # +"นาที"
        elif self.m != 0:
            self.sent += num_to_thaiword(self.m) + "นาที"

    def _type_24hr(self):
        """
        Thai time (24-hour clock)
        """
        self.sent = ""
        self.sent += num_to_thaiword(self.h) + "นาฬิกา"
        if self.m != 0:
            self.sent += num_to_thaiword(self.m) + "นาที"
