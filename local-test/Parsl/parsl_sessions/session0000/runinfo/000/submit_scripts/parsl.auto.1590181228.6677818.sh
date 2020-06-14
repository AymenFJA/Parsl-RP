
export CORES=$(getconf _NPROCESSORS_ONLN)
echo "Found cores : $CORES"
WORKERCOUNT=1

CMD ( ) {
process_worker_pool.py --debug --max_workers=3 -p 0 -c 1 -m None --poll 10 --task_url=tcp://127.0.0.1:54469 --result_url=tcp://127.0.0.1:54045 --logdir=/home/aymen/SummerRadical/Parsl-RP/local-test/runinfo/000/htex_Local --block_id=0 --hb_period=30 --hb_threshold=120 
}
for COUNT in $(seq 1 1 $WORKERCOUNT)
do
    echo "Launching worker: $COUNT"
    CMD &
done
wait
echo "All workers done"
