# -*- coding: utf-8 -*-
"""
cron: 30 8 * * *
new Env('哈啰单车');
"""
import requests
from requests import utils

from utils import check
import json


class Hldc(object):
    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(session, data):
        response = session.post(url="https://api.hellobike.com/api?common.welfare.signAndRecommend",
                                data=json.dumps(data)).json()
        msg = response
        try:

            if msg.get("data").get("didSignToday"):
                msg = [
                    {"name": "今日签到福利金：", "value": msg.get("data").get("bountyCountToday")}
                ]
            else:
                msg = [
                    {"name": "签到信息", "value": "签到出现问题"}
                ]
            return msg
        except Exception as e:
            print(f"错误信息: {e}")
            return [{"name": "签到信息", "value": "签到出现问题"}]

    def main(self):
        hldc_token = self.check_item.get("token")
        session = requests.session()
        session.headers.update(
            {
                "Host": "api.hellobike.com",
                "Content-Type": "application/json",
                "Origin": "https://m.hellobike.com",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "requestId": "3q1szjBg98dT7jM",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148; app=easybike;",
                "version": "6.16.1",
                "Referer": "https://m.hellobike.com/",
                "Content-Length": "147",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",

            }
        )
        data = {
            "platform": 4,
            "version": "6.16.1",
            "action": "common.welfare.signAndRecommend",
            "systemCode": 61,
            "token": hldc_token,
            "from": "h5"
        }
        msg = self.sign(session=session, data=data)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


@check(run_script_name="哈啰单车",run_script_expression="hldc|哈啰单车")
def main(*args, **kwargs):
    return Hldc(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()
