# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:XieCheng
# datetime:2024-12
# software: PyCharm
"""
基于imgocr的证件ocr文字识别，具体识别对象是身份证
特点-轻量化，效果也可以，缺点，相较于paddleocr差一点点
"""

from imgocr import ImgOcr
import re

from fastapi import FastAPI, File, UploadFile, Form
import uvicorn

import warnings
warnings.filterwarnings("ignore")


ocr = ImgOcr(use_gpu=False, is_efficiency_mode=True)


def identify_info_country(image):
    result_list = []
    result = ocr.ocr(image, cls=True)
    for idx, res in enumerate(result):
        result_list.append(res["text"])

    result_str = " ".join([i for i in result_list]) + " "
    print("--->", result_str)

    organization, start_date, end_date = "", "", ""

    if re.search(re.compile("签发机关(.*?)有效期限"), result_str):
        organization = re.search(re.compile("签发机关(.*?)有效期限"), result_str).group(1)

    pattern = re.compile('有效期限(.*\d{4}[\. 。]?\d{1,2}[\. 。]?\d{1,2}) ')
    if re.search(pattern, result_str):
        period_of_validity = re.search(pattern, result_str).group(1)
        start_date = period_of_validity.split("-")[0].strip()
        end_date = period_of_validity.split("-")[1].strip()

    output = {"organization": organization,
              "start_date": start_date,
              "end_date": end_date}
    output = {k: v.replace(" ", "").strip() for k, v in output.items()}

    return output


def identify_info_portrait(image):
    result_list = []
    result = ocr.ocr(image, cls=True)
    for idx, res in enumerate(result):
        result_list.append(res["text"])

    result_str = " ".join([i for i in result_list]) + " "
    print("--->", result_str)

    name, gender, nation, birth, address = "", "", "", "", ""

    if re.search(re.compile("姓名(.*?)性别"), result_str):
        name = re.search(re.compile("姓名(.*?)性别"), result_str).group(1)

    if re.search(re.compile("性别(.*?)民族"), result_str):
        gender = re.search(re.compile("性别(.*?)民族"), result_str).group(1)

    if re.search(re.compile("民族(.*?)出生"), result_str):
        nation = re.search(re.compile("民族(.*?)出生"), result_str).group(1)

    if re.search(re.compile('\d{4}年\d{1,2}月\d{1,2}日'), result_str):
        birth = re.search(re.compile('\d{4}年\d{1,2}月\d{1,2}日'), result_str).group()

    if re.search(re.compile("住址(.*?)公民"), result_str):
        address = re.search(re.compile("住址(.*?)公民"), result_str).group(1)

    if re.search(re.compile("\d{17}[\dx]|\d{15}"), result_str):
        id_number = re.search(re.compile("\d{17}[\dx]|\d{15}"), result_str).group()
    else:
        id_number = ""

    output = {"name": name, "gender": gender, "nation": nation,
              "birth": birth, "address": address, "id_number": id_number}
    output = {k: v.replace(" ", "").strip() for k, v in output.items()}

    return output


app = FastAPI()


@app.post("/ocr")
async def id_card_ocr(file: UploadFile = File(...), type_of_card: int = Form(...)):
    image_data = await file.read()
    if int(type_of_card) == 1:
        result = identify_info_country(image_data)
    elif int(type_of_card) == 2:
        result = identify_info_portrait(image_data)
    else:
        result = dict()
    return result


if __name__ == "__main__":
    """ api run """
    uvicorn.run(app, host="0.0.0.0", port=20005)
