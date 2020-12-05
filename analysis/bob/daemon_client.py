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


SERVER_IP = "127.0.0.1"
PORT = 8082


# open socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
client_socket.connect((SERVER_IP, PORT))


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

# encrypt command with (hardcoded) symmetric key
key = bytes([0x0,0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,0x9,0xa,0xb,0xc,0xd,0xe,0xf])

times = []

with open('invoice', 'r') as f:
    lines = f.readlines()

    for line in lines:
        plain = line.split()[0]
        nonce = gen_random_nonce()
        enc_msg, mac = enc(key, nonce, plain.encode('utf-8')) 

        start_time = time.time()

        # send
        # print(len(mac), len(nonce), len(enc_msg))
        client_socket.sendall(mac+nonce+enc_msg)

        # recv
        data = client_socket.recv(1024)

        end_time = time.time()

        print(data.decode())

        times.append(str(end_time - start_time))

with open('net_time', 'w') as f:
    f.write('\n'.join(times))

client_socket.close()

