printf "Starting with 10 nodes........................."
printf "10nodes analysed by ts. Initialized with one customer for one vehicle. Search: Anxious."
python app.py testbench --din ./data/10nodes --metaheu ts --memory 2 --niter 10 --init one2one --search anxious --log CRITICAL --times4ave 100 --maxs 0.2

python app.py testbench --din ./data/10nodes --metaheu ts --memory 5 --niter 10 --init one2one --search anxious --log CRITICAL --times4ave 100 --maxs 0.2

python app.py testbench --din ./data/10nodes --metaheu ts --memory 10 --niter 10 --init one2one --search anxious --log CRITICAL --times4ave 100 --maxs 0.2

python app.py testbench --din ./data/10nodes --metaheu ts --memory 30 --niter 10 --init one2one --search anxious --log CRITICAL --times4ave 100 --maxs 0.2

python app.py testbench --din ./data/10nodes --metaheu ts --memory 100 --niter 10 --init one2one --search anxious --log CRITICAL --times4ave 100 --maxs 0.2

