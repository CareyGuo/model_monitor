
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import numpy as np
from classify_var import  var_classify
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt


def feat_iv_ks(df,bin_num,cut_type,DepVarName):
    #对连续型变量进行分箱，对于分类型变量无需分箱
    def feat_bin(contns_feature,bin_num,cut_type): 
        contns_feature = pd.qcut(contns_feature,bin_num,duplicates='drop') if cut_type=='equal_frequency' else pd.cut(contns_feature,bin_num)
        return contns_feature
    categ_col = var_classify(df,classify_type='auto')[1]  
    contins_col = var_classify(df,classify_type='auto')[0]
    data_=df.copy()
    contins_bin=data_[contins_col].apply(lambda x : feat_bin(x,bin_num,cut_type))
    categ_bin  =data_[categ_col]
    data_bin=pd.concat([contins_bin,categ_bin,data_[DepVarName]],axis=1)

    
    #计算变量的IV、KS
    def cal_iv_ks(data_,DepVarName,x):
        df_agg=data_.groupby(x,as_index=False).agg({DepVarName:[np.sum,np.size]})
        df_agg.columns=["index","bad","total"]
        df_agg.set_index(["index"], inplace=True)
        df_agg=df_agg.replace(np.nan,0)
        df_agg['good'] = df_agg['total'] - df_agg['bad']
        df_agg['woe'] = np.log( (df_agg['bad']/df_agg['bad'].sum()+0.0000001)/(df_agg['good']/df_agg['good'].sum()+0.0000001) )
        diff = (df_agg['bad']/df_agg['bad'].sum()) - (df_agg['good']/df_agg['good'].sum())
        iv=(diff*df_agg['woe']).sum()
        df_agg['cum_good']=np.cumsum(df_agg['good'])
        df_agg['cum_bad']=np.cumsum(df_agg['bad'])
        ks=abs(df_agg['cum_bad']/df_agg['bad'].sum() - df_agg['cum_good']/df_agg['good'].sum()).max()
        return iv,ks
    
    feat_iv_ks=pd.DataFrame([[feat,cal_iv_ks(data_bin,DepVarName,feat)[0],cal_iv_ks(data_bin,DepVarName,feat)[1]] for feat in contins_col+categ_col ],columns=["Feature",'IV','KS'])
    return feat_iv_ks


def feat_des(df):
    """
    此程序目的：分别查看分类特征和连续特征的数据概况
    """
    categ_col = var_classify(df,classify_type='auto')[1]  
    contins_col = var_classify(df,classify_type='auto')[0]
    df[categ_col]   = df[categ_col].astype('O')
    df[contins_col] = df[contins_col].apply(pd.to_numeric,errors='ignore')
    
    writer = pd.ExcelWriter('features_describe.xlsx')
    if categ_col:
        cat_features_describe = df[categ_col].describe().T.assign(missing_pct=df.apply(lambda x : (len(x)-x.count())/len(x)))
        cat_features_describe.to_excel(writer,sheet_name='cat_features',encoding='gbk')
    else:
        print('无分类变量')
    if contins_col:
        num_features_describe = df[contins_col].describe().T.assign(missing_pct=df.apply(lambda x : (len(x)-x.count())/len(x)))
        num_features_describe.to_excel(writer,sheet_name='num_features',encoding='gbk')
    else:
        print('无连续变量')
    writer.save()
    

def feat_analy_table_plot(df,feature_imp,max_feat,_cut_type,_intervals,y_var):
    """
    此程序目的：观察变量和坏账率之间的关系，输出变量不同取值对应的坏账率
    df：数据集
    feature_imp：特征重要性数据集，输出变量的顺序按特征重要性大小排列
    max_feat：最多输出多少特征的单变量分析结果
    _cut_type：数值型变量的分箱方式，cut_type='equal_frequency’为等频分箱，cut_type='equal_length’为等宽分箱
    _intervals：分箱箱数
    y_var:Y标签变量名
    """
    def feat_analy(df,feat_type,xlabel_name,y_label_name2,cut_type,intervals):
        if feat_type=='num':
            if cut_type=='equal_frequency':
                group_names = pd.qcut(df[xlabel_name],intervals,duplicates='drop').values.categories.left
                df['feature_bin'] = pd.qcut(df[xlabel_name],intervals,labels=group_names,duplicates='drop')
            else:
                group_names = pd.cut(df[xlabel_name],intervals).values.categories.left
                df['feature_bin'] = pd.qcut(df[xlabel_name],intervals,labels=group_names)
        else:
            df['feature_bin']=df[xlabel_name]

        feat_label_analy = pd.pivot_table(df, values=y_label_name2, index=['feature_bin'],aggfunc=[len,np.mean]).sort_index()
        feat_label_analy.columns=['客户数','实际坏账率(%)'] 
        feat_label_analy['实际坏账率(%)']=feat_label_analy['实际坏账率(%)']*100
        feat_label_analy['实际坏账率(%)']=feat_label_analy['实际坏账率(%)'].map(lambda x:format(x,'.2f'))

        if feat_type=='num':
            lx=[]
            for i in range(len(feat_label_analy)):
                if i<len(feat_label_analy)-1:
                    lx.append(str(round(group_names[i],2))+'-'+str(round(group_names[i+1],2)))
                else:
                    lx.append(str(round(group_names[i],2))+'+')
            feat_label_analy.index=lx
        feat_label_analy.index.names=[xlabel_name]
        return feat_label_analy
    
    #绘制变量不同取值对应坏账率的表
    def feat_nanly_plot(var_analy,xlabel_name,title_name):
        var_analy = var_analy.apply(pd.to_numeric,errors='ignore')

        fig=plt.figure(figsize=(10,6))
        l=range(len(var_analy))
        ax1=fig.add_subplot(111) 
        ax1.plot(l,var_analy['实际坏账率(%)'],'-',color='r',label='实际坏账率(%)')
        ax1.set_xlabel(xlabel_name)
        ax1.set_ylabel('坏账率')

        #分布图
        ax2 = ax1.twinx()
        ax2.bar(l,var_analy['客户数'],color='b',alpha=0.5,align='center',edgecolor='white',label='客户数')

        fig.legend(loc=1,bbox_to_anchor=(0.96,1),bbox_transform=ax1.transAxes)
        lx=var_analy.index
        plt.xticks(l,lx)
        plt.title(title_name)

        for tick in ax1.get_xticklabels():
            tick.set_rotation(45)
        #设置百分比形式的坐标轴
        fmt='%.2f%%'
        yticks = mtick.FormatStrFormatter(fmt)  
        ax1.yaxis.set_major_formatter(yticks)
        plt.show()
        
    #输出变量不同取值对应坏账率的表和图
    writer = pd.ExcelWriter('feat_analy.xlsx')
    for i in range(max_feat):
        feat=feature_imp['column'].iloc[i]
        exec("var%s_analy=feat_analy(df,feature_imp['var_type'].iloc[i],feat,y_var,cut_type=_cut_type,intervals=_intervals)"%i)
        exec("var%s_analy.to_excel(writer,sheet_name=str(i+1))"%i)
        exec("feat_nanly_plot(var%s_analy,feat,feat+'分析')"%i)
    writer.save()

