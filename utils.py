# encoding=gb18030
import datetime
import logging
import os
import shlex
import subprocess
import time



# ��ȡĿ¼�µ������ļ��к��ļ�
def get_files(path):
    global allFileNum

    # �����ļ��У���һ���ֶ��Ǵ�Ŀ¼�ļ���
    dirList = []
    # �����ļ�
    fileList = []
    # ����һ���б������а�����Ŀ¼��Ŀ������(google����)
    files = os.listdir(path)
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # �ų������ļ��С���Ϊ�����ļ��й���
            if (f[0] == '.'):
                pass
            else:
                # ���ӷ������ļ���
                dirList.append(f)
        if (os.path.isfile(path + '/' + f)):
            # �����ļ�
            fileList.append(path + '/' + f)
    # ��һ����־ʹ�ã��ļ����б���һ�����𲻴�ӡ
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
    return fileList,dirList
    # for fl in fileList:
    #     # ��ӡ�ļ�
    #     print '-' * (int(dirList[0])), fl
    #     # ������һ���ж��ٸ��ļ�
    #     allFileNum = allFileNum + 1


# ����logger
def get_logger(log_file_name):
    # ����һ��logger
    logger = logging.getLogger(log_file_name)
    logger.setLevel(logging.DEBUG)
    # ����һ��handler������д����־�ļ�
    fh = logging.FileHandler(log_file_name+".log")
    fh.setLevel(logging.DEBUG)
    # �ٴ���һ��handler���������������̨
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # ����handler�������ʽ
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # ��logger����handler
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# ִ�нű�����
def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """ִ��һ��SHELL����
            ��װ��subprocess��Popen����, ֧�ֳ�ʱ�жϣ�֧�ֶ�ȡstdout��stderr
           ����:
        cwd: ��������ʱ����·����������趨���ӽ��̻�ֱ���ȸ��ĵ�ǰ·����cwd
        timeout: ��ʱʱ�䣬�룬֧��С��������0.1��
        shell: �Ƿ�ͨ��shell����
    Returns: return_code
    Raises:  Exception: ִ�г�ʱ
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    # û��ָ����׼����ʹ�������Ĺܵ�����˻��ӡ����Ļ�ϣ�
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdout=None, shell=shell, bufsize=1)

    # subprocess.poll()����������ӽ����Ƿ�����ˣ���������ˣ��趨�������룬����subprocess.returncode������
    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout��%s" % cmdstring)
    return str(sub.returncode)