
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pandas.tseries.offsets import MonthBegin, MonthEnd
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore")


if not os.path.exists("../data/output"):
    os.mkdir("../data/output")
if not os.path.exists("../data/output/sorted_portfolio_vw"):
    os.mkdir("../data/output/sorted_portfolio_vw")
if not os.path.exists("../data/output/sorted_portfolio_ew"):
    os.mkdir("../data/output/sorted_portfolio_ew")
if not os.path.exists("../data/tmp"):
    os.mkdir("../data/tmp")

# returns

df = pd.read_csv("../data/input/return/TRD_Mnth.csv")
#,encoding='utf8',error_bad_lines=False, engine ='python')
df = df[['Stkcd','Trdmnt','Mretwd']]
df.columns = ['asset','date','ret']
df['date'] = pd.to_datetime(df['date'])  # date formated
df['date'] = df['date']+MonthEnd(0)      # date is formatted as month end
df = df[ (df['date']>='2000') & (df['date']<='2023')]

df_pivot = pd.pivot(data=df,values='ret', index='date', columns='asset')
df_pivot = df_pivot.reset_index()
df_pivot.head()

plt.figure(figsize=(10,5))
df.groupby('date').count()['ret'].plot()
plt.title('Number of Stock in Each Month')
plt.show()
plt.close()


## cross-sectional 
# 
# - asset characteristics


char_list = os.listdir("../data/input/chars")
char_list = [i if i[-4:]=='.csv' for i in char_list]
char_list = [i[:-4].lower() for i in char_list]
char_list.sort()
print(char_list)
for i in ['size3','im6','im12','ivchg','opla','ople','gpla','idsff','idvff',
          'idvq','turnq','turna','dtvq','dtva','pr','age','lfe',
         'hn',
          'betafp'
#           'betadm'
         ]:
    char_list.remove(i)
print(len(char_list))

char_list_new = char_list.copy()
char_list_new.remove('size')
char_list_new = ['me']+char_list_new
char_list_new.sort()

for char in tqdm(char_list):
    print(char)
    da = pd.read_csv("../data/input/chars/"+char+".csv")
    #,encoding='utf8',error_bad_lines=False, engine ='python')
    da['Trdmnt'] = pd.to_datetime(da['Trdmnt'],format='%Y%m')
    da['Trdmnt'] = da['Trdmnt'] + MonthEnd(0)
    da['Trdmnt'] = da['Trdmnt'] + MonthEnd(1)
    da = da[ (da['Trdmnt']>='2000') & (da['Trdmnt']<='2023')]
    df_melt = da.melt(id_vars=['Trdmnt'],value_name =char)
    df_melt.columns = ['date','asset',char]
    outputpath="../data/tmp/"+char+".csv"
    df_melt.to_csv(outputpath,sep=',',index=False,header=True)


da = df.copy()
for char in tqdm(char_list):
    s1 = pd.read_csv("../data/tmp/"+char+".csv")
    #,encoding='utf8',error_bad_lines=False, engine ='python')
    s1['date'] = pd.to_datetime(s1['date'])
    da = pd.merge(da,s1,how='left',on=['date','asset'])


# time-series variables
# 
# - factors
# - macro predictors


f= pd.read_csv("../data/input/factors/ch4/CH_4_fac_update_20211231.csv",skiprows=9)
#,encoding='utf8',error_bad_lines=False, engine ='python')
f.rename(columns={'mnthdt':'date'}, inplace = True)
f['date'] = pd.to_datetime([str(i) for i in f['date']])
for i in f.columns[1:]:
    print(i)
    f[i]=f[i]/100

da = pd.merge(da,f,how='left',on=['date'])
da['xret']=da['ret']-da['rf_mon']

da['lag_me'] = np.exp(da['size'])
da['log_me'] = da['size']
da['me'] = da['size']
del da['size']

## output the raw data

da=da[[
        # id
        'asset', 'date', 'ret', 'xret', 'lag_me', 'log_me',
        # ts
        'rf_mon', 'mktrf', 'VMG', 'SMB', 'PMO'
    ]+char_list_new
]

print(da.shape)
da=da[~da['xret'].isna()]
print(da.shape)
da=da[~da['me'].isna()]
print(da.shape)

da.to_csv("../data/output/panel_raw.csv")

# cross-sectional rank $[-1,1]$

def standardize(df):
    # exclude the the information columns
    col_names = df.columns.values.tolist()
    list_to_remove = ['asset', 'date',
                      'ret', 'xret', 'lag_me', 'log_me', 'rf_mon', 'mktrf', 'VMG', 'SMB', 'PMO'
                     ]
    
    col_names = list(set(col_names).difference(set(list_to_remove)))
    print(col_names)
    for col_name in tqdm(col_names):
        # print('processing %s' % col_name)
        # count the non-missing number of factors, we only count non-missing values
        unique_count = df.dropna(subset=['%s' % col_name]).groupby(['date'])['%s' % col_name].unique().apply(len)
        unique_count = pd.DataFrame(unique_count).reset_index()
        unique_count.columns = ['date', 'count']
        df = pd.merge(df, unique_count, how='left', on=['date'])
        # ranking, and then standardize the data
        df['%s_rank' % col_name] = df.groupby(['date'])['%s' % col_name].rank(method='dense')
        df['rank_%s' % col_name] = (df['%s_rank' % col_name] - 1) / (df['count'] - 1) * 2 - 1
        df = df.drop(['%s_rank' % col_name, '%s' % col_name, 'count'], axis=1)
    df = df.fillna(0)
    return df

da_rank = standardize(da)
print(da_rank.columns)

# # output rank data

da_rank.to_csv("../data/output/panel_rank.csv")


