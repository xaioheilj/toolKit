
# encoding:utf-8
# !/usr/bin/python3
import requests
import os
import base64
import winreg
import xlsxwriter
from datetime import datetime



class ID_OCR:
    # 要求base64编码和urlencode后大小不超过4M，最短边至少15px，最长边最大4096px, 支持jpg / jpeg / png / bmp格式
    def __init__(self, client_id, client_secret):


        self.request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard"
        self.client_id = 'aOGGacEadRLxIV2I7L5It9ET'
        self.client_secret = 'LVgMIzUzTvUrmEXAQ8qbZ68FVzCCL77d'
        self.token = self.get_token()
        self.file_list = []

    # 获取token
    def get_token(self):
        hosts = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            self.client_id, self.client_secret)
        res = requests.get(hosts)
        return res.json().get("access_token") if res else None

    # 遍历所有文件及子文件下的图片
    def getFileList(self, dirs, ext=None):
        """
        输入 dir：文件夹根目录
        输入 ext: 扩展名
        """
        if os.path.isfile(dirs):
            if ext is None:
                self.file_list.append(dirs)
            else:
                if ext in dirs[-3:]:
                    self.file_list.append(dirs)

        elif os.path.isdir(dirs):
            for s in os.listdir(dirs):
                newDir = os.path.join(dirs, s)
                self.getFileList(newDir, ext)

    # 获取本地桌面路径
    @staticmethod
    def get_desktop():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]

    # 写入excel
    def white_excel(self, file_name):
        url = self.get_desktop() + file_name  # 桌面路径与文件名相加

        workbook = xlsxwriter.Workbook(url)  # 新建excel表,可写不使用以上函数自己写入要保存的路径

        worksheet = workbook.add_worksheet()  # 新建sheet,也可设置为sheet的名称为"sheet1"等自定义字段

        headings = ['银行卡号']  # 设置表头数据

        worksheet.write_row('A1', headings)  # 插入表头

        for i in range(2, len(self.file_list) + 2):  # 遍历file_list
            data = self.post_api(self.file_list[i - 2])  # 调用self.post_api获取data
            worksheet.write_row("A" + str(i), data)  # 写入一行
        workbook.close()  # 将excel文件保存关闭

    # 调用api
    def post_api(self, img_url):
        """
        :param img_url: 图片路径
        :return: 列表 ，内容为【"姓名","民族","住址","性别","公民身份号码"】
        """
        f = open(img_url, 'rb')  # 打开文件
        img = base64.b64encode(f.read())  # 以二进制的形式打开图片
        # params = {"id_card_side": "front", "image": img}  # 写入body参数,front代表正面
        params ={"image": img}
        request_url = self.request_url + "?access_token=" + self.token  # 修改请求url
        headers = {'content-type': 'application/x-www-form-urlencoded'}  # 写入headers参数
        response = requests.post(request_url, data=params, headers=headers)  # 发送post请求并获取响应
        data = []
        if response:
            print(response.json())
            try:
                bankcard_number = response.json().get("result").get("bank_card_number")

                #                 # name = response.json().get("get("姓名").get("words")
                # birth = response.json().get("words_result").get("出生").get("words")
                # mz = response.json().get("words_result").get("民族").get("words")
                # zz = response.json().get("words_result").get("住址").get("words")
                # xb = response.json().get("words_result").get("性别").get("words")
                # sfz = response.json().get("words_result").get("公民身份号码").get("words")
                # data = [name,birth, mz, xb, zz, sfz]
                data = [bankcard_number]
            except:
                pass
        return data

    def run(self, file_url, filename="/new_excel.xlsx", ext=None):
        # 获取文件夹及其子文件夹下所有的图片
        self.getFileList(file_url, ext)
        # 写入excel
        self.white_excel(filename)


if __name__ == '__main__':
    # client_id 为官网获取的AK， client_secret 为官网获取的SK 两参数为必传
    p1 = ID_OCR(client_id="client_id", client_secret="client_secret")
    """
    file_url  必传：存放图片的文件夹，可写相对路径和绝对路径
    filename  选传：生成的excel的名字，默认为"/new_excel.xlsx"
    ext       选传：文件夹下图片的类型，默认为全部类型
    """

    now = datetime.now()  # 获得当前时间
    timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
    filename1 = timestr
    p1.run(file_url="D://Picture/BankCard/", filename='/'+filename1, ext="")