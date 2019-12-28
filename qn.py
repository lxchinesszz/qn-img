from qiniu import Auth, put_file, etag
from prettytable import PrettyTable
import argparse
import hashlib
import time
from colorama import init, Fore, Back

class Color:
    @staticmethod
    def red(s,isLight = False):
        if not isLight:
            return Fore.RED + s + Fore.RESET
        return Fore.LIGHTRED_EX + s + Fore.RESET

    @staticmethod
    def green(s,isLight = False):
        if not isLight:
            return Fore.GREEN + s + Fore.RESET
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    @staticmethod
    def yellow(s,isLight = False):
        if not isLight:
            return Fore.YELLOW + s + Fore.RESET
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    @staticmethod
    def white(s,isLight = False):
        if not isLight:
            return Fore.WHITE + s + Fore.RESET
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    @staticmethod
    def blue(s,isLight = False):
        if not isLight:
            return Fore.BLUE + s + Fore.RESET
        return Fore.LIGHTBLUE_EX + s + Fore.RESET

    @staticmethod
    def black(s,isLight = False):
        if not isLight:
            return Fore.BLACK + s + Fore.RESET
        return Fore.LIGHTBLACK_EX + s + Fore.RESET

def fileByLocation(fileLocation):
    '''从完整的路径名计算出文件名'''
    if fileLocation.count('/') > 0:
        return fileLocation.split('/')[-1]
    else:
        return fileLocation


def fileNameEncode(fileName):
    '''文件名加密,使用md算法'''
    index = fileName.index('.')
    fileEncode = hashlib.md5(fileName[0:index].encode(encoding='UTF-8')).hexdigest()
    suffix = fileName[index:]
    return fileEncode + suffix

def checkBucketName(bucket_name):
    if not bucket_name:
        return "springlearn"
    return bucket_name

parser = argparse.ArgumentParser(description="图床工具")
parser.add_argument('-i', '--imgLocation', type=str, help='文件地址')
parser.add_argument('-b', '--bucket_name', type=str, help='bucket_name')
args = parser.parse_args()
bucket_name = checkBucketName(args.bucket_name)
# 文件的完整路径
fileLocation = args.imgLocation
# 根据文件路径获取文件名
fileName = fileByLocation(fileLocation)
# 对文件名进行加密
key = fileNameEncode(fileName)

access_key = '使用自己的'
secret_key = '使用自己的'


q = Auth(access_key, secret_key)
token = q.upload_token(bucket_name, key, 3600)
ret, info = put_file(token, key, fileLocation)


base_table_head = ["文件名", "加密文件名", "上传路径", "外链", "时间","成功"]
table = PrettyTable(base_table_head)
raw = list()
raw.append(fileName)
raw.append(key)
raw.append(fileLocation)
raw.append("https://img.springlearn.cn/{0}".format(key))
raw.append(time.strftime('%Y-%m-%d %H:%M:%S'))
raw.append(info.ok())
table.add_row(raw)
print(Color.green(str(table)))%
