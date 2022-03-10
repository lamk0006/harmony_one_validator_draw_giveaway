# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:35:38 2022

@author: Jonathan
"""

import pandas as pd
import subprocess
import schedule
import time
from pyhmy import staking
from datetime import datetime

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

print('Program running..')

def job():
    min_100()
    
def min_100():
    try:
        main_net = 'https://rpc.s0.t.hmny.io'
        
        validator_addr = 'one1y2udc388ylc0kx62jm92zxkm0lax3h8t6gchwk'
        validator_information = staking.get_validator_information(validator_addr, endpoint=main_net)
        validator_delegator = validator_information['validator']['delegations']
        
        df = pd.DataFrame(validator_delegator)
        df = df.loc[df['amount'] >= 100000000000000000000]
        df = df.reset_index(drop=True)
        
        winner_info = df.sample()
        winner_addr = winner_info['delegator-address'].values[0]
        
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        
        with open(f'/root/harmony/giveaway/{current_timestamp}.txt', 'w') as f:
            f.write('Date: \t \t \t \t' + current_timestamp)
            f.write('\n')
            f.write('Total delegators: \t \t' + str(len(df)))
            f.write('\n')
            f.write('Random picked address (Winner): ' + str(winner_addr))
            f.write('\n')
            f.write('\n')
            f.write('List of eligible delegators:')
            f.write('\n')
            f.write(str(df))
            process = subprocess.Popen(f'./hmy --node="https://api.s0.t.hmny.io" transfer --from one1y2udc388ylc0kx62jm92zxkm0lax3h8t6gchwk --to {winner_addr} --from-shard 0 --to-shard 0 --amount 10 --chain-id mainnet --passphrase-file passphrase.txt --true-nonce --gas-price 30', shell=True, stdout=subprocess.PIPE)
            output = process.communicate()[0]
            f.write('\n')
            f.write('\n')
            f.write('Tx confirmation:')
            f.write('\n')
            f.write(str(output))
    except Exception as e:
        print(e)
        
    print('Completed',current_timestamp)

schedule.every().day.at("00:00").do(job)
schedule.every().day.at("00:00").do(job)
schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
