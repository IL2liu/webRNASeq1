import pandas as pd

import itertools

df = pd.DataFrame.from_csv("/Users/mitras/self/teleshova/Teleshova_Phenotype_csv_final.csv", index_col = False)

fslist = []

fslist.append(list(set(df["Group"].tolist())))

#print str(fslist)

fslist.append(list(set(df["Condition"].tolist())))

#print str(fslist)

#print str([".".join(x) for x in zip (*fslist)])

print ( list(itertools.combinations(fslist,2)))