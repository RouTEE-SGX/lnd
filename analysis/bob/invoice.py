import os
import subprocess
import ast
import time
import sys
from tqdm import tqdm


if len(sys.argv) != 2:
    print("Insufficient arguments: Required one extra integer.")
    sys.exit()

# env
os.system('export DOCKER_HOST="tcp://147.46.115.173:8081" && export NETWORK="simnet"')

# run
# res = os.systeim("docker exec -it bob lncli --network=simnet addinvoice --amt=10")
# print(res)

rounds = sys.argv[1]
invoices_times = []
for _ in tqdm(range(int(rounds))):
    start_time = time.time()
    res = subprocess.check_output('docker exec -it bob lncli --network=simnet addinvoice --amt=10', shell=True)
    end_time = time.time()

    elapsed_time = end_time - start_time

    res_dict = ast.literal_eval(res.decode('UTF-8'))
    invoice = res_dict['payment_request']

    invoices_times.append(str(invoice) + '\t' + str(elapsed_time))

with open('invoice', 'w') as f:
    f.write('\n'.join(invoices_times))

