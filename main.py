#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#%%
df_merged = pd.read_excel("Series_dataset_2.xlsx")
df_merged.head()
#%%
df_merged.drop("ESGScore", axis=1, inplace = True)
#%%
df_merged.drop("Unnamed: 0", axis=1, inplace = True)
#%%
df_merged.head()
# %%
rule = lambda x: 1 if x>=1 else 0
controversy_cols = df_merged.iloc[:, 3:26]
controversy_cols
#%%
df_merged["Sum"] = controversy_cols.sum(axis=1)
df_merged["Label"] = controversy_cols.sum(axis=1).apply(rule)
#%%
# The imbalance between classes can be seen from here 
df_merged["Label"].value_counts()
df_merged.drop(controversy_cols.columns.values.tolist(), axis=1,inplace=True)
df_merged.head()
#%%
# High percentages mean more missing values in proportion
print(df_merged.isna().mean())  
# Identify the columns that have more than half of their values missing
df_merged[df_merged.columns[df_merged.isnull().mean() > 0.5]]
#%%
# Separate the features
feature_set = df_merged.iloc[:,2:56]
#feature_set["Health&SafetyPolicy"].iloc[0:10].replace(to_replace = 500, value = np.nan , inplace = True)
feature_set.head()

#%%
df_merged = df_merged[df_merged["Company Name"].notna()]
df_merged["Company Name"].isna().value_counts()
#%%
years = []
index_length = len(df_merged["Company Name"])//10
for i in range(index_length):
    for j in range(10):
        years.append(j)
df_merged.insert(1, "Fiscal Years", years)
df_merged.head()
#%%
#feature_set = feature_set.reset_index()
df_merged.set_index(["Company Name", "Fiscal Years"], inplace=True)
#%%
df_merged.head()

#%%
# HOW TO ACCESS THE MULTIINDEX
df_merged.index.get_level_values('Company Name')

#%%
# Shape before dropping columns
keep_track = df_merged.shape
df_merged.loc["Zignago Vetro SpA",9].isnull().sum() 


#%%
controversy_companies = dict()
non_controversy_companies = dict()
counter = 0
nan_threshold = 90

df_merged_sorted = df_merged.copy()
df_merged_sorted.sort_index(level = "Company Name", inplace = True)

for idx,row in df_merged_sorted.iterrows():

    df_merged_grouped = df_merged_sorted.groupby(level = ["Company Name"])
    temp_df = df_merged_grouped.get_group(idx[0])

    # Count the number of controversies per company across all years
    controversy_sum = temp_df["Label"].sum() 

    # These dictionaries will be used for visualizations
    # if controversy_sum > 0:
    #     controversy_companies[f"{idx[0]}"] = controversy_sum
    # else:
    #     non_controversy_companies[f"{idx[0]}"] = controversy_sum
    
    percent_missing_value = temp_df.loc[idx].isnull().sum() * 100/(len(row)- 4)
    
    #print(f"Missing value percentage in FY{idx[1]}", " : " , percent_missing_value,"% ")
    

    if percent_missing_value > nan_threshold:
        df_merged_sorted.drop(index = idx, axis=0, inplace=True)
        
    keep_track = df_merged.shape
    counter = counter + 1

    print("Iteration number: ", counter)
    # break
    # print("Iteration number", counter)
    # print(controversy_companies)
    # print(non_controversy_companies)


##%%
#%%

df_merged_sorted.to_excel("Nans_removed_dataset.xlsx")    
print(controversy_companies)
print(non_controversy_companies)

#%%
df_merged_sorted.shape

# METHODOLOGY

# 1) Loop through the row values of the dataset

# 2) While looping, select a subset of dataset of the dataset that has the same index name (company)

# 3) If the ratio of NaN's to reported values is above a threshold drop the entire observation (this should be comparative based on the max())

# 4) 
# %%
