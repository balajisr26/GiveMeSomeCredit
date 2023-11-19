import streamlit as st
import numpy as np

st.title('Credit Dashboard - LR')
st.subheader('Loan Approval')
st.write('This App Scores each Application and Suggest Course of Action as Approval, Manual, or Reject')

row1,row2,row3 = st.columns(3)

with row1:
    numberoftimes_30 = st.number_input('Number of Times 30+',min_value=0)
    numberoftimes_60 = st.number_input('Number of Times 60+',min_value=0)
    numberoftimes_90 = st.number_input('Number of Times 90+',min_value=0)
    
with row2:
    age = st.number_input('Age of the Customer',min_value=18,max_value=100)
    income = st.number_input('Monthly Income',min_value=-1,step=501)
    
with row3:
    utilization = st.number_input('Utilization',min_value=0.00,max_value=1.00,step=0.1,format="%.2f")
    debtratio = st.number_input('Debt Ratio',min_value=0.00,max_value=1.00,step=0.05)

inputs = [age,utilization,numberoftimes_30,numberoftimes_60,numberoftimes_90,debtratio,income]
#st.write(f"""User Inputs are {inputs}""".format())

age_points = np.where(age <36,5.34
                             ,np.where(age <43,6.92
                                      ,np.where(age <49,7.79
                                               ,np.where(age <55,8.33
                                                        ,np.where(age <62,11.03
                                                                 ,np.where(age < 67,13.4
                                                                          ,np.where(age >=67,16.64,5.34)))))))
debtratio_points = np.where(debtratio <0.35,11.59
                                   ,np.where(debtratio >=0.35,7.25,7.25))

numberoftime3059dayspastduenotworse_points = np.where(numberoftimes_30 ==0,13.32
                                                             ,np.where(numberoftimes_30 == 1,2.33
                                                                      ,np.where(numberoftimes_30 >1 ,-5.26,-5.26)))

numberoftime6089dayspastduenotworse_points = np.where(numberoftimes_60 ==0,10.89,-3.00)

numberoftimes90dayslate_points = np.where(numberoftimes_90 ==0 ,12.36,-9.26)

revolvingutilizationofunsecuredlines_points = np.where(utilization <0.04,21.47
                                                              ,np.where(utilization <0.22,18.73
                                                                       ,np.where(utilization <0.68,9.88
                                                                                ,np.where(utilization >=0.68,-1.78,-1.78))))

Monthly_Income_Points = np.where(income == -1,10.32
                                         ,np.where(income <=5330,7.5
                                                        ,np.where(income  > 5330,10.71,7.5)))

score = age_points + debtratio_points + numberoftime3059dayspastduenotworse_points + numberoftime6089dayspastduenotworse_points +\
			 numberoftimes90dayslate_points + revolvingutilizationofunsecuredlines_points + Monthly_Income_Points 

app_status = np.where(score <50,'Reject'
		,np.where(score < 60 , 'Manual Underwriting'
			,np.where(score >=60,'Approve','Reject')))

col4,col5 =st.columns(2)

with col4:
	st.write(f"""Score is {np.round(score,2)}""".format())
with col5:
	st.write(f"""Application Status is {app_status }""".format())

