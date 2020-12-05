import os
import subprocess
import ast
import time
import sys
from tqdm import tqdm

import socket
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15


SERVER_IP = "0.0.0.0"
PORT = 8082


# open socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# for WinError 10048
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# run server
server_socket.bind((SERVER_IP, PORT))
server_socket.listen()


client_socket, addr = server_socket.accept()
# print('Connected by', addr)


NONCE_SIZE = 12 # bytes


# generate random nonce (= Initialization Vector, IV)
def gen_random_nonce():
    return get_random_bytes(NONCE_SIZE)


# AES-GCM encryption
def enc(key, nonce, plain_data):
    # AES-GCM cipher
    cipher = AES.new(key, AES.MODE_GCM, nonce)

    # encrypt plain data & get MAC tag
    cipher_data = cipher.encrypt(plain_data)
    mac = cipher.digest()

    return cipher_data, mac


# AES-GCM decryption
def dec(key, nonce, cipher_data, mac):
    # AES128-GCM cipher
    cipher = AES.new(key, AES.MODE_GCM, nonce)

    try:
        # try decrypt
        plain_data = cipher.decrypt_and_verify(cipher_data, mac)
        return plain_data
    except ValueError:
        # ERROR: wrong MAC tag, data is contaminated
        return None


# env
os.system('export DOCKER_HOST="tcp://147.46.115.173:8081" && export NETWORK="simnet"')

key = bytes([0x0,0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,0x9,0xa,0xb,0xc,0xd,0xe,0xf])

times = []
while True:
    data = client_socket.recv(1024)

    if not data:
        break

    mac = data[:16]
    nonce = data[16:16+12]
    enc_msg = data[16+12:]

    plain = dec(key, nonce, enc_msg, mac)

    try:
        invoice = plain.decode('utf-8')

        cmd = 'docker exec -it alice lncli --network=simnet sendpayment --pay_req=' + invoice + ' --force'

        start_time = time.time()
        res = subprocess.check_output(cmd, shell=True)
        end_time = time.time()

        times.append(str(end_time - start_time))

        print(res)

        client_socket.sendall(res)
    except:
        pass

with open('payment', 'w') as f:
    f.write('\n'.join(times))

client_socket.close()
server_socket.close()

