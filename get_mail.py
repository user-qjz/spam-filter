# -*- coding: utf-8 -*-
import poplib
import base64
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

user_account = '****'  # 填写自己的账号密码
password = '*****'
debuggerForGetMailInformation = True


def get_email_content(server, i):
    rsp, msgLines, msgSize = server.retr(i + 1)
    msg_content = b'\n'.join(msgLines).decode('GBK')
    msg = Parser().parsestr(text=msg_content)
    return msg


def parser_subject(msg):
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)
    print('邮件主题： {0}'.format(value))
    return value


def parser_address(msg):
    hdr, addr = parseaddr(msg['From'])
    # name 发送人邮箱名称， addr 发送人邮箱地址
    name, charset = decode_header(hdr)[0]
    if debuggerForGetMailInformation:
        if charset:
            name = name.decode(charset)
        print('发送人邮箱名称: {0}，发送人邮箱地址: {1}'.format(name, addr))
    print(addr)
    return addr


def parser_content(msg, file):
    content = msg.get_payload()
    # 获取 base64 编码的文本部分
    text = content[0].as_string().split('base64')[-1]
    # 移除可能的额外字符，如空格、换行等
    text = ''.join(text.split())
    # 使用多个编码进行尝试
    charsets_to_try = ['utf-8', 'gb18030', 'gbk']
    decoded_text = None
    for charset in charsets_to_try:
        try:
            temp = base64.urlsafe_b64decode(text.encode())
            decoded_text = temp.decode(charset)
            break  # 如果解码成功，跳出循环
        except (UnicodeDecodeError, base64.binascii.Error):
            continue  # 如果解码失败，尝试下一个编码
    decoded_text = ''.join([char for char in decoded_text if char not in ['\n', '\r']])
    file.write('0	' + decoded_text + '\n')

    return decoded_text


def get_all_email():
    # 邮件服务器地址,以下为网易邮箱
    pop3_server = 'pop.163.com'
    # 开始连接到服务器
    server = poplib.POP3_SSL(pop3_server)
    # 打开或者关闭调试信息，为打开，会在控制台打印客户端与服务器的交互信息
    server.set_debuglevel(1)
    # 打印POP3服务器的欢迎文字，验证是否正确连接到了邮件服务器
    print(server.getwelcome().decode('utf8'))
    # 开始进行身份验证
    server.user(user_account)
    server.pass_(password)
    # 使用list()返回所有邮件的编号，默认为字节类型的串
    rsp, msg_list, rsp_siz = server.list()
    print('邮件总数： {}'.format(len(msg_list)))
    file = open('email_test_input.txt', 'w')
    for i in range(0, len(msg_list)):
        message = get_email_content(server, i)
        # 解析邮件主题
        parser_subject(message)
        parser_address(message)
        parser_content(message, file)
    file.close()
    server.close()


get_all_email()
