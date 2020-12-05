import json

total_net_times = 0
with open('./travel_cost', 'r') as f:
    lines = f.readlines()
    len_net_times = len(lines)
    for line in lines:
        total_net_times += float(line)

print("net + payment:\t", total_net_times / len_net_times)
# exit()

total_invoice_times = 0
with open('./invoice', 'r') as f:
    lines = f.readlines()
    len_invoice = len(lines)
    for line in lines:
        total_invoice_times += float(line.split()[1])

print("invoice:\t", total_invoice_times / len_invoice)

print(">>> total:\t", total_net_times / len_net_times + total_invoice_times / len_invoice)
