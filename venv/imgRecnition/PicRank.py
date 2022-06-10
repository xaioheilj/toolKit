import os
import exifread


path = "D:\\Picture\\IDCard\\"
def reNameByTime(path):
    mlist = []
    # 获取文件名列表
    files = os.listdir(path)

    # 获得名称带时间戳的新文件名列表
    for filename in files:
        # 获得文件的最后修改时间
        modifytimes = os.path.getmtime(path + filename)
        filename_lower = filename.lower()
        # 筛选.jpg格式
        if '.jpg' in filename_lower:   #'.JPG', '.PNG', '.png', '.jpeg', '.JPEG')
            mlist.append(str(int(modifytimes)) + "-" + filename)  # .jpg

    mlist = sorted(mlist)

    # 遍历修改时间戳为序号
    for i in range(len(mlist)):

        # 截取获得原先的文件名
        oldname = mlist[i][11:]  # 切片操作，从11至后

        # 将时间戳部分修改为序号，得到新的文件名
        if (i + 1) < 10:  # 0-9
            newname = "000" + str(i + 1) + ".jpg"
        elif (i + 1) > 9 and (i + 1) < 100:  # 10-100
            newname = "00" + str(i + 1) + ".jpg"
        elif (i + 1) > 99 and (i + 1) < 1000:  # 100-1000
            newname = "0" + str(i + 1) + ".jpg"
        else:
            newname = str(i + 1) + ".jpg"  # 1000 - 9999

        #        print(newname, oldname)

        # 重命名文件，按修改时间排序并加序号前缀
        os.rename(path + oldname, path + newname)


# 如果想执行py文件，可以将后缀改为“.py”，如果想打包成exe，需要将后缀改为“.exe”
if __name__ == "__main__":
    filepath = os.sys.argv[0].replace("rename.py", "")
    print(os.sys.argv[0])
    reNameByTime(filepath)