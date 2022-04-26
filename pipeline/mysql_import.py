import requests
from os import listdir
from os.path import isdir, isfile, join
import logging, json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import os


logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)

root = Path("/Users/schemmy/Documents/projects/td/")
datapath = root / 'data'

dates = [f for f in listdir(datapath / 'historical_option_daily/single/') 
         if isdir(join(datapath / 'historical_option_daily/single', f))]
dates = sorted(dates)

for date in tqdm(dates[-10:]):
    logger.warning('%s' %date)

    if not os.path.exists(datapath / 'historical_option_daily/daily' / '{}.csv'.format(date)):

        files = [f for f in listdir(datapath / 'historical_option_daily/single/' / date) 
             if isfile(join(datapath / 'historical_option_daily/single' / date, f)) and f.endswith('.csv')]
        files = sorted(files)

        df1Day = {}
        for file in files:
            o0 = pd.read_csv(datapath / 'historical_option_daily/single/{}/{}'.format(date,file) )
            symb = file[:-4]
            o0['symb'] = symb
            df1Day[symb] = o0
        df1Day = pd.concat(df1Day[i] for i in df1Day)

        df1Day.reset_index(drop=True, inplace=True)
        df1Day['date'] = date
        df1Day.to_csv(datapath / 'historical_option_daily/daily' / '{}.csv'.format(date), index=False)

    # else:
        # df1Day = pd.read_csv(datapath / 'historical_option_daily/daily' / '{}.csv'.format(date))
    filename = str(datapath / 'historical_option_daily/daily' / '{}.csv'.format(date))
    os.system("docker cp %s spring-boot-ecommerce-mysql_db_container-1:/data_upload/" %filename)  

    os.system(r"""docker exec spring-boot-ecommerce-mysql_db_container-1 bash -c "mysql --local-infile=1 -uroot -proot -e \"LOAD DATA LOCAL INFILE '/data_upload/%s.csv' 
                INTO TABLE ecommerce.product 
                FIELDS TERMINATED BY ','
                LINES TERMINATED BY '\n' 
                IGNORE 1 ROWS
                (type,description,bid,ask,price,delta,gamma,theta,vega,rho,volume,open,strike,expiration,symb,date)
                SET id = NULL;\"; exit; "
                  """ %date)



    # docker exec $mysqlContainerName bash -c "mysql -h172.21.0.1 -P 3306 --protocol=tcp -u$mysqlRootUsername -p$mysqlRootPassword -e \"CREATE USER '$mysqlUsername'@'localhost' IDENTIFIED BY '$mysqlPassword';\"; exit;"

# url = "http://localhost:8080/api/products/add"
# root = Path("/Users/schemmy/Documents/projects/td/")
# datapath = root / 'data'
# header = {"Content-Type":"application/json"}

# dates = [f for f in listdir(datapath / 'historical_option_daily/single/') 
#          if isdir(join(datapath / 'historical_option_daily/single', f))]
# dates = sorted(dates)

# for date in dates[:2]:

#     logger.warning('%s' %date)
#     files = [f for f in listdir(datapath / 'historical_option_daily/single/' / date) 
#          if isfile(join(datapath / 'historical_option_daily/single' / date, f)) and f.endswith('.csv')]
#     files = sorted(files)

#     for file in files:
#         logger.warning('%s' %file)
#         o0 = pd.read_csv(datapath / 'historical_option_daily/single/{}/{}'.format(date,file) )
#         symb = file[:-4]
#         for rowId, row in tqdm(o0.iterrows(), total=o0.shape[0]):

#             record = {
#                 "name": symb + '_' + row['expirationDate'] + '_' + row['putCall'] + '_' + str(row['strikePrice']),
#                 "description": None,
#                 "category_id": None,
#                 "price": row['bid'],
#                 "weight": None,
#                 "picture1": None,
#                 "picture2": None,
#                 "picture3": None
#                 } 

#             r = requests.post(url=url, data=json.dumps(record), headers=header)
#             # pastebin_url = r.text
#             # print("The pastebin URL is:%s"%pastebin_url)
