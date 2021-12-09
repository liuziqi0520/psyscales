#!/usr/bin/env python
# coding: utf-8

# # PsyScales 库
# * 更新时间：2021.8.27
# * 描述：心理量表是心理学研究的重要研究方法之一。未方便计算，避免重复劳动，节省时间精力，特编制写此python量表计算库，用来共享。
# * 作者：刘子琪 上海交通大学医学院附属精神卫生中心 上海市重点研究室 袁逖飞课题组

# # 使用注意事项：
# 
# * 题目顺序须与本库定义的量表顺序一致
# * 注意每道题目分值【最低严重程度的选项默认分值为1】
# * 列出原版题目顺序
# * 参考文献需要更新

# # 目录：
# 
# 基本人口学信息处理
# | 量表简称 | 量表全称          | 函数         | 分量表 |
# |..........|.......................|..................|........|
# |BDI     | Beck Depression Scale | get_BDI,get_

# |BAI     | Beck Anxiety Scale   |
# |BIS     | 巴瑞特冲动量表

# In[ ]:


class PsyScales:
    """此库包含袁逖飞实验室常用心理量表"""
    import numpy as np
    import pandas as pd
    import copy
    
    ########## 一、基本本人口学信息 ##########
    def get_age(self):
        """从问卷星中计算年龄：填写问卷时间-出生日期"""
        import pandas as pd
        self['sub_time'] = pd.to_datetime(self['sub_time'])
        self['birthday'] = pd.to_datetime(self['birthday'])
        self['age'] = ((self['sub_time']-self['birthday'])/365).astype('timedelta64[D]').astype(int)
        return self['age']

    def get_gender_text(self):
        """数值型性别转换为文本型性别【1 = male；2 = female】"""
        self['gender_text'] = (self['gender_number'])
        self.gender_text.replace(1,'Male',inplace=True)
        self.gender_text.replace(2,'Female',inplace=True)
        return self['gender_text']

    def get_education_years(self):
        """yuanlab计算教育年限的方法为各个教育阶段的学习年数相加"""
        self['education_years'] = self['primary_school'] + self['middle_school'] + self['high_school'] + self['college'] + self['postgradulate']
        return self['education_years']
    
    def get_BMI(self):
        """身高单位是【cm】，体重单位是【公斤】"""
        self['BMI'] = self['weight']/ pow(self['height']/100,2)
        return self['BMI']
        
    ########## 二、神经心理量表 ##########
    
    def get_BDI(self):
        """计算BDI分数"""
        self['BDI'] = self['BDI1'] + self['BDI2'] + self['BDI3'] + self['BDI4'] + self['BDI5'] + self['BDI6'] + self['BDI7'] + self['BDI8'] + self['BDI9'] + self['BDI10'] + self['BDI11'] + self['BDI12'] + self['BDI13'] + self['BDI14'] + self['BDI15'] + self['BDI16'] + self['BDI17'] + self['BDI18'] + self['BDI19'] + self['BDI20'] + self['BDI21']-21
        return self['BDI']
    
    def get_BDI_whether_numeric(self):
        """根据BDI量表分数判断是否抑郁【0 = 无抑郁；1 = 抑郁】"""
        self['BDI'] = self['BDI1'] + self['BDI2'] + self['BDI3'] + self['BDI4'] + self['BDI5'] + self['BDI6'] + self['BDI7'] + self['BDI8'] + self['BDI9'] + self['BDI10'] + self['BDI11'] + self['BDI12'] + self['BDI13'] + self['BDI14'] + self['BDI15'] + self['BDI16'] + self['BDI17'] + self['BDI18'] + self['BDI19'] + self['BDI20'] + self['BDI21']-21
        self['whether_numeric_depression']=(self['BDI'])
        self.loc[self.BDI<=4,'whether_numeric_depression']=0
        self.loc[self.BDI>4,'whether_numeric_depression']=1
        return self['whether_numeric_depression']
    
    def get_BDI_whether_text(self):
        """根据BDI量表分数判断是否抑郁【0 = 无抑郁；1 = 抑郁】"""
        self['BDI'] = self['BDI1'] + self['BDI2'] + self['BDI3'] + self['BDI4'] + self['BDI5'] + self['BDI6'] + self['BDI7'] + self['BDI8'] + self['BDI9'] + self['BDI10'] + self['BDI11'] + self['BDI12'] + self['BDI13'] + self['BDI14'] + self['BDI15'] + self['BDI16'] + self['BDI17'] + self['BDI18'] + self['BDI19'] + self['BDI20'] + self['BDI21']-21
        self['whether_text_depression']=(self['BDI'])
        self.loc[self.BDI<=4,'whether_text_depression'] = 'Not Depressive'
        self.loc[self.BDI>4,'whether_text_depression'] = 'Depressive'
        return self['whether_text_depression']
        
    def get_BDI_level_numeric(self):
        """根据BDI量表分数判断抑郁严重程度【0 = 无抑郁；1 = 轻度抑郁； 2 = 中度抑郁；3 = 重度抑郁】"""
        self['BDI'] = self['BDI1'] + self['BDI2'] + self['BDI3'] + self['BDI4'] + self['BDI5'] + self['BDI6'] + self['BDI7'] + self['BDI8'] + self['BDI9'] + self['BDI10'] + self['BDI11'] + self['BDI12'] + self['BDI13'] + self['BDI14'] + self['BDI15'] + self['BDI16'] + self['BDI17'] + self['BDI18'] + self['BDI19'] + self['BDI20'] + self['BDI21']-21
        self['numeric_level_BDI']=(self['BDI'])
        self.loc[self.BDI<=4,'numeric_level_BDI']=0             # 无抑郁
        self.loc[self.BDI.between(5,7),'numeric_level_BDI']=1   # 轻度抑郁
        self.loc[self.BDI.between(8,15),'numeric_level_BDI']=2  # 中度抑郁
        self.loc[self.BDI>=16,'numeric_level_BDI']=3            # 重度抑郁
        return self['numeric_level_BDI']
    
    def get_BDI_level_text(self):
        """根据BDI量表分数判断抑郁严重程度"""
        self['BDI'] = self['BDI1'] + self['BDI2'] + self['BDI3'] + self['BDI4'] + self['BDI5'] + self['BDI6'] + self['BDI7'] + self['BDI8'] + self['BDI9'] + self['BDI10'] + self['BDI11'] + self['BDI12'] + self['BDI13'] + self['BDI14'] + self['BDI15'] + self['BDI16'] + self['BDI17'] + self['BDI18'] + self['BDI19'] + self['BDI20'] + self['BDI21']-21
        self['text_level_BDI']=(self['BDI'])
        self.loc[self.BDI<=4,'text_level_BDI']='Not Depressive'                  # 无抑郁
        self.loc[self.BDI.between(5,7),'text_level_BDI']='Mild Depressive'       # 轻度抑郁
        self.loc[self.BDI.between(8,15),'text_level_BDI']='Moderate Depressive'  # 中度抑郁
        self.loc[self.BDI>=16,'text_level_BDI']= 'Sever Depressive'              # 重度抑郁
        return self['text_level_BDI']
    
    def get_BAI(self):
        """计算BAI总分"""
        self['BAI'] = self['BAI1'] + self['BAI2'] + self['BAI3'] + self['BAI4'] + self['BAI5'] + self['BAI6'] + self['BAI7'] + self['BAI8'] + self['BAI9'] + self['BAI10'] + self['BAI11'] + self['BAI12'] + self['BAI13'] + self['BAI14'] + self['BAI15'] + self['BAI16'] + self['BAI17'] + self['BAI18'] + self['BAI19'] + self['BAI20'] + self['BAI21']-21
        return self['BAI']
    
    def get_BAI_level_numeric(self):
        """根据BAI量表分数判断焦虑严重程度【0 = 低焦虑；1 = 中度焦虑；2 = 重度焦虑】"""
        self['BAI'] = self['BAI1'] + self['BAI2'] + self['BAI3'] + self['BAI4'] + self['BAI5'] + self['BAI6'] + self['BAI7'] + self['BAI8'] + self['BAI9'] + self['BAI10'] + self['BAI11'] + self['BAI12'] + self['BAI13'] + self['BAI14'] + self['BAI15'] + self['BAI16'] + self['BAI17'] + self['BAI18'] + self['BAI19'] + self['BAI20'] + self['BAI21']-21
        self['numeric_level_BAI']=(self['BAI'])
        self.loc[self.BAI<=21,'numeric_level_BAI']=0             # 低焦虑
        self.loc[self.BAI.between(22,35),'numeric_level_BAI']=1   # 中度焦虑
        self.loc[self.BAI>=36,'numeric_level_BAI']=2            # 重度焦虑
        return self['numeric_level_BAI']
    
    def get_BAI_level_text(self):
        """根据BAI量表分数判断焦虑严重程度"""
        self['BAI'] = self['BAI1'] + self['BAI2'] + self['BAI3'] + self['BAI4'] + self['BAI5'] + self['BAI6'] + self['BAI7'] + self['BAI8'] + self['BAI9'] + self['BAI10'] + self['BAI11'] + self['BAI12'] + self['BAI13'] + self['BAI14'] + self['BAI15'] + self['BAI16'] + self['BAI17'] + self['BAI18'] + self['BAI19'] + self['BAI20'] + self['BAI21']-21
        self['text_level_BAI']=(self['BAI'])
        self.loc[self.BAI<=21,'text_level_BAI']='Not Anxious'                  # 无焦虑
        self.loc[self.BAI.between(22,35),'text_level_BAI']='Mild Anxious'       # 中度焦虑
        self.loc[self.BAI>=36,'text_level_BAI']= 'Sever Anxious'              # 重度焦虑
        return self['text_level_BAI']

    
    def get_BIS_subscales(self):
        """计算BIS所有分量表分数"""
        import pandas as pd
        # 计算分量表原始分
        self['nonplan_impulsivity_primary']=(6-self['BIS1'])+(6-self['BIS4'])+(6-self['BIS7'])+(6-self['BIS10'])+(6-self['BIS13'])+(6-self['BIS16'])+(6-self['BIS19'])+(6-self['BIS22'])+(6-self['BIS25'])+(6-self['BIS28'])
        self['motor_impulsivity_primary']=self['BIS2']+self['BIS5']+self['BIS8']+self['BIS11']+self['BIS14']+self['BIS17']+self['BIS20']+self['BIS23']+self['BIS26']+self['BIS29']
        self['attention_impulsivity_primary']=(6-self['BIS3'])+(6-self['BIS6'])+(6-self['BIS9'])+(6-self['BIS12'])+(6-self['BIS15'])+(6-self['BIS18'])+(6-self['BIS21'])+(6-self['BIS24'])+(6-self['BIS27'])+(6-self['BIS30'])
        #计算分量表100分制
        self['nonplan_impulsivity']=((self['nonplan_impulsivity_primary']-10)/40)*100
        self['motor_impulsivity']=((self['motor_impulsivity_primary']-10)/40)*100
        self['attention_impulsivity']=((self['attention_impulsivity_primary']-10)/40)*100
        data = pd.DataFrame(list(zip(self['nonplan_impulsivity'],self['motor_impulsivity'],self['attention_impulsivity'])))
        data.columns = ['nonplan_impulsivity','motor_impulsivity','attention_impulsivity']
        return data
    
    def get_BIS(self):
        """计算BIS所有分量表分数以及总分"""
        # 计算分量表原始分
        self['nonplan_impulsivity_primary']=(6-self['BIS1'])+(6-self['BIS4'])+(6-self['BIS7'])+(6-self['BIS10'])+(6-self['BIS13'])+(6-self['BIS16'])+(6-self['BIS19'])+(6-self['BIS22'])+(6-self['BIS25'])+(6-self['BIS28'])
        self['motor_impulsivity_primary']=self['BIS2']+self['BIS5']+self['BIS8']+self['BIS11']+self['BIS14']+self['BIS17']+self['BIS20']+self['BIS23']+self['BIS26']+self['BIS29']
        self['attention_impulsivity_primary']=(6-self['BIS3'])+(6-self['BIS6'])+(6-self['BIS9'])+(6-self['BIS12'])+(6-self['BIS15'])+(6-self['BIS18'])+(6-self['BIS21'])+(6-self['BIS24'])+(6-self['BIS27'])+(6-self['BIS30'])
        #计算分量表100分制
        self['nonplan_impulsivity']=((self['nonplan_impulsivity_primary']-10)/40)*100
        self['motor_impulsivity']=((self['motor_impulsivity_primary']-10)/40)*100
        self['attention_impulsivity']=((self['attention_impulsivity_primary']-10)/40)*100
        #计算BIS总分
        self['BIS']=(self['nonplan_impulsivity']+self['motor_impulsivity']+self['attention_impulsivity'])/3
        return self['BIS']
    
    def get_UPPS_P_subscales(self):
        """计算UPPS_P分量表分数，【简版】"""
        import pandas as pd
        self['negative_urgency']=self['UPPS_P6']+self['UPPS_P8']+self['UPPS_P13']+self['UPPS_P15']
        self['positive_urgency']=self['UPPS_P3']+self['UPPS_P10']+self['UPPS_P17']+self['UPPS_P20']
        self['lack_of_persistence']=(5-self['UPPS_P1'])+(5-self['UPPS_P4'])+(5-self['UPPS_P7'])+self['UPPS_P11']
        self['lack_of_plan']=self['UPPS_P2']+(5-self['UPPS_P5'])+(5-self['UPPS_P12'])+self['UPPS_P19']
        self['sensation_seeking']=self['UPPS_P9']+self['UPPS_P14']+self['UPPS_P16']+self['UPPS_P18']
        data = pd.DataFrame(list(zip(self['negative_urgency'],self['positive_urgency'],self['lack_of_persistence'],self['lack_of_plan'],self['sensation_seeking'])))
        data.columns = ['negative_urgency','positive_urgency','lack_of_persistence','lack_of_plan','sensation_seeking']
        return data
    
    def get_BIS_BAS_subscales(self):
        import pandas as pd
        self['BASR']=self['BAS4']+self['BAS5']+self['BAS7']+self['BAS14']+self['BAS18']+self['BAS23']
        self['BASD']=self['BAS3']+self['BAS9']+self['BAS12']+self['BAS21']
        self['BASF']=self['BAS10']+self['BAS15']+self['BAS16']+self['BAS20']
        self['BIS']=self['BAS8']+self['BAS13']+self['BAS16']+self['BAS19']+self['BAS24']
        data = pd.DataFrame(list(zip(self['BASR'],self['BASD'],self['BASF'],self['BIS'])))
        data.columns = ['BASR','BASD','BASF','BIS']
        return data
                 
    def get_PSQI_subscales(self):
        """计算PSQI所有分量表"""
        import pandas as pd
        #主观睡眠质量
        self['subjective_sleep_quality']=5-self['PSQI6']
        #睡眠潜伏期
        self['sleep_latency_transfer']=self['PSQI2']-1+self['PSQI5_1']-1
        self['sleep_latency']=(self['sleep_latency_transfer'])
        self.loc[self.sleep_latency_transfer<=0,'sleep_latency']=0
        self.loc[self.sleep_latency_transfer.between(1,2),'sleep_latency']=1
        self.loc[self.sleep_latency_transfer.between(3,4),'sleep_latency']=2
        self.loc[self.sleep_latency_transfer.between(5,6),'sleep_latency']=3
        # 睡眠持续性
        self['sleep_persistence_transfer']=(self['PSQI4_1']*60+self['PSQI4_2'])/60
        self['sleep_persistence']=(self['sleep_persistence_transfer'])
        self.loc[self.sleep_persistence_transfer>7,'sleep_persistence']=0
        self.loc[self.sleep_persistence_transfer.between(6,7),'sleep_persistence']=1
        self.loc[self.sleep_persistence_transfer.between(5,6),'sleep_persistence']=2
        self.loc[self.sleep_persistence_transfer<5,'sleep_persistence']=3
        # 睡眠效率
        self['stay_in_bed']=(12*60+self['PSQI3_1']*60+self['PSQI3_2'])-(self['PSQI1_1']*60+self['PSQI1_2'])
        self['sleep_in_bed']=self['PSQI4_1']*60+self['PSQI4_2']
        self['sleep_efficiency_transfer']=round(self['sleep_in_bed']/self['stay_in_bed'],2)
        self['sleep_efficiency']=(self['sleep_efficiency_transfer'])
        self.loc[self.sleep_efficiency_transfer>=0.85,'sleep_efficiency']=0
        self.loc[self.sleep_efficiency_transfer.between(0.75,0.84),'sleep_efficiency']=1
        self.loc[self.sleep_efficiency_transfer.between(0.65,0.74),'sleep_efficiency']=2
        self.loc[self.sleep_efficiency_transfer<=0.64,'sleep_efficiency']=3
        #睡眠紊乱
        self['sleep_turbulence_transfer']=self['PSQI5_2']+self['PSQI5_3']+self['PSQI5_4']+self['PSQI5_5']+self['PSQI5_6']+self['PSQI5_7']+self['PSQI5_8']+self['PSQI5_9']+self['PSQI5_10']
        self['sleep_turbulence']=(self['sleep_turbulence_transfer'])
        self.loc[self.sleep_turbulence_transfer<=0,'sleep_turbulence']=0
        self.loc[self.sleep_turbulence_transfer.between(1,9),'sleep_turbulence']=1
        self.loc[self.sleep_turbulence_transfer.between(10,18),'sleep_turbulence']=2
        self.loc[self.sleep_turbulence_transfer>=19,'sleep_turbulence']=3
        #使用睡眠药物
        self['use_sleep_medication']=self['PSQI7']
        # 白天功能紊乱
        self['daytime_dysfunction_transfer']=self['PSQI8']+self['PSQI9']
        self['daytime_dysfunction']=(self['daytime_dysfunction_transfer'])
        self.loc[self.daytime_dysfunction_transfer<=0,'daytime_dysfunction']=0
        self.loc[self.daytime_dysfunction_transfer.between(1,2),'daytime_dysfunction']=1
        self.loc[self.daytime_dysfunction_transfer.between(3,4),'daytime_dysfunction']=2
        self.loc[self.daytime_dysfunction_transfer>=5,'daytime_dysfunction']=3
        data = pd.DataFrame(list(zip(self['subjective_sleep_quality'],self['sleep_latency'], self['sleep_persistence'],self['sleep_efficiency'],self['sleep_turbulence'],self['use_sleep_medication'],self['daytime_dysfunction'])))
        data.columns = ['subjective_sleep_quality','sleep_latency','sleep_persistence','sleep_efficiency','sleep_turbulence','use_sleep_medication','daytime_dysfunction']
        return data
        
    def get_PSQI(self):
        """计算PSQI总分"""
        #主观睡眠质量
        self['subjective_sleep_quality']=5-self['PSQI6']
        #睡眠潜伏期
        self['sleep_latency_transfer']=self['PSQI2']-1+self['PSQI5_1']-1
        self['sleep_latency']=(self['sleep_latency_transfer'])
        self.loc[self.sleep_latency_transfer<=0,'sleep_latency']=0
        self.loc[self.sleep_latency_transfer.between(1,2),'sleep_latency']=1
        self.loc[self.sleep_latency_transfer.between(3,4),'sleep_latency']=2
        self.loc[self.sleep_latency_transfer.between(5,6),'sleep_latency']=3
        # 睡眠持续性
        self['sleep_persistence_transfer']=(self['PSQI4_1']*60+self['PSQI4_2'])/60
        self['sleep_persistence']=(self['sleep_persistence_transfer'])
        self.loc[self.sleep_persistence_transfer>7,'sleep_persistence']=0
        self.loc[self.sleep_persistence_transfer.between(6,7),'sleep_persistence']=1
        self.loc[self.sleep_persistence_transfer.between(5,6),'sleep_persistence']=2
        self.loc[self.sleep_persistence_transfer<5,'sleep_persistence']=3
        # 睡眠效率
        self['stay_in_bed']=(12*60+self['PSQI3_1']*60+self['PSQI3_2'])-(self['PSQI1_1']*60+self['PSQI1_2'])
        self['sleep_in_bed']=self['PSQI4_1']*60+self['PSQI4_2']
        self['sleep_efficiency_transfer']=round(self['sleep_in_bed']/self['stay_in_bed'],2)
        self['sleep_efficiency']=(self['sleep_efficiency_transfer'])
        self.loc[self.sleep_efficiency_transfer>=0.85,'sleep_efficiency']=0
        self.loc[self.sleep_efficiency_transfer.between(0.75,0.84),'sleep_efficiency']=1
        self.loc[self.sleep_efficiency_transfer.between(0.65,0.74),'sleep_efficiency']=2
        self.loc[self.sleep_efficiency_transfer<=0.64,'sleep_efficiency']=3
        #睡眠紊乱
        self['sleep_turbulence_transfer']=self['PSQI5_2']+self['PSQI5_3']+self['PSQI5_4']+self['PSQI5_5']+self['PSQI5_6']+self['PSQI5_7']+self['PSQI5_8']+self['PSQI5_9']+self['PSQI5_10']
        self['sleep_turbulence']=(self['sleep_turbulence_transfer'])
        self.loc[self.sleep_turbulence_transfer<=0,'sleep_turbulence']=0
        self.loc[self.sleep_turbulence_transfer.between(1,9),'sleep_turbulence']=1
        self.loc[self.sleep_turbulence_transfer.between(10,18),'sleep_turbulence']=2
        self.loc[self.sleep_turbulence_transfer>=19,'sleep_turbulence']=3
        #使用睡眠药物
        self['use_sleep_medication']=self['PSQI7']
        # 白天功能紊乱
        self['daytime_dysfunction_transfer']=self['PSQI8']+self['PSQI9']
        self['daytime_dysfunction']=(self['daytime_dysfunction_transfer'])
        self.loc[self.daytime_dysfunction_transfer<=0,'daytime_dysfunction']=0
        self.loc[self.daytime_dysfunction_transfer.between(1,2),'daytime_dysfunction']=1
        self.loc[self.daytime_dysfunction_transfer.between(3,4),'daytime_dysfunction']=2
        self.loc[self.daytime_dysfunction_transfer>=5,'daytime_dysfunction']=3
        #计算总分
        self['PSQI']=self['subjective_sleep_quality']+self['sleep_latency']+self['sleep_persistence']+self['sleep_efficiency']+self['sleep_turbulence']+self['use_sleep_medication']+self['daytime_dysfunction']
        return self['PSQI']
    
    def get_PSQI_level_numeric(self):
        """计算数值型睡眠质量【1 = Good；2 = Fair；3 = Limited；4 = Poor】"""
        #主观睡眠质量
        self['subjective_sleep_quality']=5-self['PSQI6']
        #睡眠潜伏期
        self['sleep_latency_transfer']=self['PSQI2']-1+self['PSQI5_1']-1
        self['sleep_latency']=(self['sleep_latency_transfer'])
        self.loc[self.sleep_latency_transfer<=0,'sleep_latency']=0
        self.loc[self.sleep_latency_transfer.between(1,2),'sleep_latency']=1
        self.loc[self.sleep_latency_transfer.between(3,4),'sleep_latency']=2
        self.loc[self.sleep_latency_transfer.between(5,6),'sleep_latency']=3
        # 睡眠持续性
        self['sleep_persistence_transfer']=(self['PSQI4_1']*60+self['PSQI4_2'])/60
        self['sleep_persistence']=(self['sleep_persistence_transfer'])
        self.loc[self.sleep_persistence_transfer>7,'sleep_persistence']=0
        self.loc[self.sleep_persistence_transfer.between(6,7),'sleep_persistence']=1
        self.loc[self.sleep_persistence_transfer.between(5,6),'sleep_persistence']=2
        self.loc[self.sleep_persistence_transfer<5,'sleep_persistence']=3
        # 睡眠效率
        self['stay_in_bed']=(12*60+self['PSQI3_1']*60+self['PSQI3_2'])-(self['PSQI1_1']*60+self['PSQI1_2'])
        self['sleep_in_bed']=self['PSQI4_1']*60+self['PSQI4_2']
        self['sleep_efficiency_transfer']=round(self['sleep_in_bed']/self['stay_in_bed'],2)
        self['sleep_efficiency']=(self['sleep_efficiency_transfer'])
        self.loc[self.sleep_efficiency_transfer>=0.85,'sleep_efficiency']=0
        self.loc[self.sleep_efficiency_transfer.between(0.75,0.84),'sleep_efficiency']=1
        self.loc[self.sleep_efficiency_transfer.between(0.65,0.74),'sleep_efficiency']=2
        self.loc[self.sleep_efficiency_transfer<=0.64,'sleep_efficiency']=3
        #睡眠紊乱
        self['sleep_turbulence_transfer']=self['PSQI5_2']+self['PSQI5_3']+self['PSQI5_4']+self['PSQI5_5']+self['PSQI5_6']+self['PSQI5_7']+self['PSQI5_8']+self['PSQI5_9']+self['PSQI5_10']
        self['sleep_turbulence']=(self['sleep_turbulence_transfer'])
        self.loc[self.sleep_turbulence_transfer<=0,'sleep_turbulence']=0
        self.loc[self.sleep_turbulence_transfer.between(1,9),'sleep_turbulence']=1
        self.loc[self.sleep_turbulence_transfer.between(10,18),'sleep_turbulence']=2
        self.loc[self.sleep_turbulence_transfer>=19,'sleep_turbulence']=3
        #使用睡眠药物
        self['use_sleep_medication']=self['PSQI7']
        # 白天功能紊乱
        self['daytime_dysfunction_transfer']=self['PSQI8']+self['PSQI9']
        self['daytime_dysfunction']=(self['daytime_dysfunction_transfer'])
        self.loc[self.daytime_dysfunction_transfer<=0,'daytime_dysfunction']=0
        self.loc[self.daytime_dysfunction_transfer.between(1,2),'daytime_dysfunction']=1
        self.loc[self.daytime_dysfunction_transfer.between(3,4),'daytime_dysfunction']=2
        self.loc[self.daytime_dysfunction_transfer>=5,'daytime_dysfunction']=3
        #计算总分
        self['PSQI']=self['subjective_sleep_quality']+self['sleep_latency']+self['sleep_persistence']+self['sleep_efficiency']+self['sleep_turbulence']+self['use_sleep_medication']+self['daytime_dysfunction']
        #分层
        self['sleep_quality_level']=(self['PSQI'])
        self.loc[self.PSQI.between(0,5),'sleep_quality_level']=1     # 睡眠质量好
        self.loc[self.PSQI.between(6,10),'sleep_quality_level']=2    # 睡眠质量还行
        self.loc[self.PSQI.between(11,15),'sleep_quality_level']=3   # 睡眠质量一般
        self.loc[self.PSQI.between(16,21),'sleep_quality_level']=4   # 睡眠质量差
        return self['sleep_quality_level']
    
    
    def get_PSQI_level_text(self):
        """计算文本型型睡眠质量"""
        #主观睡眠质量
        self['subjective_sleep_quality']=5-self['PSQI6']
        #睡眠潜伏期
        self['sleep_latency_transfer']=self['PSQI2']-1+self['PSQI5_1']-1
        self['sleep_latency']=(self['sleep_latency_transfer'])
        self.loc[self.sleep_latency_transfer<=0,'sleep_latency']=0
        self.loc[self.sleep_latency_transfer.between(1,2),'sleep_latency']=1
        self.loc[self.sleep_latency_transfer.between(3,4),'sleep_latency']=2
        self.loc[self.sleep_latency_transfer.between(5,6),'sleep_latency']=3
        # 睡眠持续性
        self['sleep_persistence_transfer']=(self['PSQI4_1']*60+self['PSQI4_2'])/60
        self['sleep_persistence']=(self['sleep_persistence_transfer'])
        self.loc[self.sleep_persistence_transfer>7,'sleep_persistence']=0
        self.loc[self.sleep_persistence_transfer.between(6,7),'sleep_persistence']=1
        self.loc[self.sleep_persistence_transfer.between(5,6),'sleep_persistence']=2
        self.loc[self.sleep_persistence_transfer<5,'sleep_persistence']=3
        # 睡眠效率
        self['stay_in_bed']=(12*60+self['PSQI3_1']*60+self['PSQI3_2'])-(self['PSQI1_1']*60+self['PSQI1_2'])
        self['sleep_in_bed']=self['PSQI4_1']*60+self['PSQI4_2']
        self['sleep_efficiency_transfer']=round(self['sleep_in_bed']/self['stay_in_bed'],2)
        self['sleep_efficiency']=(self['sleep_efficiency_transfer'])
        self.loc[self.sleep_efficiency_transfer>=0.85,'sleep_efficiency']=0
        self.loc[self.sleep_efficiency_transfer.between(0.75,0.84),'sleep_efficiency']=1
        self.loc[self.sleep_efficiency_transfer.between(0.65,0.74),'sleep_efficiency']=2
        self.loc[self.sleep_efficiency_transfer<=0.64,'sleep_efficiency']=3
        #睡眠紊乱
        self['sleep_turbulence_transfer']=self['PSQI5_2']+self['PSQI5_3']+self['PSQI5_4']+self['PSQI5_5']+self['PSQI5_6']+self['PSQI5_7']+self['PSQI5_8']+self['PSQI5_9']+self['PSQI5_10']
        self['sleep_turbulence']=(self['sleep_turbulence_transfer'])
        self.loc[self.sleep_turbulence_transfer<=0,'sleep_turbulence']=0
        self.loc[self.sleep_turbulence_transfer.between(1,9),'sleep_turbulence']=1
        self.loc[self.sleep_turbulence_transfer.between(10,18),'sleep_turbulence']=2
        self.loc[self.sleep_turbulence_transfer>=19,'sleep_turbulence']=3
        #使用睡眠药物
        self['use_sleep_medication']=self['PSQI7']
        # 白天功能紊乱
        self['daytime_dysfunction_transfer']=self['PSQI8']+self['PSQI9']
        self['daytime_dysfunction']=(self['daytime_dysfunction_transfer'])
        self.loc[self.daytime_dysfunction_transfer<=0,'daytime_dysfunction']=0
        self.loc[self.daytime_dysfunction_transfer.between(1,2),'daytime_dysfunction']=1
        self.loc[self.daytime_dysfunction_transfer.between(3,4),'daytime_dysfunction']=2
        self.loc[self.daytime_dysfunction_transfer>=5,'daytime_dysfunction']=3
        #计算总分
        self['PSQI']=self['subjective_sleep_quality']+self['sleep_latency']+self['sleep_persistence']+self['sleep_efficiency']+self['sleep_turbulence']+self['use_sleep_medication']+self['daytime_dysfunction']
        #分层
        self['sleep_quality_level']=(self['PSQI'])
        self.loc[self.PSQI.between(0,5),'sleep_quality_level']= 'Good'      # 睡眠质量好
        self.loc[self.PSQI.between(6,10),'sleep_quality_level']= 'Fair'     # 睡眠质量还行
        self.loc[self.PSQI.between(11,15),'sleep_quality_level']= 'Limited' # 睡眠质量一般
        self.loc[self.PSQI.between(16,21),'sleep_quality_level']= 'Poor'    # 睡眠质量差
        return self['sleep_quality_level']
        
    ########## 三、个人特质 ##########
    def get_Mini_K(self):
        self['life_strategy']=(self['mini1']+self['mini2']+self['mini3']+self['mini4']+self['mini5']+self['mini6']+self['mini7']++self['mini8']+self['mini9']+self['mini10']+self['mini11']+self['mini12']+self['mini13']+self['mini14']+self['mini15']+self['mini16']+self['mini17']+self['mini18']+self['mini19'])/19
        return self['life_strategy']
    
    
    def get_LPQ_subscales(self):
        """计算LPQ量表分量表分数"""
        import pandas as pd
        # 维度
        self['event_load'] = self['LPQ1']+self['LPQ2']+self['LPQ3']+self['LPQ4']+self['LPQ5']+self['LPQ6']+self['LPQ7']+self['LPQ8']+self['LPQ9']+self['LPQ10']
        self['individual_vulnerability'] = self['LPQ11']+self['LPQ12']+self['LPQ13']+self['LPQ14']+self['LPQ15']+self['LPQ16']+self['LPQ17']+self['LPQ18']+self['LPQ19']+self['LPQ20']+self['LPQ21']+self['LPQ22']
        data = pd.DataFrame(list(zip(self['event_load'],self['individual_load'])))
        data.columns = ['event_load','individual_load']
        return data
        
    def get_LPQ_type_numeric(self):
        """计算LPQ量表分型【1 = ; 2 = ; 3 = ; 4 = 】"""
        # 维度
        self['event_load'] = self['LPQ1']+self['LPQ2']+self['LPQ3']+self['LPQ4']+self['LPQ5']+self['LPQ6']+self['LPQ7']+self['LPQ8']+self['LPQ9']+self['LPQ10']
        self['individual_vulnerability'] = self['LPQ11']+self['LPQ12']+self['LPQ13']+self['LPQ14']+self['LPQ15']+self['LPQ16']+self['LPQ17']+self['LPQ18']+self['LPQ19']+self['LPQ20']+self['LPQ21']+self['LPQ22']
        # 分型
        self['LPQ_type']=(self['individual_vulnerability'])
        self.loc[(self['individual_vulnerability'].between(12,36))&(self['event_load'].between(10,30)),'LPQ_type']=1 # 低压力
        self.loc[(self['individual_vulnerability'].between(37,60))&(self['event_load'].between(10,30)),'LPQ_type']=2 # 易感性
        self.loc[(self['individual_vulnerability'].between(12,36))&(self['event_load'].between(31,50)),'LPQ_type']=3 # 冲击性
        self.loc[(self['individual_vulnerability'].between(37,60))&(self['event_load'].between(31,50)),'LPQ_type']=4 # 高压力
        return self['individual_vulnerability']
    
    def get_LPQ_type_text(self):
        """计算LPQ量表分型"""
        # 维度
        self['event_load'] = self['LPQ1']+self['LPQ2']+self['LPQ3']+self['LPQ4']+self['LPQ5']+self['LPQ6']+self['LPQ7']+self['LPQ8']+self['LPQ9']+self['LPQ10']
        self['individual_vulnerability'] = self['LPQ11']+self['LPQ12']+self['LPQ13']+self['LPQ14']+self['LPQ15']+self['LPQ16']+self['LPQ17']+self['LPQ18']+self['LPQ19']+self['LPQ20']+self['LPQ21']+self['LPQ22']
        # 分型
        self['LPQ_type']=(self['individual_vulnerability'])
        self.loc[(self['individual_vulnerability'].between(12,36))&(self['event_load'].between(10,30)),'LPQ_type']=1 # 低压力
        self.loc[(self['individual_vulnerability'].between(37,60))&(self['event_load'].between(10,30)),'LPQ_type']=2 # 易感性
        self.loc[(self['individual_vulnerability'].between(12,36))&(self['event_load'].between(31,50)),'LPQ_type']=3 # 冲击性
        self.loc[(self['individual_vulnerability'].between(37,60))&(self['event_load'].between(31,50)),'LPQ_type']=4 # 高压力
        return self['individual_vulnerability']
    
    def get_BAS_subscales(self):
        import pandas as pd
        self['BASR']=self['BAS4']+self['BAS5']+self['BAS7']+self['BAS14']+self['BAS18']+self['BAS23']
        self['BASD']=self['BAS3']+self['BAS9']+self['BAS12']+self['BAS21']
        self['BASF']=self['BAS10']+self['BAS15']+self['BAS16']+self['BAS20']
        self['BIS']=self['BAS8']+self['BAS13']+self['BAS16']+self['BAS19']+self['BAS24']
        data = pd.DataFrame(list(zip(self['BASR'],self['BASD'],self['BASF'],self['BIS'])))
        data.columns = ['BASR','BASD','BASF','BIS']
        return data
    
    def get_TAS_subscales(self):
        import pandas as pd
        #计算TAS维度
        self['difficult_to_recognize_feeling']=self['TAS1']+self['TAS3']+self['TAS6']+self['TAS7']+self['TAS9']+self['TAS13']+self['TAS14']
        self['difficult_to_describe_feeling']=self['TAS2']+self['TAS4']+self['TAS11']+self['TAS12']+self['TAS17']
        self['extraversion_thought']=self['TAS5']+self['TAS8']+self['TAS10']+self['TAS15']+self['TAS16']+self['TAS18']+self['TAS19']+self['TAS20']
        data = pd.DataFrame(list(zip(self['difficult_to_recognize_feeling'],self['difficult_to_describe_feeling'],self['extraversion_thought'])))
        data.columns = ['difficult_to_recognize_feeling','difficult_to_describe_feeling','extraversion_thought']
        return data
    
    def get_TAS(self):
        
        #计算TAS维度
        self['difficult_to_recognize_feeling']=self['TAS1']+self['TAS3']+self['TAS6']+self['TAS7']+self['TAS9']+self['TAS13']+self['TAS14']
        self['difficult_to_describe_feeling']=self['TAS2']+self['TAS4']+self['TAS11']+self['TAS12']+self['TAS17']
        self['extraversion_thought']=self['TAS5']+self['TAS8']+self['TAS10']+self['TAS15']+self['TAS16']+self['TAS18']+self['TAS19']+self['TAS20']
        #计算TAS总分
        self['TAS']=self['difficult_to_recognize_feeling']+self['difficult_to_describe_feeling']+self['extraversion_thought']
        return self['TAS']
    
    def get_ERQ_subscales(self):
        """计算ERQ分数"""
        import pandas as pd
        self['cognitive_reappraisal']=self['ERQ1']+self['ERQ3']+self['ERQ4']+self['ERQ5']+self['ERQ7']+self['ERQ8']
        self['expression_inhibition']=self['ERQ2']+self['ERQ4']+self['ERQ6']+self['ERQ9']
        data = pd.DataFrame(list(zip(self['cognitive_reappraisal'],self['expression_inhibition'])))
        data.columns = ['cognitive_reappraisal','expression_inhibition']
        return data
    
    def get_BPAQ_subscales(self):
        """使用Buss_Perry中文22题修订版，《中文版大学生Buss-Perry攻击性量表的修订与信效度分析，心理卫生评估，2013》"""
        import pandas as pd
        self['hostility'] = self['BPAQ18']+self['BPAQ15']+self['BPAQ4']+self['BPAQ21']+self['BPAQ11']+self['BPAQ16']+self['BPAQ7']+self['BPAQ19']
        self['physical_aggression'] = self['BPAQ17']+self['BPAQ13']+self['BPAQ12']+self['BPAQ22']+self['BPAQ9']
        self['impulsivity'] = self['BPAQ10']+self['BPAQ6']+self['BPAQ14']+self['BPAQ8']+self['BPAQ2']+self['BPAQ3']
        self['anger'] = self['BPAQ1']+self['BPAQ20']+self['BPAQ5']
        data = pd.DataFrame(list(zip(self['hostility'],self['physical_aggression'],self['impulsivity'],self['anger'])))
        data.columns = ['hostility','physical_aggression','impulsivity','anger']
        return data
    
    def get_EQ(self):
        """计算共情量表得分
        参考文献：
        [1] The Empathy Quotient: An Investigation of Adults with Asperger Syndrome or High Functioning Autism, and Normal Sex Differences
        [2] Measuring empathy: reliability and validity of the Empathy Quotient
        [3] https://www.autismresearchcentre.com/tests/empathy-quotient-eq-for-adults/"""
        # 正向计分
        def forward(a):
            if a >= 3:
                b = a-2
            else:
                b = 0
            return b
        def reverse(a):
            if a >= 3:
                b = 0
            elif a == 2:
                b = 1
            else:
                b = 2
            return b
        
        self['empathy_forward'] = self['EQ1'].apply(forward)+self['EQ6'].apply(forward)+self['EQ19'].apply(forward)+self['EQ22'].apply(forward)+self['EQ25'].apply(forward)+self['EQ26'].apply(forward)+self['EQ35'].apply(forward)+self['EQ36'].apply(forward)+self['EQ37'].apply(forward)+self['EQ38'].apply(forward)+self['EQ41'].apply(forward)+self['EQ42'].apply(forward)+self['EQ43'].apply(forward)+self['EQ44'].apply(forward)+self['EQ52'].apply(forward)+self['EQ54'].apply(forward)+self['EQ55'].apply(forward)+self['EQ57'].apply(forward)+self['EQ58'].apply(forward)+self['EQ59'].apply(forward)+self['EQ60'].apply(forward)        
        self['empathy_reverse'] = self['EQ4'].apply(reverse)+self['EQ8'].apply(reverse)+self['EQ10'].apply(reverse)+self['EQ11'].apply(reverse)+self['EQ12'].apply(reverse)+self['EQ14'].apply(reverse)+self['EQ15'].apply(reverse)+self['EQ18'].apply(reverse)+self['EQ21'].apply(reverse)+self['EQ27'].apply(reverse)+self['EQ28'].apply(reverse)+self['EQ29'].apply(reverse)+self['EQ32'].apply(reverse)+self['EQ34'].apply(reverse)+self['EQ39'].apply(reverse)+self['EQ46'].apply(reverse)+self['EQ48'].apply(reverse)+self['EQ49'].apply(reverse)+self['EQ50'].apply(reverse)
        self['empathy'] = self['empathy_forward'] + self ['empathy_reverse']
        return self['empathy']
    
    #def get_EQ_subscales(self):

    ########## 四、社会环境 ##########
    def get_CTQ_subscales(self):
        import pandas as pd
        self['emotional_abuse']=self['CTQ3']+self['CTQ8']+self['CTQ14']+self['CTQ18']+self['CTQ25']
        self['physical_abuse']=self['CTQ9']+self['CTQ11']+self['CTQ12']+self['CTQ15']+self['CTQ17']
        self['sexual_abuse']=self['CTQ20']+self['CTQ21']+self['CTQ23']+self['CTQ24']+self['CTQ27']
        self['emotional_neglect']=(6-self['CTQ5'])+(6-self['CTQ7'])+(6-self['CTQ12'])+(6-self['CTQ15'])+(6-self['CTQ17'])
        self['physical_neglect']=self['CTQ1']+6-self['CTQ2']+self['CTQ4']+self['CTQ6']+6-self['CTQ26']
        data = pd.DataFrame(list(zip(self['emotional_abuse'],self['physical_abuse'],self['sexual_abuse'],self['emotional_neglect'],self['physical_neglect'])))
        data.columns = ['emotional_abuse','physical_abuse','sexual_abuse','emotional_neglect','physical_neglect']
        return data
    
    def get_CTQ(self):
        self['emotional_abuse']=self['CTQ3']+self['CTQ8']+self['CTQ14']+self['CTQ18']+self['CTQ25']
        self['physical_abuse']=self['CTQ9']+self['CTQ11']+self['CTQ12']+self['CTQ15']+self['CTQ17']
        seldeff['sexual_abuse']=self['CTQ20']+self['CTQ21']+self['CTQ23']+self['CTQ24']+self['CTQ27']
        self['emotional_neglect']=(6-self['CTQ5'])+(6-self['CTQ7'])+(6-self['CTQ12'])+(6-self['CTQ15'])+(6-self['CTQ17'])
        self['physical_neglect']=self['CTQ1']+6-self['CTQ2']+self['CTQ4']+self['CTQ6']+6-self['CTQ26']
        self['CTQ']=self['emotional_abuse']+self['physical_abuse']+self['sexual_abuse']+self['emotional_neglect']+self['physical_neglect']
        return self['CTQ']
    
    def get_CTQ_whether_numeric(self):
        """判断各方面的童年虐待是否存在【1 = 构成童年虐待；0 = 不构成童年虐待】"""
        self['whether_emotional_abuse']=(self['emotional_abuse'])
        self.loc[self.emotional_abuse>=13,'whether_emotional_abuse']= 1
        self.loc[self.emotional_abuse<13,'whether_emotional_abuse']=0
        self['whether_physical_abuse']=(self['physical_abuse'])
        self.loc[self.physical_abuse>=10,'whether_physical_abuse']= 1
        self.loc[self.physical_abuse<10,'whether_physical_abuse']= 0
        self['whether_sexual_abuse']=(self['sexual_abuse'])
        self.loc[self.sexual_abuse>=8,'whether_sexual_abuse']=1
        self.loc[self.sexual_abuse<8,'whether_sexual_abuse']=0 
        self['whether_emotional_neglect']=(self['emotional_neglect'])
        self.loc[self.emotional_neglect>=15,'whether_emotional_neglect']=1
        self.loc[self.emotional_neglect<15,'whether_emotional_neglect']=0
        self['whether_physical_neglect']=(self['physical_neglect'])
        self.loc[self.physical_neglect>=15,'whether_physical_neglect']=1
        self.loc[self.physical_neglect<15,'whether_physical_neglect']=0
        return self['whether_emotional_abuse'],self['whether_physical_abuse','whether_sexual_abuse','whether_emotional_neglect','whether_physical_neglect']

    
    
    #def get_SSQ_subscales(self):
        #self['SSQ_1']=self['SSQ1']+self['SSQ3']+self['SSQ5']+self['SSQ7']+self['SSQ9']+self['SSQ11']
        #self['SSQ_2']=self['SSQ2']+self['SSQ4']+self['SSQ6']+self['SSQ8']+self['SSQ10']+self['SSQ12']
        
        
    def get_SSQ(self):
        """计算社会支持总分"""
        self['SSQ_1']=self['SSQ1']+self['SSQ3']+self['SSQ5']+self['SSQ7']+self['SSQ9']+self['SSQ11']
        self['SSQ_2']=self['SSQ2']+self['SSQ4']+self['SSQ6']+self['SSQ8']+self['SSQ10']+self['SSQ12']
        self['SSQ']=self['SSQ_1']+self['SSQ_2']
        return self['SSQ']

    ######### 五、症状评估 ##########
        
    def get_AUDIT(self):
        self['AUDIT9_transfer']=(self['AUDIT9'])
        self['AUDIT10_transfer']=(self['AUDIT10'])
        self.loc[self.AUDIT9<=1,'AUDIT9_transfer']=0
        self.loc[self.AUDIT10<=1,'AUDIT10_transfer']=0
        self.loc[self.AUDIT9>=4,'AUDIT9_transfer']=3
        self.loc[self.AUDIT10>=4,'AUDIT10_transfer']=3
        self['AUDIT']=self['AUDIT1']+self['AUDIT2']+self['AUDIT3']+self['AUDIT4']+self['AUDIT5']+self['AUDIT6']+self['AUDIT7']+self['AUDIT8']+self['AUDIT9_transfer']+self['AUDIT10_transfer']-8
        return self['AUDIT']
    
    def get_FTND(self):
        self['FTND']=self['FTND1']+self['FTND2']+self['FTND3']+self['FTND4']+self['FTND5']+self['FTND6']-6
        return self['FTND']
    
    def get_FTND_whether_numeric(self):
        self['FTND_whether']=(self['FTND'])
        self.loc[self.FTND>=6,'FTND_whether']=1
        self.loc[self.FTND<6,'FTND_whether']=0
        return self['FTND_whether']
    
    
    def get_EDI_subscales(self):
        import pandas as pd
        """计算EDI得分，来自陈珏老师组"""
        def transfer(a):
            if a <= 2:
                b=0
            else:
                b=a-2
            return b
        self['drive_for_thinness']=((self['EDI1']-1).apply(transfer)+(self['EDI7']-1).apply(transfer)+(self['EDI11']-1).apply(transfer)+(self['EDI16']-1).apply(transfer)+(self['EDI25']-1).apply(transfer)+(self['EDI32']-1).apply(transfer)+(self['EDI49']-1).apply(transfer))/7
        self['bulimia']=((self['EDI4']-1).apply(transfer)+(self['EDI5']-1).apply(transfer)+(self['EDI28']-1).apply(transfer)+(self['EDI38']-1).apply(transfer)+(self['EDI46']-1).apply(transfer)+(self['EDI53']-1).apply(transfer)+(self['EDI61']-1).apply(transfer))/7
        self['body_dissatisfaction']=((self['EDI2']-1).apply(transfer)+(self['EDI9']-1).apply(transfer)+(3-(self['EDI12']-1).apply(transfer))+3-((self['EDI19']-1).apply(transfer))+abs(3-(self['EDI31']-1).apply(transfer))+(self['EDI45']-1).apply(transfer).apply(transfer)+abs(3-(self['EDI55']-1)).apply(transfer)+(self['EDI59']-1).apply(transfer)+abs(3-(self['EDI62']-1).apply(transfer)))/9
        self['ineffectiveness']=((self['EDI10']-1).apply(transfer)+(self['EDI18']-1).apply(transfer)+abs(3-(self['EDI20']-1).apply(transfer))+(self['EDI24']-1).apply(transfer)+(self['EDI27']-1).apply(transfer)+abs(3-(self['EDI37']-1).apply(transfer))+(self['EDI41']-1+(self['EDI42']-1).apply(transfer)+abs(3-(self['EDI50']-1).apply(transfer))+(self['EDI56']-1).apply(transfer)).apply(transfer))/10
        self['perfectionism']=((self['EDI13']-1).apply(transfer)+(self['EDI29']-1).apply(transfer)+(self['EDI36']-1).apply(transfer)+(self['EDI43']-1).apply(transfer)+(self['EDI52']-1).apply(transfer)+(self['EDI63']-1).apply(transfer))/6
        self['interpersonal_distrust']=(abs(3-(self['EDI15']-1).apply(transfer))+abs(3-(self['EDI17']-1).apply(transfer))+abs(3-(self['EDI23']-1).apply(transfer))+abs(3-(self['EDI30']-1).apply(transfer))+(self['EDI34']-1).apply(transfer)+(self['EDI54']-1).apply(transfer)+abs(3-(self['EDI57']-1).apply(transfer)))/7
        self['interoceptive_awareness']=((self['EDI8']-1).apply(transfer)+(self['EDI21']-1).apply(transfer)+abs(3-(self['EDI26']-1).apply(transfer))+(self['EDI33']-1).apply(transfer)+(self['EDI40']-1).apply(transfer)+(self['EDI44']-1).apply(transfer)+(self['EDI47']-1).apply(transfer)+(self['EDI51']-1).apply(transfer)+(self['EDI60']-1).apply(transfer)+(self['EDI64']-1).apply(transfer))/10
        self['maturity_fears']=((self['EDI3']-1).apply(transfer)+(self['EDI6']-1).apply(transfer)+(self['EDI14']-1).apply(transfer)+abs(3-(self['EDI22']-1).apply(transfer))+(self['EDI35']-1).apply(transfer)+abs(3-(self['EDI39']-1).apply(transfer))+(self['EDI48']-1).apply(transfer)+abs(3-(self['EDI58']-1).apply(transfer)))/8
        self['asceticism_subscale']=((self['EDI66']-1).apply(transfer)+(self['EDI68']-1).apply(transfer)+abs(3-(self['EDI71']-1).apply(transfer))+(self['EDI75']-1).apply(transfer)+(self['EDI78']-1).apply(transfer)+(self['EDI82']-1).apply(transfer)+(self['EDI86']-1+(self['EDI88']-1).apply(transfer)).apply(transfer))/8
        self['impulse_regulation_subscale']=((self['EDI65']-1).apply(transfer)+(self['EDI67']-1).apply(transfer)+(self['EDI70']-1).apply(transfer)+(self['EDI72']-1).apply(transfer)+(self['EDI74']-1).apply(transfer)+(self['EDI77']-1).apply(transfer)+(self['EDI79']-1+(self['EDI81']-1).apply(transfer)+(self['EDI83']-1).apply(transfer)+(self['EDI85']-1).apply(transfer)+(self['EDI90']-1).apply(transfer)).apply(transfer))/11
        self['social_insecurity_subscale']=(abs(3-(self['EDI69']-1).apply(transfer))+abs(3-(self['EDI73']-1).apply(transfer))+abs(3-(self['EDI76']-1).apply(transfer))+abs(3-(self['EDI80']-1).apply(transfer))+(self['EDI84']-1).apply(transfer)+(self['EDI87']-1).apply(transfer)+abs(3-(self['EDI89']-1).apply(transfer))+abs(3-(self['EDI91']-1).apply(transfer)))/8
        self['social_insecurity_subscale_false']=((self['EDI69']-1).apply(transfer)+(self['EDI73']-1).apply(transfer)+(self['EDI76']-1).apply(transfer)+(self['EDI80']-1).apply(transfer)+(self['EDI84']-1).apply(transfer)+(self['EDI87']-1).apply(transfer)+(self['EDI89']-1).apply(transfer))/7
        data = pd.DataFrame(list(zip(self['drive_for_thinness'],self['bulimia'],self['body_dissatisfaction'],self['ineffectiveness'],self['perfectionism'],self['interpersonal_distrust'],self['interoceptive_awareness'],self['maturity_fears'],self['asceticism_subscale'],self['impulse_regulation_subscale'],self['social_insecurity_subscale'],self['social_insecurity_subscale_false'])))
        data.columns = ['drive_for_thinness','bulimia','body_dissatisfaction','ineffectiveness','perfectionism','interpersonal_distrust','interoceptive_awareness','maturity_fears','asceticism_subscale','impulse_regulation_subscale','social_insecurity_subscale','social_insecurity_subscale_false']
        return data
    
    def get_YFAS_subscales(self):
        import pandas as pd
        """计算YFAS耶鲁食物成瘾量表各分量表分数"""
        # 复制原始数值
        self['YFAS_1']=(self['YFAS1'])
        self['YFAS_2']=(self['YFAS2'])
        self['YFAS_3']=(self['YFAS3'])
        self['YFAS_4']=(self['YFAS4'])
        self['YFAS_5']=(self['YFAS5'])
        self['YFAS_6']=(self['YFAS6'])
        self['YFAS_7']=(self['YFAS7'])
        self['YFAS_8']=(self['YFAS8'])
        self['YFAS_9']=(self['YFAS9'])
        self['YFAS_10']=(self['YFAS10'])
        self['YFAS_11']=(self['YFAS11'])
        self['YFAS_12']=(self['YFAS12'])
        self['YFAS_13']=(self['YFAS13'])
        self['YFAS_14']=(self['YFAS14'])
        self['YFAS_15']=(self['YFAS15'])
        self['YFAS_16']=(self['YFAS16'])
        self['YFAS_17']=(self['YFAS17'])
        self['YFAS_18']=(self['YFAS18'])
        self['YFAS_19']=(self['YFAS19'])
        self['YFAS_20']=(self['YFAS20'])
        self['YFAS_21']=(self['YFAS21'])
        self['YFAS_22']=(self['YFAS22'])
        self['YFAS_23']=(self['YFAS23'])
        self['YFAS_24']=(self['YFAS24'])
        self['YFAS_25']=(self['YFAS25'])
        self['YFAS_26']=(self['YFAS26'])
        self['YFAS_27']=(self['YFAS27'])
        self['YFAS_28']=(self['YFAS28'])
        self['YFAS_29']=(self['YFAS29'])
        self['YFAS_30']=(self['YFAS30'])
        self['YFAS_31']=(self['YFAS31'])
        self['YFAS_32']=(self['YFAS32'])
        self['YFAS_33']=(self['YFAS33'])
        self['YFAS_34']=(self['YFAS34'])
        self['YFAS_35']=(self['YFAS35'])

        #题目分数转换
        #1)	Once a month: #9, #10, #19, #27, #33, #35
        self.loc[(self['YFAS9'])>=2,'YFAS_9']=1
        self.loc[(self['YFAS9'])<2,'YFAS_9']=0
        self.loc[(self['YFAS10'])>=2,'YFAS_10']=1
        self.loc[(self['YFAS10'])<2,'YFAS_10']=0
        self.loc[(self['YFAS19'])>=2,'YFAS_19']=1
        self.loc[(self['YFAS19'])<2,'YFAS_19']=0
        self.loc[(self['YFAS27'])>=2,'YFAS_27']=1
        self.loc[(self['YFAS27'])<2,'YFAS_27']=0
        self.loc[(self['YFAS33'])>=2,'YFAS_33']=1
        self.loc[(self['YFAS33'])<2,'YFAS_33']=0
        self.loc[(self['YFAS35'])>=2,'YFAS_35']=1
        self.loc[(self['YFAS35'])<2,'YFAS_35']=0
        #2)	Two to three times a month: #8, #18, #20, #21, #34
        self.loc[(self['YFAS8'])>=3,'YFAS_8']=1
        self.loc[(self['YFAS8'])<3,'YFAS_8']=0
        self.loc[(self['YFAS18'])>=3,'YFAS_18']=1
        self.loc[(self['YFAS18'])<3,'YFAS_18']=0
        self.loc[(self['YFAS20'])>=3,'YFAS_20']=1
        self.loc[(self['YFAS20'])<3,'YFAS_20']=0
        self.loc[(self['YFAS21'])>=3,'YFAS_21']=1
        self.loc[(self['YFAS21'])<3,'YFAS_21']=0
        self.loc[(self['YFAS34'])>=3,'YFAS_34']=1
        self.loc[(self['YFAS34'])<3,'YFAS_34']=0
        #3)	Once a week: #3, #11, #13, #14, #22, #28, #29
        self.loc[(self['YFAS3'])>=4,'YFAS_3']=1
        self.loc[(self['YFAS3'])<4,'YFAS_3']=0
        self.loc[(self['YFAS11'])>=4,'YFAS_11']=1
        self.loc[(self['YFAS11'])<4,'YFAS_11']=0
        self.loc[(self['YFAS13'])>=4,'YFAS_13']=1
        self.loc[(self['YFAS13'])<4,'YFAS_13']=0
        self.loc[(self['YFAS14'])>=4,'YFAS_14']=1
        self.loc[(self['YFAS14'])<4,'YFAS_14']=0
        self.loc[(self['YFAS22'])>=4,'YFAS_22']=1
        self.loc[(self['YFAS22'])<4,'YFAS_22']=0
        self.loc[(self['YFAS28'])>=4,'YFAS_28']=1
        self.loc[(self['YFAS28'])<4,'YFAS_28']=0
        self.loc[(self['YFAS29'])>=4,'YFAS_29']=1
        self.loc[(self['YFAS29'])<4,'YFAS_29']=0
        #4)	Two to three time's a week: #5, #12, #16, #17, #23, #24, #26, #30, #31, #32
        self.loc[(self['YFAS5'])>=5,'YFAS_5']=1
        self.loc[(self['YFAS5'])<5,'YFAS_5']=0
        self.loc[(self['YFAS12'])>=5,'YFAS_12']=1
        self.loc[(self['YFAS12'])<5,'YFAS_12']=0
        self.loc[(self['YFAS16'])>=5,'YFAS_16']=1
        self.loc[(self['YFAS16'])<5,'YFAS_16']=0
        self.loc[(self['YFAS17'])>=5,'YFAS_17']=1
        self.loc[(self['YFAS17'])<5,'YFAS_17']=0
        self.loc[(self['YFAS23'])>=5,'YFAS_23']=1
        self.loc[(self['YFAS23'])<5,'YFAS_23']=0
        self.loc[(self['YFAS24'])>=5,'YFAS_24']=1
        self.loc[(self['YFAS24'])<5,'YFAS_24']=0
        self.loc[(self['YFAS26'])>=5,'YFAS_26']=1
        self.loc[(self['YFAS26'])<5,'YFAS_26']=0
        self.loc[(self['YFAS30'])>=5,'YFAS_30']=1
        self.loc[(self['YFAS30'])<5,'YFAS_30']=0
        self.loc[(self['YFAS31'])>=5,'YFAS_31']=1
        self.loc[(self['YFAS31'])<5,'YFAS_31']=0
        self.loc[(self['YFAS32'])>=5,'YFAS_32']=1
        self.loc[(self['YFAS32'])<5,'YFAS_32']=0
        #5)	Four to six times a week: #1, #2, #4, #6, #7, #15, #25
        self.loc[(self['YFAS1'])>=6,'YFAS_1']=1
        self.loc[(self['YFAS1'])<6,'YFAS_1']=0
        self.loc[(self['YFAS2'])>=6,'YFAS_2']=1
        self.loc[(self['YFAS2'])<6,'YFAS_2']=0
        self.loc[(self['YFAS4'])>=6,'YFAS_4']=1
        self.loc[(self['YFAS4'])<6,'YFAS_4']=0
        self.loc[(self['YFAS6'])>=6,'YFAS_6']=1
        self.loc[(self['YFAS6'])<6,'YFAS_6']=0
        self.loc[(self['YFAS7'])>=6,'YFAS_7']=1
        self.loc[(self['YFAS7'])<6,'YFAS_7']=0
        self.loc[(self['YFAS15'])>=6,'YFAS_15']=1
        self.loc[(self['YFAS15'])<6,'YFAS_15']=0
        self.loc[(self['YFAS25'])>=6,'YFAS_25']=1
        self.loc[(self['YFAS25'])<6,'YFAS_25']=0
        #维度分
        self['1_longer_than_intend'] = self['YFAS_1'] + self['YFAS_2'] + self['YFAS_3']
        self['2_unsuccessful_attempts'] = self['YFAS_4'] + self['YFAS_25'] + self['YFAS_31'] + self['YFAS_32']
        self['3_much_time'] = self['YFAS_5'] + self['YFAS_6'] + self['YFAS_7']
        self['4_given_up'] = self['YFAS_8'] + self['YFAS_10'] + self['YFAS_18'] + self['YFAS_20']
        self['5_despite_adverse_consequences'] = self['YFAS_22'] + self['YFAS_23']
        self['6_tolerance'] = self['YFAS_24'] + self['YFAS_26']
        self['7_withdraw_symptoms'] = self['YFAS_11'] + self['YFAS_12']+ self['YFAS_13']+ self['YFAS_14']+ self['YFAS_15']
        self['8_despite_interpersonal_problems'] = self['YFAS_9'] + self['YFAS_21']+ self['YFAS_35']
        self['9_failure_role'] = self['YFAS_19'] + self['YFAS_27']
        self['10_failure_role'] = self['YFAS_28'] + self['YFAS_33']+ self['YFAS_34']
        self['11_craving'] = self['YFAS_29'] + self['YFAS_30']
        self['12_clinical_impairment'] = self['YFAS_16'] + self['YFAS_17']
        data = pd.DataFrame(list(zip(self['1_longer_than_intend'],self['2_unsuccessful_attempts'],self['3_much_time'],self['4_given_up'],self['5_despite_adverse_consequences'],self['6_tolerance'],self['7_withdraw_symptoms'],self['8_despite_interpersonal_problems'],self['9_failure_role'],self['10_failure_role'],self['11_craving'],self['12_clinical_impairment'])))
        data.columns = ['1_longer_than_intend','2_unsuccessful_attempts','3_much_time','4_given_up','5_despite_adverse_consequences','6_tolerance','7_withdraw_symptoms','8_despite_interpersonal_problems','9_failure_role','10_failure_role','11_craving','12_clinical_impairment']
        return data
    
    def get_YFAS(self):
        """计算YFAS耶鲁食物成瘾量表总分"""
        import numpy as np
        # 复制原始数值
        self['YFAS_1']=(self['YFAS1'])
        self['YFAS_2']=(self['YFAS2'])
        self['YFAS_3']=(self['YFAS3'])
        self['YFAS_4']=(self['YFAS4'])
        self['YFAS_5']=(self['YFAS5'])
        self['YFAS_6']=(self['YFAS6'])
        self['YFAS_7']=(self['YFAS7'])
        self['YFAS_8']=(self['YFAS8'])
        self['YFAS_9']=(self['YFAS9'])
        self['YFAS_10']=(self['YFAS10'])
        self['YFAS_11']=(self['YFAS11'])
        self['YFAS_12']=(self['YFAS12'])
        self['YFAS_13']=(self['YFAS13'])
        self['YFAS_14']=(self['YFAS14'])
        self['YFAS_15']=(self['YFAS15'])
        self['YFAS_16']=(self['YFAS16'])
        self['YFAS_17']=(self['YFAS17'])
        self['YFAS_18']=(self['YFAS18'])
        self['YFAS_19']=(self['YFAS19'])
        self['YFAS_20']=(self['YFAS20'])
        self['YFAS_21']=(self['YFAS21'])
        self['YFAS_22']=(self['YFAS22'])
        self['YFAS_23']=(self['YFAS23'])
        self['YFAS_24']=(self['YFAS24'])
        self['YFAS_25']=(self['YFAS25'])
        self['YFAS_26']=(self['YFAS26'])
        self['YFAS_27']=(self['YFAS27'])
        self['YFAS_28']=(self['YFAS28'])
        self['YFAS_29']=(self['YFAS29'])
        self['YFAS_30']=(self['YFAS30'])
        self['YFAS_31']=(self['YFAS31'])
        self['YFAS_32']=(self['YFAS32'])
        self['YFAS_33']=(self['YFAS33'])
        self['YFAS_34']=(self['YFAS34'])
        self['YFAS_35']=(self['YFAS35'])

        #题目分数转换
        #1)	Once a month: #9, #10, #19, #27, #33, #35
        self.loc[(self['YFAS9'])>=2,'YFAS_9']=1
        self.loc[(self['YFAS9'])<2,'YFAS_9']=0
        self.loc[(self['YFAS10'])>=2,'YFAS_10']=1
        self.loc[(self['YFAS10'])<2,'YFAS_10']=0
        self.loc[(self['YFAS19'])>=2,'YFAS_19']=1
        self.loc[(self['YFAS19'])<2,'YFAS_19']=0
        self.loc[(self['YFAS27'])>=2,'YFAS_27']=1
        self.loc[(self['YFAS27'])<2,'YFAS_27']=0
        self.loc[(self['YFAS33'])>=2,'YFAS_33']=1
        self.loc[(self['YFAS33'])<2,'YFAS_33']=0
        self.loc[(self['YFAS35'])>=2,'YFAS_35']=1
        self.loc[(self['YFAS35'])<2,'YFAS_35']=0
        #2)	Two to three times a month: #8, #18, #20, #21, #34
        self.loc[(self['YFAS8'])>=3,'YFAS_8']=1
        self.loc[(self['YFAS8'])<3,'YFAS_8']=0
        self.loc[(self['YFAS18'])>=3,'YFAS_18']=1
        self.loc[(self['YFAS18'])<3,'YFAS_18']=0
        self.loc[(self['YFAS20'])>=3,'YFAS_20']=1
        self.loc[(self['YFAS20'])<3,'YFAS_20']=0
        self.loc[(self['YFAS21'])>=3,'YFAS_21']=1
        self.loc[(self['YFAS21'])<3,'YFAS_21']=0
        self.loc[(self['YFAS34'])>=3,'YFAS_34']=1
        self.loc[(self['YFAS34'])<3,'YFAS_34']=0
        #3)	Once a week: #3, #11, #13, #14, #22, #28, #29
        self.loc[(self['YFAS3'])>=4,'YFAS_3']=1
        self.loc[(self['YFAS3'])<4,'YFAS_3']=0
        self.loc[(self['YFAS11'])>=4,'YFAS_11']=1
        self.loc[(self['YFAS11'])<4,'YFAS_11']=0
        self.loc[(self['YFAS13'])>=4,'YFAS_13']=1
        self.loc[(self['YFAS13'])<4,'YFAS_13']=0
        self.loc[(self['YFAS14'])>=4,'YFAS_14']=1
        self.loc[(self['YFAS14'])<4,'YFAS_14']=0
        self.loc[(self['YFAS22'])>=4,'YFAS_22']=1
        self.loc[(self['YFAS22'])<4,'YFAS_22']=0
        self.loc[(self['YFAS28'])>=4,'YFAS_28']=1
        self.loc[(self['YFAS28'])<4,'YFAS_28']=0
        self.loc[(self['YFAS29'])>=4,'YFAS_29']=1
        self.loc[(self['YFAS29'])<4,'YFAS_29']=0
        #4)	Two to three time's a week: #5, #12, #16, #17, #23, #24, #26, #30, #31, #32
        self.loc[(self['YFAS5'])>=5,'YFAS_5']=1
        self.loc[(self['YFAS5'])<5,'YFAS_5']=0
        self.loc[(self['YFAS12'])>=5,'YFAS_12']=1
        self.loc[(self['YFAS12'])<5,'YFAS_12']=0
        self.loc[(self['YFAS16'])>=5,'YFAS_16']=1
        self.loc[(self['YFAS16'])<5,'YFAS_16']=0
        self.loc[(self['YFAS17'])>=5,'YFAS_17']=1
        self.loc[(self['YFAS17'])<5,'YFAS_17']=0
        self.loc[(self['YFAS23'])>=5,'YFAS_23']=1
        self.loc[(self['YFAS23'])<5,'YFAS_23']=0
        self.loc[(self['YFAS24'])>=5,'YFAS_24']=1
        self.loc[(self['YFAS24'])<5,'YFAS_24']=0
        self.loc[(self['YFAS26'])>=5,'YFAS_26']=1
        self.loc[(self['YFAS26'])<5,'YFAS_26']=0
        self.loc[(self['YFAS30'])>=5,'YFAS_30']=1
        self.loc[(self['YFAS30'])<5,'YFAS_30']=0
        self.loc[(self['YFAS31'])>=5,'YFAS_31']=1
        self.loc[(self['YFAS31'])<5,'YFAS_31']=0
        self.loc[(self['YFAS32'])>=5,'YFAS_32']=1
        self.loc[(self['YFAS32'])<5,'YFAS_32']=0
        #5)	Four to six times a week: #1, #2, #4, #6, #7, #15, #25
        self.loc[(self['YFAS1'])>=6,'YFAS_1']=1
        self.loc[(self['YFAS1'])<6,'YFAS_1']=0
        self.loc[(self['YFAS2'])>=6,'YFAS_2']=1
        self.loc[(self['YFAS2'])<6,'YFAS_2']=0
        self.loc[(self['YFAS4'])>=6,'YFAS_4']=1
        self.loc[(self['YFAS4'])<6,'YFAS_4']=0
        self.loc[(self['YFAS6'])>=6,'YFAS_6']=1
        self.loc[(self['YFAS6'])<6,'YFAS_6']=0
        self.loc[(self['YFAS7'])>=6,'YFAS_7']=1
        self.loc[(self['YFAS7'])<6,'YFAS_7']=0
        self.loc[(self['YFAS15'])>=6,'YFAS_15']=1
        self.loc[(self['YFAS15'])<6,'YFAS_15']=0
        self.loc[(self['YFAS25'])>=6,'YFAS_25']=1
        self.loc[(self['YFAS25'])<6,'YFAS_25']=0
        #维度分
        self['1_longer_than_intend'] = self['YFAS_1'] + self['YFAS_2'] + self['YFAS_3']
        self['2_unsuccessful_attempts'] = self['YFAS_4'] + self['YFAS_25'] + self['YFAS_31'] + self['YFAS_32']
        self['3_much_time'] = self['YFAS_5'] + self['YFAS_6'] + self['YFAS_7']
        self['4_given_up'] = self['YFAS_8'] + self['YFAS_10'] + self['YFAS_18'] + self['YFAS_20']
        self['5_despite_adverse_consequences'] = self['YFAS_22'] + self['YFAS_23']
        self['6_tolerance'] = self['YFAS_24'] + self['YFAS_26']
        self['7_withdraw_symptoms'] = self['YFAS_11'] + self['YFAS_12']+ self['YFAS_13']+ self['YFAS_14']+ self['YFAS_15']
        self['8_despite_interpersonal_problems'] = self['YFAS_9'] + self['YFAS_21']+ self['YFAS_35']
        self['9_failure_role'] = self['YFAS_19'] + self['YFAS_27']
        self['10_failure_role'] = self['YFAS_28'] + self['YFAS_33']+ self['YFAS_34']
        self['11_craving'] = self['YFAS_29'] + self['YFAS_30']
        self['12_clinical_impairment'] = self['YFAS_16'] + self['YFAS_17']
        #维度分转换
        self['food_addiction_1']= np.where(self['1_longer_than_intend']>=1,1,0)
        self['food_addiction_2']= np.where(self['2_unsuccessful_attempts']>=1,1,0)
        self['food_addiction_3']= np.where(self['3_much_time']>=1,1,0)
        self['food_addiction_4']= np.where(self['4_given_up']>=1,1,0)
        self['food_addiction_5']= np.where(self['5_despite_adverse_consequences']>=1,1,0)
        self['food_addiction_6']= np.where(self['6_tolerance']>=1,1,0)
        self['food_addiction_7']= np.where(self['7_withdraw_symptoms']>=1,1,0)
        self['food_addiction_8']= np.where(self['8_despite_interpersonal_problems']>=1,1,0)
        self['food_addiction_9']= np.where(self['9_failure_role']>=1,1,0)
        self['food_addiction_10']= np.where(self['10_failure_role']>=1,1,0)
        self['food_addiction_11']= np.where(self['11_craving']>=1,1,0)
        self['food_addiction_12']= np.where(self['12_clinical_impairment']>=1,1,0)
        
        #总分计算
        self['food_addiction_score']= self['food_addiction_1']+self['food_addiction_2']+self['food_addiction_3']+self['food_addiction_4']+self['food_addiction_5']+self['food_addiction_6']+self['food_addiction_7']+self['food_addiction_8']+self['food_addiction_9']+self['food_addiction_10']+self['food_addiction_11']+self['food_addiction_12'] 
        return self['food_addiction_score']
    
    def get_YFAS_whether_numberic(self):
        """根据YFAS耶鲁食物成瘾量表总分诊断是否食物成瘾【这里临界值定为2，需要根据中国地区的情况更新】"""
        import numpy as np
        # 复制原始数值
        self['YFAS_1']=(self['YFAS1'])
        self['YFAS_2']=(self['YFAS2'])
        self['YFAS_3']=(self['YFAS3'])
        self['YFAS_4']=(self['YFAS4'])
        self['YFAS_5']=(self['YFAS5'])
        self['YFAS_6']=(self['YFAS6'])
        self['YFAS_7']=(self['YFAS7'])
        self['YFAS_8']=(self['YFAS8'])
        self['YFAS_9']=(self['YFAS9'])
        self['YFAS_10']=(self['YFAS10'])
        self['YFAS_11']=(self['YFAS11'])
        self['YFAS_12']=(self['YFAS12'])
        self['YFAS_13']=(self['YFAS13'])
        self['YFAS_14']=(self['YFAS14'])
        self['YFAS_15']=(self['YFAS15'])
        self['YFAS_16']=(self['YFAS16'])
        self['YFAS_17']=(self['YFAS17'])
        self['YFAS_18']=(self['YFAS18'])
        self['YFAS_19']=(self['YFAS19'])
        self['YFAS_20']=(self['YFAS20'])
        self['YFAS_21']=(self['YFAS21'])
        self['YFAS_22']=(self['YFAS22'])
        self['YFAS_23']=(self['YFAS23'])
        self['YFAS_24']=(self['YFAS24'])
        self['YFAS_25']=(self['YFAS25'])
        self['YFAS_26']=(self['YFAS26'])
        self['YFAS_27']=(self['YFAS27'])
        self['YFAS_28']=(self['YFAS28'])
        self['YFAS_29']=(self['YFAS29'])
        self['YFAS_30']=(self['YFAS30'])
        self['YFAS_31']=(self['YFAS31'])
        self['YFAS_32']=(self['YFAS32'])
        self['YFAS_33']=(self['YFAS33'])
        self['YFAS_34']=(self['YFAS34'])
        self['YFAS_35']=(self['YFAS35'])

        #题目分数转换
        #1)	Once a month: #9, #10, #19, #27, #33, #35
        self.loc[(self['YFAS9'])>=2,'YFAS_9']=1
        self.loc[(self['YFAS9'])<2,'YFAS_9']=0
        self.loc[(self['YFAS10'])>=2,'YFAS_10']=1
        self.loc[(self['YFAS10'])<2,'YFAS_10']=0
        self.loc[(self['YFAS19'])>=2,'YFAS_19']=1
        self.loc[(self['YFAS19'])<2,'YFAS_19']=0
        self.loc[(self['YFAS27'])>=2,'YFAS_27']=1
        self.loc[(self['YFAS27'])<2,'YFAS_27']=0
        self.loc[(self['YFAS33'])>=2,'YFAS_33']=1
        self.loc[(self['YFAS33'])<2,'YFAS_33']=0
        self.loc[(self['YFAS35'])>=2,'YFAS_35']=1
        self.loc[(self['YFAS35'])<2,'YFAS_35']=0
        #2)	Two to three times a month: #8, #18, #20, #21, #34
        self.loc[(self['YFAS8'])>=3,'YFAS_8']=1
        self.loc[(self['YFAS8'])<3,'YFAS_8']=0
        self.loc[(self['YFAS18'])>=3,'YFAS_18']=1
        self.loc[(self['YFAS18'])<3,'YFAS_18']=0
        self.loc[(self['YFAS20'])>=3,'YFAS_20']=1
        self.loc[(self['YFAS20'])<3,'YFAS_20']=0
        self.loc[(self['YFAS21'])>=3,'YFAS_21']=1
        self.loc[(self['YFAS21'])<3,'YFAS_21']=0
        self.loc[(self['YFAS34'])>=3,'YFAS_34']=1
        self.loc[(self['YFAS34'])<3,'YFAS_34']=0
        #3)	Once a week: #3, #11, #13, #14, #22, #28, #29
        self.loc[(self['YFAS3'])>=4,'YFAS_3']=1
        self.loc[(self['YFAS3'])<4,'YFAS_3']=0
        self.loc[(self['YFAS11'])>=4,'YFAS_11']=1
        self.loc[(self['YFAS11'])<4,'YFAS_11']=0
        self.loc[(self['YFAS13'])>=4,'YFAS_13']=1
        self.loc[(self['YFAS13'])<4,'YFAS_13']=0
        self.loc[(self['YFAS14'])>=4,'YFAS_14']=1
        self.loc[(self['YFAS14'])<4,'YFAS_14']=0
        self.loc[(self['YFAS22'])>=4,'YFAS_22']=1
        self.loc[(self['YFAS22'])<4,'YFAS_22']=0
        self.loc[(self['YFAS28'])>=4,'YFAS_28']=1
        self.loc[(self['YFAS28'])<4,'YFAS_28']=0
        self.loc[(self['YFAS29'])>=4,'YFAS_29']=1
        self.loc[(self['YFAS29'])<4,'YFAS_29']=0
        #4)	Two to three time's a week: #5, #12, #16, #17, #23, #24, #26, #30, #31, #32
        self.loc[(self['YFAS5'])>=5,'YFAS_5']=1
        self.loc[(self['YFAS5'])<5,'YFAS_5']=0
        self.loc[(self['YFAS12'])>=5,'YFAS_12']=1
        self.loc[(self['YFAS12'])<5,'YFAS_12']=0
        self.loc[(self['YFAS16'])>=5,'YFAS_16']=1
        self.loc[(self['YFAS16'])<5,'YFAS_16']=0
        self.loc[(self['YFAS17'])>=5,'YFAS_17']=1
        self.loc[(self['YFAS17'])<5,'YFAS_17']=0
        self.loc[(self['YFAS23'])>=5,'YFAS_23']=1
        self.loc[(self['YFAS23'])<5,'YFAS_23']=0
        self.loc[(self['YFAS24'])>=5,'YFAS_24']=1
        self.loc[(self['YFAS24'])<5,'YFAS_24']=0
        self.loc[(self['YFAS26'])>=5,'YFAS_26']=1
        self.loc[(self['YFAS26'])<5,'YFAS_26']=0
        self.loc[(self['YFAS30'])>=5,'YFAS_30']=1
        self.loc[(self['YFAS30'])<5,'YFAS_30']=0
        self.loc[(self['YFAS31'])>=5,'YFAS_31']=1
        self.loc[(self['YFAS31'])<5,'YFAS_31']=0
        self.loc[(self['YFAS32'])>=5,'YFAS_32']=1
        self.loc[(self['YFAS32'])<5,'YFAS_32']=0
        #5)	Four to six times a week: #1, #2, #4, #6, #7, #15, #25
        self.loc[(self['YFAS1'])>=6,'YFAS_1']=1
        self.loc[(self['YFAS1'])<6,'YFAS_1']=0
        self.loc[(self['YFAS2'])>=6,'YFAS_2']=1
        self.loc[(self['YFAS2'])<6,'YFAS_2']=0
        self.loc[(self['YFAS4'])>=6,'YFAS_4']=1
        self.loc[(self['YFAS4'])<6,'YFAS_4']=0
        self.loc[(self['YFAS6'])>=6,'YFAS_6']=1
        self.loc[(self['YFAS6'])<6,'YFAS_6']=0
        self.loc[(self['YFAS7'])>=6,'YFAS_7']=1
        self.loc[(self['YFAS7'])<6,'YFAS_7']=0
        self.loc[(self['YFAS15'])>=6,'YFAS_15']=1
        self.loc[(self['YFAS15'])<6,'YFAS_15']=0
        self.loc[(self['YFAS25'])>=6,'YFAS_25']=1
        self.loc[(self['YFAS25'])<6,'YFAS_25']=0
        #维度分
        self['1_longer_than_intend'] = self['YFAS_1'] + self['YFAS_2'] + self['YFAS_3']
        self['2_unsuccessful_attempts'] = self['YFAS_4'] + self['YFAS_25'] + self['YFAS_31'] + self['YFAS_32']
        self['3_much_time'] = self['YFAS_5'] + self['YFAS_6'] + self['YFAS_7']
        self['4_given_up'] = self['YFAS_8'] + self['YFAS_10'] + self['YFAS_18'] + self['YFAS_20']
        self['5_despite_adverse_consequences'] = self['YFAS_22'] + self['YFAS_23']
        self['6_tolerance'] = self['YFAS_24'] + self['YFAS_26']
        self['7_withdraw_symptoms'] = self['YFAS_11'] + self['YFAS_12']+ self['YFAS_13']+ self['YFAS_14']+ self['YFAS_15']
        self['8_despite_interpersonal_problems'] = self['YFAS_9'] + self['YFAS_21']+ self['YFAS_35']
        self['9_failure_role'] = self['YFAS_19'] + self['YFAS_27']
        self['10_failure_role'] = self['YFAS_28'] + self['YFAS_33']+ self['YFAS_34']
        self['11_craving'] = self['YFAS_29'] + self['YFAS_30']
        self['12_clinical_impairment'] = self['YFAS_16'] + self['YFAS_17']
        #维度分转换
        self['food_addiction_1']= np.where(self['1_longer_than_intend']>=1,1,0)
        self['food_addiction_2']= np.where(self['2_unsuccessful_attempts']>=1,1,0)
        self['food_addiction_3']= np.where(self['3_much_time']>=1,1,0)
        self['food_addiction_4']= np.where(self['4_given_up']>=1,1,0)
        self['food_addiction_5']= np.where(self['5_despite_adverse_consequences']>=1,1,0)
        self['food_addiction_6']= np.where(self['6_tolerance']>=1,1,0)
        self['food_addiction_7']= np.where(self['7_withdraw_symptoms']>=1,1,0)
        self['food_addiction_8']= np.where(self['8_despite_interpersonal_problems']>=1,1,0)
        self['food_addiction_9']= np.where(self['9_failure_role']>=1,1,0)
        self['food_addiction_10']= np.where(self['10_failure_role']>=1,1,0)
        self['food_addiction_11']= np.where(self['11_craving']>=1,1,0)
        self['food_addiction_12']= np.where(self['12_clinical_impairment']>=1,1,0)
        #总分计算
        self['food_addiction_score']= self['food_addiction_1']+self['food_addiction_2']+self['food_addiction_3']+self['food_addiction_4']+self['food_addiction_5']+self['food_addiction_6']+self['food_addiction_7']+self['food_addiction_8']+self['food_addiction_9']+self['food_addiction_10']+self['food_addiction_11']+self['food_addiction_12'] 
        #诊断
        self['food_addiction']=(self['food_addiction_score'])
        self.loc[self['food_addiction_score']>=2,'food_addiction']=1
        self.loc[self['food_addiction_score']<2,'food_addiction']=0
        
    def get_YFAS_whether_text(self): 
        """根据YFAS耶鲁食物成瘾量表总分诊断是否食物成瘾【这里临界值定为2，需要根据中国地区的情况更新】"""
        import numpy as np
        # 复制原始数值
        self['YFAS_1']=(self['YFAS1'])
        self['YFAS_2']=(self['YFAS2'])
        self['YFAS_3']=(self['YFAS3'])
        self['YFAS_4']=(self['YFAS4'])
        self['YFAS_5']=(self['YFAS5'])
        self['YFAS_6']=(self['YFAS6'])
        self['YFAS_7']=(self['YFAS7'])
        self['YFAS_8']=(self['YFAS8'])
        self['YFAS_9']=(self['YFAS9'])
        self['YFAS_10']=(self['YFAS10'])
        self['YFAS_11']=(self['YFAS11'])
        self['YFAS_12']=(self['YFAS12'])
        self['YFAS_13']=(self['YFAS13'])
        self['YFAS_14']=(self['YFAS14'])
        self['YFAS_15']=(self['YFAS15'])
        self['YFAS_16']=(self['YFAS16'])
        self['YFAS_17']=(self['YFAS17'])
        self['YFAS_18']=(self['YFAS18'])
        self['YFAS_19']=(self['YFAS19'])
        self['YFAS_20']=(self['YFAS20'])
        self['YFAS_21']=(self['YFAS21'])
        self['YFAS_22']=(self['YFAS22'])
        self['YFAS_23']=(self['YFAS23'])
        self['YFAS_24']=(self['YFAS24'])
        self['YFAS_25']=(self['YFAS25'])
        self['YFAS_26']=(self['YFAS26'])
        self['YFAS_27']=(self['YFAS27'])
        self['YFAS_28']=(self['YFAS28'])
        self['YFAS_29']=(self['YFAS29'])
        self['YFAS_30']=(self['YFAS30'])
        self['YFAS_31']=(self['YFAS31'])
        self['YFAS_32']=(self['YFAS32'])
        self['YFAS_33']=(self['YFAS33'])
        self['YFAS_34']=(self['YFAS34'])
        self['YFAS_35']=(self['YFAS35'])

        #题目分数转换
        #1)	Once a month: #9, #10, #19, #27, #33, #35
        self.loc[(self['YFAS9'])>=2,'YFAS_9']=1
        self.loc[(self['YFAS9'])<2,'YFAS_9']=0
        self.loc[(self['YFAS10'])>=2,'YFAS_10']=1
        self.loc[(self['YFAS10'])<2,'YFAS_10']=0
        self.loc[(self['YFAS19'])>=2,'YFAS_19']=1
        self.loc[(self['YFAS19'])<2,'YFAS_19']=0
        self.loc[(self['YFAS27'])>=2,'YFAS_27']=1
        self.loc[(self['YFAS27'])<2,'YFAS_27']=0
        self.loc[(self['YFAS33'])>=2,'YFAS_33']=1
        self.loc[(self['YFAS33'])<2,'YFAS_33']=0
        self.loc[(self['YFAS35'])>=2,'YFAS_35']=1
        self.loc[(self['YFAS35'])<2,'YFAS_35']=0
        #2)	Two to three times a month: #8, #18, #20, #21, #34
        self.loc[(self['YFAS8'])>=3,'YFAS_8']=1
        self.loc[(self['YFAS8'])<3,'YFAS_8']=0
        self.loc[(self['YFAS18'])>=3,'YFAS_18']=1
        self.loc[(self['YFAS18'])<3,'YFAS_18']=0
        self.loc[(self['YFAS20'])>=3,'YFAS_20']=1
        self.loc[(self['YFAS20'])<3,'YFAS_20']=0
        self.loc[(self['YFAS21'])>=3,'YFAS_21']=1
        self.loc[(self['YFAS21'])<3,'YFAS_21']=0
        self.loc[(self['YFAS34'])>=3,'YFAS_34']=1
        self.loc[(self['YFAS34'])<3,'YFAS_34']=0
        #3)	Once a week: #3, #11, #13, #14, #22, #28, #29
        self.loc[(self['YFAS3'])>=4,'YFAS_3']=1
        self.loc[(self['YFAS3'])<4,'YFAS_3']=0
        self.loc[(self['YFAS11'])>=4,'YFAS_11']=1
        self.loc[(self['YFAS11'])<4,'YFAS_11']=0
        self.loc[(self['YFAS13'])>=4,'YFAS_13']=1
        self.loc[(self['YFAS13'])<4,'YFAS_13']=0
        self.loc[(self['YFAS14'])>=4,'YFAS_14']=1
        self.loc[(self['YFAS14'])<4,'YFAS_14']=0
        self.loc[(self['YFAS22'])>=4,'YFAS_22']=1
        self.loc[(self['YFAS22'])<4,'YFAS_22']=0
        self.loc[(self['YFAS28'])>=4,'YFAS_28']=1
        self.loc[(self['YFAS28'])<4,'YFAS_28']=0
        self.loc[(self['YFAS29'])>=4,'YFAS_29']=1
        self.loc[(self['YFAS29'])<4,'YFAS_29']=0
        #4)	Two to three time's a week: #5, #12, #16, #17, #23, #24, #26, #30, #31, #32
        self.loc[(self['YFAS5'])>=5,'YFAS_5']=1
        self.loc[(self['YFAS5'])<5,'YFAS_5']=0
        self.loc[(self['YFAS12'])>=5,'YFAS_12']=1
        self.loc[(self['YFAS12'])<5,'YFAS_12']=0
        self.loc[(self['YFAS16'])>=5,'YFAS_16']=1
        self.loc[(self['YFAS16'])<5,'YFAS_16']=0
        self.loc[(self['YFAS17'])>=5,'YFAS_17']=1
        self.loc[(self['YFAS17'])<5,'YFAS_17']=0
        self.loc[(self['YFAS23'])>=5,'YFAS_23']=1
        self.loc[(self['YFAS23'])<5,'YFAS_23']=0
        self.loc[(self['YFAS24'])>=5,'YFAS_24']=1
        self.loc[(self['YFAS24'])<5,'YFAS_24']=0
        self.loc[(self['YFAS26'])>=5,'YFAS_26']=1
        self.loc[(self['YFAS26'])<5,'YFAS_26']=0
        self.loc[(self['YFAS30'])>=5,'YFAS_30']=1
        self.loc[(self['YFAS30'])<5,'YFAS_30']=0
        self.loc[(self['YFAS31'])>=5,'YFAS_31']=1
        self.loc[(self['YFAS31'])<5,'YFAS_31']=0
        self.loc[(self['YFAS32'])>=5,'YFAS_32']=1
        self.loc[(self['YFAS32'])<5,'YFAS_32']=0
        #5)	Four to six times a week: #1, #2, #4, #6, #7, #15, #25
        self.loc[(self['YFAS1'])>=6,'YFAS_1']=1
        self.loc[(self['YFAS1'])<6,'YFAS_1']=0
        self.loc[(self['YFAS2'])>=6,'YFAS_2']=1
        self.loc[(self['YFAS2'])<6,'YFAS_2']=0
        self.loc[(self['YFAS4'])>=6,'YFAS_4']=1
        self.loc[(self['YFAS4'])<6,'YFAS_4']=0
        self.loc[(self['YFAS6'])>=6,'YFAS_6']=1
        self.loc[(self['YFAS6'])<6,'YFAS_6']=0
        self.loc[(self['YFAS7'])>=6,'YFAS_7']=1
        self.loc[(self['YFAS7'])<6,'YFAS_7']=0
        self.loc[(self['YFAS15'])>=6,'YFAS_15']=1
        self.loc[(self['YFAS15'])<6,'YFAS_15']=0
        self.loc[(self['YFAS25'])>=6,'YFAS_25']=1
        self.loc[(self['YFAS25'])<6,'YFAS_25']=0
        #维度分
        self['1_longer_than_intend'] = self['YFAS_1'] + self['YFAS_2'] + self['YFAS_3']
        self['2_unsuccessful_attempts'] = self['YFAS_4'] + self['YFAS_25'] + self['YFAS_31'] + self['YFAS_32']
        self['3_much_time'] = self['YFAS_5'] + self['YFAS_6'] + self['YFAS_7']
        self['4_given_up'] = self['YFAS_8'] + self['YFAS_10'] + self['YFAS_18'] + self['YFAS_20']
        self['5_despite_adverse_consequences'] = self['YFAS_22'] + self['YFAS_23']
        self['6_tolerance'] = self['YFAS_24'] + self['YFAS_26']
        self['7_withdraw_symptoms'] = self['YFAS_11'] + self['YFAS_12']+ self['YFAS_13']+ self['YFAS_14']+ self['YFAS_15']
        self['8_despite_interpersonal_problems'] = self['YFAS_9'] + self['YFAS_21']+ self['YFAS_35']
        self['9_failure_role'] = self['YFAS_19'] + self['YFAS_27']
        self['10_failure_role'] = self['YFAS_28'] + self['YFAS_33']+ self['YFAS_34']
        self['11_craving'] = self['YFAS_29'] + self['YFAS_30']
        self['12_clinical_impairment'] = self['YFAS_16'] + self['YFAS_17']
        #维度分转换
        self['food_addiction_1']= np.where(self['1_longer_than_intend']>=1,1,0)
        self['food_addiction_2']= np.where(self['2_unsuccessful_attempts']>=1,1,0)
        self['food_addiction_3']= np.where(self['3_much_time']>=1,1,0)
        self['food_addiction_4']= np.where(self['4_given_up']>=1,1,0)
        self['food_addiction_5']= np.where(self['5_despite_adverse_consequences']>=1,1,0)
        self['food_addiction_6']= np.where(self['6_tolerance']>=1,1,0)
        self['food_addiction_7']= np.where(self['7_withdraw_symptoms']>=1,1,0)
        self['food_addiction_8']= np.where(self['8_despite_interpersonal_problems']>=1,1,0)
        self['food_addiction_9']= np.where(self['9_failure_role']>=1,1,0)
        self['food_addiction_10']= np.where(self['10_failure_role']>=1,1,0)
        self['food_addiction_11']= np.where(self['11_craving']>=1,1,0)
        self['food_addiction_12']= np.where(self['12_clinical_impairment']>=1,1,0)
        #总分计算
        self['food_addiction_score']= self['food_addiction_1']+self['food_addiction_2']+self['food_addiction_3']+self['food_addiction_4']+self['food_addiction_5']+self['food_addiction_6']+self['food_addiction_7']+self['food_addiction_8']+self['food_addiction_9']+self['food_addiction_10']+self['food_addiction_11']+self['food_addiction_12'] 
        #诊断
        self['food_addiction']=(self['food_addiction_score'])
        self.loc[self['food_addiction_score']>=2,'food_addiction']= 'Addiction'
        self.loc[self['food_addiction_score']<2,'food_addiction']= 'No Addiction'
        
    def get_SSI(self):
        """计算贝克自杀意念：是否有自杀意念，自杀意念分数，自杀危险"""
        import pandas as pd
        import numpy as np
        self['whether_suicide_ideation_text'] = np.where((self['SSI4']+self['SSI5'])>2,'Suicide Ideation','No Suicid Ideation')
        self['whether_suicide_ideation_numeric'] = np.where((self['SSI4']+self['SSI5'])>2,1,0)
        self['suicide_ideation'] = np.mean(self['SSI1']+self['SSI2']+self['SSI3']+self['SSI4']+self['SSI5'])
        self['suicide_risk'] = (((self['SSI6']-1)+(self['SSI7']-1)+self['SSI8']+self['SSI9']+self['SSI10']+(self['SSI11']-1)+self['SSI12']+(self['SSI13']-1)+self['SSI14']+self['SSI15']+self['SSI16']+self['SSI17']+self['SSI18']+(self['SSI19']-1)-9)/33)*100
        self.loc[(self['whether_suicide_ideation_numeric'])==0,'suicide_risk'] = np.nan
        data = pd.DataFrame(list(zip( self['whether_suicide_ideation_numeric'],self['suicide_risk'])))
        data.columns = ['whether_suicide_ideation_numeric','suicide_risk']
        return data

    ##########六、问卷实现行为学###############
    def get_CRA_quality(self):
        import numpy as np
        import pandas as pd
        self['test1'] = np.where(self.iloc[:,[12]]==2,1,0)
        self['test2'] = np.where(self.iloc[:,[13]]==3,1,0)
        self['test3'] = np.where(self.iloc[:,[14]]==4,1,0)
        self['test4'] = np.where(self.iloc[:,[15]]==4,1,0)
        self['test5'] = np.where(self.iloc[:,[16]]==3,1,0)
        self['test6'] = np.where(self.iloc[:,[17]]==2,1,0)
        self['test7'] = np.where(self.iloc[:,[18]]==2,1,0)
        self['score'] = (self['test1']+self['test2']+self['test3']+self['test4']+self['test5']+self['test6']+self['test7'])/7 * 100
        quality = (self.iloc[:,[9]]).join(self['score'])
        return quality
    
    def get_CRA_for_modeling(self):
        import numpy as np
        import pandas as pd
        CRA_parameter = pd.DataFrame({'trial':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80],
                              'prob':[0.13,0.13,0.13,0.13,0.13,0.25,0.25,0.25,0.25,0.25,0.38,0.38,0.38,0.38,0.38,0.5,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,0.75,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.13,0.13,0.13,0.13,0.13,0.25,0.25,0.25,0.25,0.25,0.38,0.38,0.38,0.38,0.38,0.5,0.5,0.5,0.5,0.5,0.75,0.75,0.75,0.75,0.75,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
                              'ambig':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.24,0.24,0.24,0.24,0.24,0.5,0.5,0.5,0.5,0.5,0.74,0.74,0.74,0.74,0.74,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.24,0.24,0.24,0.24,0.24,0.5,0.5,0.5,0.5,0.5,0.74,0.74,0.74,0.74,0.74],
                              'reward_var':[35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875,35,56,140,350,875],
                              'reward_fix':[35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35]})
        choice = (self.iloc[:,[20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99]]-1).T
        choice.index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79]
        subjID = self.iloc[:,9]
        choice.columns = subjID
        CRA = CRA_parameter.join(choice)
        CRA = pd.melt(CRA, id_vars=['trial','prob','ambig','reward_var','reward_fix'], value_vars=None, var_name='subjID', value_name='choice', col_level=None)
        return CRA
        
    
    def get_DDT_single_trial_for_modeling(self):
        import numpy as np
        import pandas as pd
        DDT_questionnaire_parameter = pd.DataFrame({'trial':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50],
                                            'delay_later':[7,7,7,7,7,7,7,7,7,7,15,15,15,15,15,15,15,15,15,15,30,30,30,30,30,30,30,30,30,30,60,60,60,60,60,60,60,60,60,60,120,120,120,120,120,120,120,120,120,120],
                                            'amount_later':[21,25,28,32,36,41,45,49,54,60,21,26,32,38,44,50,56,63,79,80,21,28,36,45,54,60,72,80,89,100,22,34,42,50,56,68,80,94,105,120,24,38,50,60,72,84,98,116,135,150],
                                            'delay_sooner':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                            'amount_sooner':[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]})
        choice = (self.iloc[:,[12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61]]-1).T
        choice.index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49]
        subjID = self.iloc[:,9]
        choice.columns = subjID
        DDT = DDT_questionnaire_parameter.join(choice)
        DDT = pd.melt(DDT, id_vars=['trial','delay_later','amount_later','delay_sooner','amount_sooner'], value_vars=None, var_name='subjID', value_name='choice', col_level=None)
        return DDT
    
#    def get_DDT_double_trial_for_modeling(self):
        #import numpy as np
        #import pandas as pd
#        DDT_questionnaire_parameter = pd.DataFrame({'trial':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100],
 #                                           'delay_later':[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120],
#                                            'amount_later':[21,21,25,25,28,28,32,32,36,36,41,41,45,45,49,49,54,54,60,60,21,21,26,26,32,32,38,38,44,44,50,50,56,56,63,63,79,79,80,80,21,21,28,28,36,36,45,45,54,54,60,60,72,72,80,80,89,89,100,100,22,22,34,34,42,42,50,50,56,56,68,68,80,80,94,94,105,105,120,120,24,24,38,38,50,50,60,60,72,72,84,84,98,98,116,116,135,135,150,150],
#                                            'delay_sooner':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#                                            'amount_sooner':[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]})
 #       choice = (self.iloc[:,([10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109]).T
#        choice.index =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99]
 #       subjID = self.iloc[:,9]
#        choice.columns = subjID
#        DDT = DDT_questionnaire_parameter.join(choice)
#        DDT = pd.melt(DDT, id_vars=['trial','delay_later','amount_later','delay_sooner','amount_sooner'], value_vars=None, var_name='subjID', value_name='choice', col_level=None)
#        return DDT
