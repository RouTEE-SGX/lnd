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

for _ in tqdm(range(10000)):
    # Hardcoded
    plain = "lnsb100n1p0ujehypp529d8d42ntf6n3htq3m7hpfn24nz0y64lp0v2wdcj4dvjkg4g9n3sdqqcqzpgsp5jhm0lx6qtzx32dsjmuuyyvvqmn0pdzxtewu70vxtr8nkg94g5vds9qy9qsqcgzx7wzweumj2r6ex5aupswwh97l9wdyyawmlwjwpm4kjf7yh8532q4jt2ux3uwxxxytvn2kyulx637kpdjhev64cek3hcduyszvkzcqngh3ye"
    nonce = gen_random_nonce()
    enc_msg, mac = enc(key, nonce, plain.encode('utf-8')) 

    start_time = time.time()

    # send
    client_socket.sendall(mac+nonce+enc_msg)

    # recv
    data = client_socket.recv(1024)

    end_time = time.time()

    # print(data.decode())

    times.append(str(end_time - start_time))

print(sum([float(time) for time in times]) / 10000.)

with open('travel_cost', 'w') as f:
    f.write('\n'.join(times))

client_socket.close()

