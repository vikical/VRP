printf "Starting with 10 nodes........................."
printf "10nodes analysed by ls,vnd,bvns,ts. Initialized with one customer for one vehicle. Search: Anxious."
python app.py testbench --din ./data/10nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init one2one --search anxious --log CRITICAL --times4ave 100 --maxs 0.2

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized with one customer for one vehicle. Search: Greedy."
python app.py testbench --din ./data/10nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init one2one --search greedy --log CRITICAL --times4ave 100 --maxs 0.2

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized randomly. Search: Anxious."
python app.py testbench --din ./data/10nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init random --search anxious --log CRITICAL --times4ave 100 --maxs 0.2

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized randomly. Search: Greedy."
python app.py testbench --din ./data/10nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init random --search greedy --log CRITICAL --times4ave 100 --maxs 0.2

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized sequentially in groups. Search: Anxious."
python app.py testbench --din ./data/10nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init group --search anxious --log CRITICAL --times4ave 100 --maxs 0.2

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized sequentially in groups. Search: Greedy."
python app.py testbench --din ./data/10nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init group --search greedy --log CRITICAL --times4ave 100 --maxs 0.2

printf "Starting with 30 nodes........................."
python app.py testbench --din ./data/30nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init one2one --search anxious --log CRITICAL --times4ave 100 --maxs 1

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized with one customer for one vehicle. Search: Greedy."
python app.py testbench --din ./data/30nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init one2one --search greedy --log CRITICAL --times4ave 100 --maxs 1

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized randomly. Search: Anxious."
python app.py testbench --din ./data/30nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init random --search anxious --log CRITICAL --times4ave 100 --maxs 1

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized randomly. Search: Greedy."
python app.py testbench --din ./data/30nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init random --search greedy --log CRITICAL --times4ave 100 --maxs 1

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized sequentially in groups. Search: Anxious."
python app.py testbench --din ./data/30nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init group --search anxious --log CRITICAL --times4ave 100 --maxs 1

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized sequentially in groups. Search: Greedy."
python app.py testbench --din ./data/30nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init group --search greedy --log CRITICAL  --times4ave 100 --maxs 1

printf "Starting with 50 nodes........................."
python app.py testbench --din ./data/50nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init one2one --search anxious --log CRITICAL  --times4ave 1 --maxs 10

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized with one customer for one vehicle. Search: Greedy."
python app.py testbench --din ./data/50nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init one2one --search greedy --log CRITICAL  --times4ave 1 --maxs 10

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized randomly. Search: Anxious."
python app.py testbench --din ./data/50nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init random --search anxious --log CRITICAL  --times4ave 1 --maxs 10

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized randomly. Search: Greedy."
python app.py testbench --din ./data/50nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init random --search greedy --log CRITICAL --times4ave 1 --maxs 10

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized sequentially in groups. Search: Anxious."
python app.py testbench --din ./data/50nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init group --search anxious --log CRITICAL --times4ave 1 --maxs 10

printf "10nodes analysed by ls,vnd,bvns,ts. Initialized sequentially in groups. Search: Greedy."
python app.py testbench --din ./data/50nodes --metaheu ls,vnd,bvns,ts --memory 10 --niter 10 --init group --search greedy --log CRITICAL --times4ave 1 --maxs 10