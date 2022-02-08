
# coding: utf-8

import sys
import os
import pandas as pd
import numpy as np
from var_dict import acard_var_dict as var_dict
from classify_var import  var_classify
import univariate_analysis as ua
sys.path.append('E:\code\publictools')
import publictools


def var_coding(data):
    others_code_value='other'
    for var_ in var_dict.keys():
        if var_ in data.columns.tolist():
            try:
                data[var_]=data[var_][pd.notnull(data[var_])].astype('int').astype(str)
            except:
                data[var_]=data[var_].astype(str)
            print("需要编码的变量为：%s"%var_)
            print( 'Before Coding:')
            print(data[var_].value_counts())
            data[var_]=np.where(data[var_].isin(var_dict.get(var_).get('value')),data[var_],others_code_value)
            data[var_]=data[var_].map(dict( 
                            zip(
                                    list(var_dict.get(var_).get('value'))+[others_code_value], 
                                    list(range(len(var_dict.get(var_).get('value'))))+[-1]  
                                    )))
            print( 'After Coding:')
            print(data[var_].value_counts())
            print('\n')
    return data

def miss_homo_drop(data,missrate_thr,homo_drop_thr,not_feat):
    """1、删除全空的行和列"""
    print('\n1、删除全空的行和列')
    all_nan_col = data.columns[data.isna().all()].tolist()
    print('全空的列为：%s'%all_nan_col)
    data = data.dropna(axis=0,subset=[i for i in data.columns if i not in not_feat],how='all') #删除表中全部为NaN的行
    data = data.dropna(axis=1, how='all') #删除表中全部为NaN的列
    print('去除全空的行和列之后的数据维度：',data.shape)

    """2、删除缺失率较高的特征"""
    print('\n2、删除缺失率较高的数据')
    thr=1-missrate_thr
    miss_rate = data.apply(lambda x : (len(x)-x.count())/len(x))
    print('缺失率大于{missrate}的变量为:'.format(missrate=missrate_thr),miss_rate[miss_rate>missrate_thr].index)
    data=data.dropna(thresh=len(data) * thr,axis=1) #将缺失率>thr的列删除

    print('删除缺失率{missrate}以上的列之后的数据维度：'.format(missrate=missrate_thr),data.shape)

    """3、删除单一值变量"""
    print('\n3、删除单一值变量')
    single_value_col = data.loc[:,data.apply(pd.Series.nunique) == 1].columns
    print('单一值变量为:%s'%single_value_col)
    data = data.loc[:,data.apply(pd.Series.nunique) != 1]
    print('删除单一值之后的数据维度：',data.shape)
    return data


    """4、删除同质化较高的变量"""
    print('\n4、删除同质化较高的变量')
    var_list=[]
    ratio_list=[]
    value_list=[]

    for var in list(data.columns):
        primaryvalue_ratio=round(data[var].value_counts().max()/len(data),2)
        primaryvalue=list(data[var].value_counts().index)[0]
        var_list.append(var)
        ratio_list.append(primaryvalue_ratio)
        value_list.append(primaryvalue)


    homo_data=pd.concat([pd.Series(var_list),pd.Series(ratio_list),pd.Series(value_list)],axis=1,keys=['变量','频次最高的值对应的频率',
                                                                                           '频次最高的值'])
    homo_data.sort_values('频次最高的值对应的频率',ascending=False).to_csv('homo_data.csv',encoding='gbk')
    print('同质化超过%.2f的变量为：%s'%(homo_drop_thr,homo_data[homo_data['频次最高的值对应的频率']>homo_drop_thr]['变量'].tolist()))

    #将同质化大于0.95的删掉
    homo_drop_list=list(homo_data[homo_data['频次最高的值对应的频率']>homo_drop_thr]['变量'])
    data=data.drop(homo_drop_list,axis=1)   #由于这三个变量出现同质化>0.95的情况也正常，在业务上能解释，因此不删去

    print('删除同质化变量之后的数据维度：',data.shape)
    return data


def psi_drop(df,df_bins,psi_thr,sort_var):
    def df_bin(df,df_sort_var,bins):
        """
        程序目的：实现将数据集按照时间先后顺序拆分成几等份
        df:数据集
        df_bins：将数据集均拆为几份子数据集，用于计算各子数据集两两比较的psi值
        psi_thr：psi超过psi_thr时，将变量删除
        sort_var:拆分子数据集之前，对数据排序的依据变量
        """
        df=df.sort_values(by=df_sort_var,ascending=True).reset_index(drop=True)
        sub_num=int(len(df)/bins)
        sub_df=[]
        for i in range(bins):
            if i<bins-1: 
                exec("data_set%s=df.iloc[(sub_num*i):sub_num*(i+1),:].reset_index(drop=True)"%i)        
            else:
                exec("data_set%s=df.iloc[(sub_num*i):,:].reset_index(drop=True)"%i)
            exec("sub_df.append(data_set%s)"%i)
        return sub_df

    def cal_psi(actual,expected,var_type,quant=10):
        """
        程序目的：计算变量psi
        var_type为'categ'时，计算分类变量的psi
        var_type为'contins'时，计算连续变量的psi（分类变量无需分箱，连续变量分成10箱）
        """
        if var_type=='categ':
            acnt = actual.value_counts().sort_index()
            ecnt = expected.value_counts().sort_index()
            arate= acnt/len(actual)
            erate= ecnt/len(expected)
            psi = np.sum((arate - erate)*np.log(arate/erate)) 
        else:
            minv = min(min(actual),min(expected))
            maxv = max(max(actual),max(expected))
            step = 1.0*(maxv-minv)/quant
            acnt = []
            ecnt = []
            s,e = minv,minv+step
            act = np.array(actual)
            ex = np.array(expected)

            while e <= maxv and step!=0:
                acnt.append(((act>=s) & (act < e)).sum())
                ecnt.append(((ex>=s )& (ex < e)).sum())
                s = e
                e = e+step

            arate = np.array(acnt)/ len(actual)
            erate = np.array(ecnt)/ len(expected)

            arate[arate==0] = 0.000001
            erate[erate==0] = 0.000001

            psi = np.sum((arate - erate)*np.log(arate/erate))
        return psi
    
    categ_col = var_classify(df,classify_type='auto')[1]  
    contins_col = var_classify(df,classify_type='auto')[0]
    
    #切分数据集
    sub_df=df_bin(df,df_sort_var=sort_var,bins=df_bins)
    
    #计算psi
    feature_psi=pd.DataFrame()
    for i in contins_col+categ_col:
        var_type1='categ' if i in categ_col else 'contins' 
        a=[str(x) for x in range(len(sub_df))]
        col_name= ['compare_'+x for x in a]
        for a1 in range(len(sub_df)-1):
            a2=a1
            while a2<=len(sub_df)-2:
                a2=a2+1
                feature_psi.loc[i,'compare_set'+str(a1)+'_set'+str(a2)]=cal_psi(sub_df[a1][i],sub_df[a2][i],var_type=var_type1,quant=10)
    feature_psi.to_csv('feature_psi.csv')
    
    #删除psi较高的变量
    print('\n7、删除不稳定的变量')
    unstable_feature=[]
    for i in feature_psi.index:
        for j in feature_psi.columns:
            if feature_psi.loc[i,j]>psi_thr:
                unstable_feature.append(i)
                break
    print('psi>{psi_thr}的变量为:{unstable_feature}'.format(psi_thr=psi_thr,unstable_feature=unstable_feature))
    df = df.drop(unstable_feature,axis=1)
    print('删除不稳定的变量之后的数据维度：',df.shape)
    return df

def iv_drop(df,iv_thr,bin_num,cut_type,label_var):
    """
    程序目的：删除IV值较低的变量
    df:数据集；
    iv_thr：删除iv值<iv_thr的变量；
    bin_num：将连续变量分箱的箱数；
    cut_type:对于连续变量的分箱类型，当cut_type='equal_frequency'为等频分箱，当cut_type='equal_length'为等宽分箱
    label_var:Y变量字段
    """
    feat_iv_ks=ua.feat_iv_ks(df,bin_num=bin_num,cut_type=cut_type,DepVarName=label_var)
    df=df.drop(feat_iv_ks[feat_iv_ks['IV']<iv_thr]['Feature'].tolist(),axis=1)
    print('因iv值较低被删除的变量为：',feat_iv_ks[feat_iv_ks['IV']<iv_thr]['Feature'].tolist())
    print('删除iv值小于{iv_thr}的变量之后的数据维度：'.format(iv_thr=iv_thr),df.shape)
    return df


def high_corr_drop(df,high_corr_thr,id_var,label_var,bin_num,cut_type):
    """
    程序目的：计算两两变量间的相关系数，对于两个相关性较高的变量，删除IV值较低的 ，保留IV值较高的
    """
    df1      = df.drop(id_var,axis=1)
    df_corr = df1.drop(label_var,axis=1).corr()
    df_corr_col = df_corr.columns.tolist()
    
    #只取相关系数矩阵的额下三角部分
    df_corr=pd.DataFrame(np.tril(df_corr,k=-1))
    df_corr.columns=df_corr_col
    df_corr.index=df_corr_col
    #求相关系数超过high_corr_thr的变量
    dic = {i:df_corr[df_corr[i]>high_corr_thr].index.tolist() for i in df_corr.columns.tolist()}
    # dic=dict(zip(df_corr.columns.tolist(), [df_corr[df_corr[i]>high_corr_thr].index for i in df_corr.columns.tolist()]))
    df_high_corr=pd.DataFrame.from_dict(dic, orient='index').T
    df_high_corr = df_high_corr.dropna(axis=1, how='all') #删除表中全部为NaN的列

    high_corr_var_iv=ua.feat_iv_ks(df,bin_num=bin_num,cut_type=cut_type,DepVarName=label_var)

    remove_high_corr_var = []
    for i in df_high_corr.columns.tolist():
        if i not in remove_high_corr_var:  #判断在前面的过程中是否已被删除，如被删除不再进行以下的判断，加快运行速度
            col_iv = high_corr_var_iv.IV[high_corr_var_iv.Feature==i]
            col_iv = np.float(col_iv)
            for j in range(len(df_high_corr)):
                if type(df_high_corr.loc[j,i]).__name__=='str':
                    row_iv = high_corr_var_iv.IV[high_corr_var_iv.Feature==df_high_corr.loc[j,i]]
                    #print(type(row_iv))
                    row_iv = np.float(row_iv)
                    if col_iv<row_iv:
                        remove_high_corr_var.append(i)
                        break
                    else:
                        remove_high_corr_var.append(df_high_corr.loc[j,i])


    remove_high_corr_var=list(set(remove_high_corr_var))
    print('因多重共线性删除的变量为：',remove_high_corr_var)
    
    df = df.drop(remove_high_corr_var,axis=1)
    print('删除相关性较高的变量之后的数据维度：',df.shape)
    return df  


def var_stab_by_month(df,time_var):
    """
    此程序目的:分月份观察各变量的稳定性，包括变量的均值、方差、峰度、偏度、缺失率
    df:数据集
    time_var:时间变量
    """
#     df[time_var] = df[time_var].astype(str)
#     month_list = sorted(df[time_var].str[:7].unique())
    df[time_var] =pd.to_datetime(df[time_var])
    month_list=sorted(df[time_var].dt.strftime('%Y-%m').unique())
    
    feature_mean=pd.DataFrame()
    feature_std=pd.DataFrame()
    feature_kurt=pd.DataFrame()
    feature_skew=pd.DataFrame()
    feature_missrate=pd.DataFrame()
    
#     categ_col = var_classify(df)[1]  
#     contins_col = var_classify(df)[0]
#     col=contins_col+categ_col
    col=[x for x in df.columns if x not in [time_var]]
    
    for j in month_list:
        for i in col:
            feature_mean.loc[i,j] = df[df[time_var].dt.strftime('%Y-%m')==j][i].mean()
            feature_std.loc[i,j] = df[df[time_var].dt.strftime('%Y-%m')==j][i].std()
            feature_kurt.loc[i,j] = df[df[time_var].dt.strftime('%Y-%m')==j][i].kurt()
            feature_skew.loc[i,j] = df[df[time_var].dt.strftime('%Y-%m')==j][i].skew()   
            feature_missrate.loc[i,j] = df[df[time_var].dt.strftime('%Y-%m')==j][i].isnull().sum()/df[df[time_var].dt.strftime('%Y-%m')==j][i].isnull().count()

    feature_distb=pd.concat([feature_mean, feature_std,feature_kurt,feature_skew,feature_missrate], ignore_index=False)

    feature_distb.index=[['mean']*len(col)+['std']*len(col)+['kurt']*len(col)+['skew']*len(col)+['missrate']*len(col),col*5]
    feature_distb.to_csv('feature_distb.csv')
    feature_distb
    

def sample_summary_byMonth(df,time_var,label_var):
    """
    程序目的：计算各月样本量及坏样本比例
    """
    df=df.sort_values(time_var,ascending=True)
    df[time_var] =pd.to_datetime(df[time_var])
    df_byMonth_size=df.groupby(df[time_var].dt.strftime('%Y-%m')).size()
    df_byMonth_size=df_byMonth_size.reset_index()
    df_byMonth_size.columns=[time_var,'各月数量']

    df_byMonth_rate=df.groupby([df[time_var].dt.strftime('%Y-%m'),df[label_var]]).size()/df.groupby(df[time_var].dt.strftime('%Y-%m')).size()
    df_byMonth_rate=df_byMonth_rate.reset_index()
    df_byMonth_rate=df_byMonth_rate[df_byMonth_rate[label_var]==1]
    df_byMonth_rate.columns=[time_var,label_var,'各月坏比例']

    df_byMonth=pd.merge(df_byMonth_size,df_byMonth_rate,how='left',on=[time_var])
    df_byMonth=df_byMonth.drop(label_var,axis=1)
    df_byMonth['各月坏比例']=df_byMonth['各月坏比例'].map(lambda x:format(x,'.2%'))
    return df_byMonth
    
def flag_summary(df,
                 flag_col,
                 rename_dict):
    df_flag_size_list=[]
    for i in flag_col:
        df_flag_size=df[i].value_counts(dropna=False).reset_index()
        df_flag_size_list.append(df_flag_size)
    flag_summary=publictools.merge_ds(df_flag_size_list,on_var=['index'],how='outer')
    flag_summary.set_index(["index"], inplace=True)
    flag_summary=flag_summary.T
    flag_summary=flag_summary.rename(columns=rename_dict)
    flag_summary['badrate']=flag_summary['bad']/(flag_summary['good']+flag_summary['bad'])
    flag_summary['badrate']=flag_summary['badrate'].map(lambda x:format(x,'.2%'))
    return flag_summary

