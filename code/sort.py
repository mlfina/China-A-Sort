
from tools.crosssection import *

file = '../data/output/panel_rank.csv'
df = pd.read_csv(file, index_col=0)

print(df.columns)

char_list = ['me','52w', 'abr', 'abturn', 'adm', 'ag',
       'ala', 'alm', 'am', 'ami', 'ato', 'beta', 'betadm', 'bl', 'bm',
       'cdi', 'cei', 'cfp', 'ch4mkt_beta', 'ch4pmo_beta', 'ch4smb_beta',
       'ch4vmg_beta', 'cs', 'ct', 'cta', 'cvd', 'cvturn', 'dbe', 'dbeta',
       'dcoa', 'dcol', 'de', 'dfin', 'dgs', 'dm', 'dnca', 'dncl', 'dnco',
       'dnoa', 'dpia', 'droa', 'droe', 'dsa', 'dsi', 'dss', 'dtvm', 'dwc',
       'ebp', 'em', 'ep', 'esm', 'etr', 'fscore', 'gad', 'gpa', 'idsc',
       'idsq', 'idvc', 'ig', 'indmom', 'ivg', 'm1', 'm11', 'm24', 'm3',
       'm6', 'm60', 'mchg', 'mdr', 'ndp', 'noa', 'oacc', 'ocfp', 'ol',
       'opa', 'ope', 'oscore', 'pm', 'rdm', 'rds', 'rna', 'roa', 'roe',
       'rs', 'season', 'sg', 'sgq', 'sp', 'sr', 'sue', 'tacc', 'tan',
       'tbi', 'tes', 'ts', 'turnm', 'tv', 'vcf', 'vdtv', 'vturn']

print(len(char_list))
rank_char_list = ['rank_'+i for i in char_list]

# identifiers
ids = ['asset','date','ret','xret','lag_me','log_me','rf_mon']


# ### delete obs. with NA me

df1 = df[ids+rank_char_list]
print(df1.shape)
df1 = df1[~df1['lag_me'].isna()]
print(df1.shape)

print(df1.head())

# do sorting based on the rank
## construct decile portfolios
## calculate the ls factors

cs_vw = cs(df1, char_list, 10, 'lag_me', 20)
cs_vw.update_all(parallel=True)

cs_ew = cs(df1, char_list, 10, 'ew', 20)
cs_ew.update_all(parallel=True)

with open('../data/output/cs_vw.pkl', 'wb') as f:
    pkl.dump(cs_vw, f)

with open('../data/output/cs_ew.pkl', 'wb') as f:
    pkl.dump(cs_ew, f)

