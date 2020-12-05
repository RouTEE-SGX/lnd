while read invoice; do
        lncli --network=simnet sendpayment --pay_req=$invoice --force &
done
echo "done"