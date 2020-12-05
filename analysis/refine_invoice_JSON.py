import json

FILE_NAME = './invoice10000'

invoices = []
with open(FILE_NAME, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if 'payment_request' in line:
            invoice = line.split()[1][1:-2]
            # print(invoice)
            invoices.append(invoice)

with open(FILE_NAME + '_refined', 'w') as f:
    # print('\n'.join(invoices))
    f.write('\n'.join(invoices))
