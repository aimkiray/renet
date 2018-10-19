#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/14
# @Author  : aimkiray


import winreg as registry
import os
import sys
import threading
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer

# A value of 3 mean use manual settings
# A value of 5 mean use pac settings
# A value of 9 mean use automatic settings
# A value of 1 means it is not enabled

key = registry.OpenKey(registry.HKEY_CURRENT_USER,
                       "Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections", 0,
                       registry.KEY_ALL_ACCESS)

my_pac_proxy = b'F\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00.\x00\x00\x00http=10.158.100.9:8080;https=10.158.100.9:8080\x07\x00\x00\x00<local>'

my_ip_proxy = b'F\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00'

my_bak_proxy = b'F\x00\x00\x00\x00\x00\x00\x00\x09\x00\x00\x00'

local_port = 2333


def query_key():
    return registry.QueryValueEx(key, "DefaultConnectionSettings")


def monitor_key(key_name, proxy_type):
    value, regtype = query_key()
    if regtype == registry.REG_BINARY:
        if key_name.encode() not in value or not proxy_type == value[8]:
            return False
    return True


def prepare_my_proxy(raw):
    if 'http' in raw:
        pac_path = bytes(raw, encoding="utf-8")
        final_pac_proxy = my_pac_proxy + bytes([len(pac_path)]) + b'\x00\x00\x00' + pac_path
    else:
        ip_proxy = 'http=' + raw + ';https=' + raw
        ip_path = bytes(ip_proxy, encoding="utf-8")
        final_pac_proxy = my_ip_proxy + bytes([len(
            ip_path)]) + b'\x00\x00\x00' + ip_path + b'\x07\x00\x00\x00<local>(\x00\x00\x00http://proxyconf.glb.nokia.com/proxy.pac'
    return final_pac_proxy


def exec_change(value):
    if value:
        registry.SetValueEx(key, "DefaultConnectionSettings", None, registry.REG_BINARY, value)
        # TODO Once modified, it may probably not change within half an hour


def load_pac_file_path():
    current_path = os.path.abspath(__file__)
    pac_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep), 'renet.pac')
    return 'file:///' + pac_file_path.replace('\\', '/')


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def start_server(port, file_dir):
    # Change the current thread root directory
    os.chdir(file_dir)
    server = ThreadingSimpleServer(('127.0.0.1', port), SimpleHTTPRequestHandler)
    try:
        while True:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print("\nShutting down server per users request.")
    except Exception as e:
        print(e)


def run_server(port, path):
    file_dir = os.path.dirname(path)
    # start file server
    threading.Thread(target=start_server, args=(int(port), file_dir,)).start()


# def load_pac_http_path(port):
#     # get ip
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#     return 'http://' + ip + ':' + str(port) + '/renet.pac'


if __name__ == '__main__':

    run_server(2333, r"C:\Users\sunzhang\Desktop\Tools\proxy.md")
    # start_server(local_port, pac_dir)
    pac_proxy = prepare_my_proxy('http://127.0.0.1:' + str(local_port) + '/renet.pac')
    exec_change(pac_proxy)
    while True:
        monitor_key()
