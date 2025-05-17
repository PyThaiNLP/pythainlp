# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2016-2025 PyThaiNLP Project
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

def convert_currency(value: float, from_unit: str) -> dict:
    """
    Convert ancient Thai currency to other units

    * เบี้ย (Bia)
    * อัฐ (At)
    * ไพ (Pi)
    * เฟื้อง (Feuang)
    * สลึง (Saleung)
    * บาท (Bath)
    * ตำลึง (Tamleung)
    * ชั่ง (Chang)

    See more:
        `Thai money <https://en.wikipedia.org/wiki/History_of_Thai_money>`_.

    :param float value: value
    :param str from_unit: currency unit \
        ('เบี้ย', 'อัฐ', 'ไพ', 'เฟื้อง', 'สลึง', 'บาท', 'ตำลึง', 'ชั่ง')
    :return: Thai currency
    :rtype: dict

    :Example:
    ::

        from pythainlp.ancient import convert_currency

        print(convert_currency(8, "บาท"))
        # output:
        # {
        #  'เบี้ย': 51200.0,
        #  'อัฐ': 512.0,
        #  'ไพ': 256.0,
        #  'เฟื้อง': 64.0,
        #  'สลึง': 32.0,
        #  'บาท': 8.0,
        #  'ตำลึง': 2.0,
        #  'ชั่ง': 0.1
        # }
    """
    conversion_factors_to_att = {
        'เบี้ย': 1,
        'อัฐ': 100,  # 1 อัฐ = 100 เบี้ย
        'ไพ': 2 * 100,  # 1 ไพ = 2 อัฐ
        'เฟื้อง': 4 * 2 * 100,  # 1 เฟื้อง = 4 ไพ
        'สลึง': 2 * 4 * 2 * 100,  # 1 สลึง = 2 เฟื้อง
        'บาท': 4 * 2 * 4 * 2 * 100,  # 1 บาท = 4 สลึง
        'ตำลึง': 4 * 4 * 2 * 4 * 2 * 100,  # 1 ตำลึง = 4 บาท
        'ชั่ง': 20 * 4 * 4 * 2 * 4 * 2 * 100,  # 1 ชั่ง = 20 ตำลึง
    }

    if from_unit not in conversion_factors_to_att:
        raise NotImplementedError(
            f"Currency unit '{from_unit}' is not support."
        )

    # start from 'อัฐ'
    value_in_att = value * conversion_factors_to_att[from_unit]

    # Calculate values ​​in other units
    results = {}
    for unit, factor in conversion_factors_to_att.items():
        results[unit] = value_in_att / factor

    return results
