#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os

def var_classify(df,classify_type):
    """
    程序目的：对照vars_dict表里的变量类型，将数据集中的变量分成连续变量和分类变量
    """
    var_ds=pd.read_excel(os.path.join('E:\code\multi_loan','vars_dict.xlsx'),sheet_name='Sheet1')
    #定义连续变量和分类变量
    df_col=df.columns.tolist() 
    if classify_type=='artificial':
        contins_col=var_ds.loc[var_ds['变量类型']=='连续变量']['var'].tolist()
        categ_col=var_ds.loc[var_ds['变量类型']=='分类变量']['var'].tolist()
        contins_col=list(set(df_col).intersection(set(contins_col)))
        categ_col=list(set(df_col).intersection(set(categ_col)))
    else:
        contins_col=[i for i in df_col if df[i].nunique()>20]
        categ_col=[i for i in df_col if df[i].nunique()<=20]  
        contins_col=list(set(var_ds['var']).intersection(set(contins_col)))
        categ_col=list(set(var_ds['var']).intersection(set(categ_col)))
    return contins_col,categ_col

