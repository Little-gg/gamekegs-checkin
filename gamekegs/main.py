#!/usr/bin/env python
# coding=utf-8

"""
Author: Little-gg <little.gg.talk@gmail.com>
Date: 2022-01-06 09:59:37
LastEditors: Chen GuanJi
LastEditTime: 2022-01-06 10:00:53
FilePath: /gamekegs-checkin/checkin.py

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT

"""
import os
import json
import requests
import urllib3
from dailycheckin import CheckIn

urllib3.disable_warnings()


class Gamekegs(CheckIn):
    name = "游戏大桶"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(session):
        msg = []
        data = {"action": "user.checkin"}
        # data = {}
        response = session.post(
            url="https://gamekegs.com/wp-content/themes/modown/action/user.php",
            data=data,
            verify=False,
        )
        if response.status_code != 200:
            return "返回不为200，签到失败，请查找原因"
        elif not response.json():
            return "返回为空，签到失败，请查找原因"
        else:
            r = response.json()
            if r.get("error"):
                # 失败
                raise Exception(response.json().get("msg"))
            else:
                msg += [
                    {"name": "签到结果", "value": "成功"},
                    {"name": "日志", "value": response.json().get("msg")},
                ]
            return msg

    def main(self):
        cookie = {
            item.split("=")[0]: item.split("=")[1]
            for item in self.check_item.get("cookie").split("; ")
        }
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, cookie)
        session.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        )
        msg = self.sign(session=session)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"),
        "r",
        encoding="utf-8",
    ) as f:
        datas = json.loads(f.read()).get
    _check_item = datas.get("GAMEKEGS", [])[0]
    print(Gamekegs(check_item=_check_item).main())
