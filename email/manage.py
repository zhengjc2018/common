# -*- coding: UTF-8 -*-
import os
import pandas as pd
import numpy as np
import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class EmailFactory:
    def __init__(self, email_df):
        self.recivers = email_df
        self.title = "哈哈哈哈"  # 标题
        self.content = ""  # 发送内容
        self.sys_sender = 'xxxxx@qq.com'  # 系统账户
        self.sys_pwd = ''  # 系统账户密码

    def send(self, file_name, address):
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['From'] = self.sys_sender
        msg['To'] = address
        msg['Subject'] = self.title
        msg.attach(MIMEText(self.content, 'plain', 'utf-8'))

        file_part = MIMEApplication(open("%s.txt" % file_name, 'rb').read())
        file_part.add_header('Content-Disposition',
                             'attachment', filename='%s.txt' % file_name)
        msg.attach(file_part)

        # SMTP服务器
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)
        server.login(self.sys_sender, self.sys_pwd)
        server.sendmail(self.sys_sender, [address, ], msg.as_string())
        # 退出账户
        server.quit()

    def run(self):
        for (teacher, address) in self.recivers:
            try:
                self.send(teacher, address)
                print("send to %s: %s success" % (teacher, address))
            except Exception as e:
                print("send to %s: %s fail, error: %s" %
                      (teacher, address, str(e)))


def run():
    email_df_new = ["xxxxx@qq.com"]
    obj = EmailFactory(email_df_new)
    obj.run()


if __name__ == "__main__":
    run()
