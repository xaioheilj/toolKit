# -*- coding:utf-8 -*-
import os
import shutil
import time
from PIL import Image
from PIL import ImageFile
from datetime import datetime


def copyFile(sourcePath, savePath):
    image_end = ['.jpg', '.JPG', '.PNG', '.png', '.jpeg', '.JPEG']
    for dir_or_file in os.listdir(sourcePath):
        filePath = os.path.join(sourcePath, dir_or_file)
        if os.path.isfile(filePath):  # 判断是否为文件
            if os.path.splitext(os.path.basename(filePath))[
                1] in image_end:  # 如果文件是图片，则复制，如果都是同一种图片类型也可以用这句：if os.path.basename(filePath).endswith('.jpg'):
                print('this copied pic name is ' + os.path.basename(filePath))  # 拷贝jpg文件到自己想要保存的目录下
                shutil.copyfile(filePath, os.path.join(savePath, os.path.basename(filePath)))
            else:
                continue
        elif os.path.isdir(filePath):  # 如果是个dir，则再次调用此函数，传入当前目录，递归处理。
            copyFile(filePath, savePath)
        else:
            print('not file and dir ' + os.path.basename(filePath))



# 压缩图片文件
def compress_image(outfile, mb=2048, quality=85, k=0.9):  # 通常你只需要修改mb大小
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param k: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """

    o_size = os.path.getsize(outfile) // 1024  # 函数返回为字节，除1024转为kb（1kb = 1024 bit）
    print('before_size:{} after_size:{}'.format(o_size, mb))
    if o_size <= mb:
        return outfile

    ImageFile.LOAD_TRUNCATED_IMAGES = True  # 防止图像被截断而报错

    # now = datetime.now()  # 获得当前时间
    # timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
    # filename1 = timestr
    #

    while o_size > mb:
        im = Image.open(outfile)
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Image.Resampling.LANCZOS)  # 最后一个参数设置可以提高图片转换后的质量
        try:
            out.save(outfile, quality=quality)  # quality为保存的质量，从1（最差）到95（最好），此时为85
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024

    # now = datetime.now()  # 获得当前时间
    # timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
    # filename1 = timestr

    return outfile

if __name__=="__main__":


    time_now = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    sourcePath = "D:\\Picture\\ImageCompress\\"
    #path1 = sourcePath + "\\" + "Copy"
    # savePath = "D:\\Picture\\ImageCompress\\Copy\\"
    savePath = sourcePath + '\\' + time_now + '\\'
    os.makedirs(savePath)
    copyFile(sourcePath, savePath)

    #path = r'D:\Picture\ImageCompress\\'  # 待压缩图片文件夹
    for img in os.listdir(savePath):
        compress_image(savePath + str(img))