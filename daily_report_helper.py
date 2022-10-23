import requests
import json
import os


class DailyReportHelper:

    """
    使用前需要将secureglobaltoken改成自己对应的token，具体拿的方法可以使用fiddler，过期时间的话不确定
    """

    def __init__(self):
        cookie = open(os.path.join(os.path.dirname(__file__), "cookie.txt"), "r").read()
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "com.bjc.app Mozilla/5.0 (Linux; Android 8.0)",
            "secureglobaltoken": cookie,
        }

    def get_context_id(self):
        url = "http://oa.bill-jc.com/api/System/CreateId"
        resp = requests.get(url, headers=self.headers)
        print(resp.text)
        return resp.text

    def get_identity(self):
        headers = {'Content-Type': 'application/json'}
        url = "http://sso.bill-jc.com/api/Secure/GetIdentity"
        param = {"ContextID": self.get_context_id(),
                 "Data": {
                     "Token": self.headers["secureglobaltoken"],
                     "FullUrl": "http://oa.bill-jc.com/timesheet/?v=3.0.6/#/",
                     "ApplicationID": "HOST"}}
        resp = requests.post(url, headers=headers, data=json.dumps(param))
        print(resp.text)

    def report(self, date_string="2022-10-20"):
        url = "http://api-cloud.bill-jc.com/TimeSheet/api/DailyReport/Save"
        payload = {
            "ContextID": self.get_context_id(),
            "Data": {
                "ID": "",
                "Date": date_string,
                "WorkID": "B-54545",
                "WorkName": "郑佳诚",
                "DeptID": 1869,
                "DeptName": "ISBG-BU1-交付管理部-资源部",
                "WorkItems": [
                        {
                            "ID": "",
                            "JobType": "A1-交付",
                            "FirstType": "开发",
                            "SecondType": "后台开发",
                            "Ratio": "100",
                            "Remark": "",
                            "DeptName": "",
                            "ProjectID": "D-202209-17888",
                            "ProjectName": "FY23-基础产品-非混合云Q3",
                            "ApproverWorkID": "B-12347",
                            "ApproverWorkName": "张冲冲",
                            "WorkTypeID": 86,
                            "RecordList": []
                        }
                ],
                "IsSubmit": True
            }
        }
        headers = {
              'secureglobaltoken': self.headers["secureglobaltoken"],
              'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        print(response.text)


if __name__ == '__main__':
    helper = DailyReportHelper()
    year, month = 2022, 10
    # 用于过滤节假日和周末
    date_filter = []

    # for i in range(1, )
    helper.report()

    # todo 增加对节假日的自动过滤
