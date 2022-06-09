import os
from PIL import Image
from PIL import ImageFile
from datetime import datetime
import shutil


#备份图片
# 复制图像到另一个文件夹
# 文件所在文件夹
file_dir = 'D:\Picture\ImageCompress'
# 创建一个子文件存放文件
name = 'class'

file_list = os.listdir(file_dir)

for image in file_list:

    #如果图像名为B.png 则将B.png复制到F:\\Test\\TestA\\class
    if image:
        if os.path.exists(os.path.join(file_dir,'class_name')):
            shutil.copy(os.path.join(file_dir,image), os.path.join(file_dir, 'class_name'))
        else:
            os.makedirs(os.path.join(file_dir,'class_name'))
            shutil.copy(os.path.join(file_dir, image), os.path.join(file_dir, 'class_name'))


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

    while o_size > mb:
        im = Image.open(outfile)
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)  # 最后一个参数设置可以提高图片转换后的质量
        try:
            now = datetime.now()  # 获得当前时间
            timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
            filename1 = timestr
            out.save(outfile+os.mkdir("/filename1"), quality=quality)  # quality为保存的质量，从1（最差）到95（最好），此时为85
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024

    now = datetime.now()  # 获得当前时间
    timestr = now.strftime("%Y_%m_%d_%H_%M_%S")
    filename1 = timestr

    return outfile

if __name__=="__main__":
    path = r'D:\\Picture\\ImageCompress\\class_name'  # 待压缩图片文件夹
    for img in os.listdir(path):
        compress_image(path + str(img))