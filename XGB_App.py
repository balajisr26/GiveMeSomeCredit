import streamlit as st
import numpy as np
import pandas as pd
import xgboost as xgb
import pickle
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit.components.v1 as components


st.title('Credit Dashboard - XGBoost')
st.subheader('Loan Approval')
st.write('This App Scores each Application and Suggest Course of Action as Approval, Manual, or Reject')

row1_col1,row1_col2,row1_col3,row1_col4,row1_col5 = st.columns(5)
row2_col1,row2_col2,row2_col3,row2_col4 = st.columns(4)


with row1_col1:
    numberoftimes_30 = st.number_input('Number of Times 30+',min_value=0)
with row1_col2:
    numberoftimes_60 = st.number_input('Number of Times 60+',min_value=0)
with row1_col3:
    numberoftimes_90 = st.number_input('Number of Times 90+',min_value=0)
with row1_col4:
    age = st.number_input('Age of the Customer',min_value=18,max_value=100)
with row1_col5:
    income = st.number_input('Monthly Income',min_value=-1,step=501)
     
with row2_col1:
    utilization = st.number_input('Utilization',min_value=0.00,max_value=1.00,step=0.1,format="%.2f")
with row2_col2:
    debtratio = st.number_input('Debt Ratio',min_value=0.00,max_value=1.00,step=0.05)
    
inputs = [age,utilization,numberoftimes_30,numberoftimes_60,numberoftimes_90,debtratio,income]
#st.write(f"""User Inputs are {inputs}""".format())

bins=[-99999,36,43,49,55,62,67,999999999]
labels=['0-36','36-43','43-49','49-55','55-62','62-67','More than 67']
AGE_BIN = pd.cut([age],bins,labels=labels,right=False)

bins=[-99999,0.04,0.22,0.68,999999999]
labels=['0-0.04','0.04-0.22','0.22-0.68','More than 0.68']
REVOLVING_UTILIZATION_BIN = pd.cut([utilization],bins,labels=labels,right=False)

bins=[-99999,1,2,999999999]
labels=['0','1','More than 1']
NO_TIMES_30PASTDUE_BIN = pd.cut([numberoftimes_30],bins,labels=labels,right=False)

bins=[-99999,0.35,999999999]
labels=['0-0.35','More than 0.35']
DebtRatio_BIN = pd.cut([debtratio],bins,labels=labels,right=False)

bins=[-99999,5330,999999999]
labels=['0-5330','More than 5330']
MonthlyIncome_BIN = pd.cut([income],bins,labels=labels,right=False)

bins=[-99999,1,999999999]
labels=['0','More than 0']
NumberOfTimes90DaysLate_BIN = pd.cut([numberoftimes_90],bins,labels=labels,right=False)

bins=[-99999,1,999999999]
labels=['0','More than 0']
NumberOfTime6089DaysPastDueNotWorse_BIN = pd.cut([numberoftimes_60],bins,labels=labels,right=False)

final_df = pd.DataFrame([[AGE_BIN,REVOLVING_UTILIZATION_BIN,NO_TIMES_30PASTDUE_BIN,DebtRatio_BIN,MonthlyIncome_BIN,NumberOfTimes90DaysLate_BIN
		,NumberOfTime6089DaysPastDueNotWorse_BIN]])
final_df.columns=['AGE_BIN','REVOLVING_UTILIZATION_BIN','NO_TIMES_30PASTDUE_BIN','DebtRatio_BIN','MonthlyIncome_BIN','NumberOfTimes90DaysLate_BIN'
		,'NumberOfTime6089DaysPastDueNotWorse_BIN']
features = final_df.columns


clf_pickle = open('xgbmodel','rb')
clf = pickle.load(clf_pickle)
clf_pickle.close()

dict_pickle = open('lblencode_dict','rb')
full_dict_pickle = pickle.load(dict_pickle)
dict_pickle.close()

#st.write([full_dict_pickle])

#st.write([final_df[['AGE_BIN']]])

if AGE_BIN=='0-36':
    AGE_LBL =0
elif AGE_BIN=='36-43':
    AGE_LBL=1
elif AGE_BIN=='43-49':
    AGE_LBL=2
elif AGE_BIN=='49-55':
    AGE_LBL=3
elif AGE_BIN=='55-62':
    AGE_LBL=4
elif AGE_BIN=='62-67':
    AGE_LBL=5
else:
    AGE_LBL=6

if REVOLVING_UTILIZATION_BIN=='0-0.04':
	REVOLVING_UTILIZATION_BIN=0
elif REVOLVING_UTILIZATION_BIN=='0.04-0.22':
	REVOLVING_UTILIZATION_BIN=1
elif REVOLVING_UTILIZATION_BIN=='0.22-0.68':
	REVOLVING_UTILIZATION_BIN=2
elif REVOLVING_UTILIZATION_BIN=='More than 0.68':
	REVOLVING_UTILIZATION_BIN=3
else:
	REVOLVING_UTILIZATION_BIN=4

if NO_TIMES_30PASTDUE_BIN=='0':
	NO_TIMES_30PASTDUE_BIN=0
elif NO_TIMES_30PASTDUE_BIN=='1':
	NO_TIMES_30PASTDUE_BIN=1
else:
	NO_TIMES_30PASTDUE_BIN=2	

if NumberOfTime6089DaysPastDueNotWorse_BIN=='0':
	NumberOfTime6089DaysPastDueNotWorse_BIN=0
else:
	NumberOfTime6089DaysPastDueNotWorse_BIN=1

if NumberOfTimes90DaysLate_BIN=='0':
	NumberOfTimes90DaysLate_BIN=0
else:
	NumberOfTimes90DaysLate_BIN=1

if DebtRatio_BIN=='0-0.35':
	DebtRatio_BIN=0
else:
	DebtRatio_BIN=1

if MonthlyIncome_BIN=='0-5330':
	MonthlyIncome_BIN=0
elif MonthlyIncome_BIN=='MISSING':
	MonthlyIncome_BIN=1
else:
	MonthlyIncome_BIN=2
  

prediction = clf.predict_proba([[AGE_LBL,REVOLVING_UTILIZATION_BIN,NO_TIMES_30PASTDUE_BIN,DebtRatio_BIN
				,MonthlyIncome_BIN,NumberOfTimes90DaysLate_BIN,NumberOfTime6089DaysPastDueNotWorse_BIN]])[:,1]


#app_status = np.where(score <50,'Reject'
#		,np.where(score < 60 , 'Manual Underwriting'
#			,np.where(score >=60,'Approve','Reject')))


input_shap = pd.DataFrame({'AGE_LBL':[AGE_LBL],'REVOLVING_UTILIZATION_BIN':[REVOLVING_UTILIZATION_BIN]
                            ,'NO_TIMES_30PASTDUE_BIN':[NO_TIMES_30PASTDUE_BIN],'DebtRatio_BIN':[DebtRatio_BIN]
                            ,'MonthlyIncome_BIN':[MonthlyIncome_BIN],'NumberOfTimes90DaysLate_BIN':[NumberOfTimes90DaysLate_BIN]
                            ,'NumberOfTime6089DaysPastDueNotWorse_BIN':[NumberOfTime6089DaysPastDueNotWorse_BIN]})


shap_tree = shap.TreeExplainer(clf)
shap_val = shap_tree(input_shap)

#st_shap(shap.plots.waterfall(shap_val[0]))

shap_df = pd.DataFrame(shap_val.values,columns=input_shap.columns)
shap_df['base_values'] = shap_val.base_values

final_df = pd.DataFrame(columns=['Variable','LogOdds'])
for c in shap_df.columns:
    temp = pd.DataFrame.from_dict({"Variable":c,"LogOdds":shap_df[c]})
    final_df = pd.concat([final_df,temp],ignore_index=True)
final_df.sort_values(by='LogOdds',inplace=True)
#st.write(final_df)

#fig = plt.figure(figsize=(8,4))
#plt.clf()

app_status = np.where(prediction >= 0.585,'Reject',np.where(prediction >=0.429,'Manual Review','Approve'))

with row2_col3:
    st.write(f"""Score is {np.round(prediction,2)}""".format())

with row2_col4:
    st.write(f"""Application Status is {app_status }""".format())

#row3_col1 = st.columns(1)

#with row3_col1:
 #   st.write('Hi')
fig=px.bar(data_frame=final_df,x='Variable',y='LogOdds',title='Model Interpretation')
st.plotly_chart(fig)




