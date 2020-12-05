round=`expr $1 - 1`
for i in `seq 1 1 $round`; do
        lncli --network=simnet addinvoice --amt=10 &
done
lncli --network=simnet addinvoice --amt=10