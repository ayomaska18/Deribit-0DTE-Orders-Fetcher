0 8 * * * tmux new-session -d -s btc_fetch 'python3 /usr/src/app/get_0dte_position_data_btc.py' 
0 8 * * * tmux new-session -d -s eth_fetch 'python3 /usr/src/app/get_0dte_position_data_eth.py' 
0 8 * * * tmux new-session -d -s sol_fetch 'python3 /usr/src/app/get_0dte_position_data_sol.py' 
1 8 * * * tmux new-session -d -s summary_run 'python3 /usr/src/app/get_summary.py'
