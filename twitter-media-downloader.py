'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2023-01-15 23:44:15
LastEditors: mengzonefire
Description: 程序主函数入口
'''
from common.console import cmdMode, startCrawl
from common.exceptHandler import except_handler
from common.tools import *


def main():
    exe_path, _ = os.path.split(sys.argv[0])
    if exe_path:
        os.chdir(exe_path)  # 切换工作目录到程序根目录
    initalArgs()
    getEnv()
    if len(sys.argv) == 1:  # 命令行参数为空 -> 双击运行程序
        print('version: {}\ndonate page: {}\nissue page: {}\n'.format(
            version, donate_page, issue_page))
        getProxy()
        checkUpdate()
        getHeader()
        cmdMode(clearScreen=False)
    else:
        argsHandler()
        getProxy()
        getHeader()
        startCrawl(getContext('args').url)
    saveEnv()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        except_handler(e)
        if len(sys.argv) == 1 and input(reset_ask):
            if sys.platform in ['win32', 'win64']:  # 判断是否为win平台
                os.system('cls')
            else:
                os.system('clear')
            main()
