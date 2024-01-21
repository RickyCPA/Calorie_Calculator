#Running on Anaconda interpreter (base)

import streamlit as st
import pandas as pd
import numpy as np
import sympy as sym
from IPython.display import display,Math

#import MET values and correct Dtype of Code column
met_details = pd.read_excel("met_vals/2011 Compendium of Physical Activities.xlsx")
met_details.CODE = met_details.CODE.astype(str)

#Initialize Dashboard
st.title("Exercise Calorie Burn Calculator")
st.write("Computes calories burned during exercise using Mifflin Corrected MET values")

calorie_burn, calculation_detail = st.tabs(['Calorie Burn Calculator', 'Calculation Details'])

with calorie_burn:
    calc_details={} #initialize dict of calulation values

    st.header("Information Entry")
    
    #take user input of Exercise details and add to dictionary of calculation values
    st.subheader("Exercise Details")
    #Select relevant MET code column, extract value from series object by converting to an array and slicing
    calc_details['Met_Code'] = met_details[met_details['SPECIFIC ACTIVITIES']== st.selectbox("Exercise Completed",met_details['SPECIFIC ACTIVITIES'])].CODE.array[0]
    calc_details['Duration']=st.number_input('Exercise Duration (mins)',0)

    st.subheader("Personal Details")
    general, height = st.columns(2)
    with general:
        calc_details['Sex']=st.selectbox('Sex',['M','F'])
        calc_details['Age']=st.number_input('Age',0,130)
        calc_details['Weight']=st.number_input('Weight (lb)',0.0)
        #convert weight to kg for computation
        calc_details['Weight_kg'] = calc_details['Weight']*0.45359237
    with height:
        calc_details['Height_ft']=st.number_input('Height(ft)',0)
        calc_details['Height_in']=st.number_input('Height(in)',0,12)
        #combine ft and inch data entry to one hieght figure in imperial units
        calc_details['Height_imperial'] = calc_details['Height_in']/12+calc_details['Height_ft']
        #convert hight to cm for computation
        calc_details['Height_cm']=calc_details['Height_imperial']*30.48
    st.title('') #blank to create space between button and data entry
 
    
    but_col1,but_col2,but_col3 = st.columns(3) #columns to center button object

    with but_col2:
        if st.button('Compute Calories Burned','cals_burned'):
            #access standard MET value
            calc_details['Strd_Met'] = met_details[met_details['CODE']==calc_details['Met_Code']].METS.array[0]
            #compute BMR using Mifflin correction
            if calc_details['Sex'] == 'M':
                calc_details['BMR_Mifflin'] = 10*calc_details['Weight_kg'] + 6.25*calc_details['Height_cm'] - 5*calc_details['Age']+5 
            else:
                calc_details['BMR_Mifflin'] = 10*calc_details['Weight_kg'] + 6.25*calc_details['Height_cm'] - 5*calc_details['Age']-161
            #compute calorie burn per min
            calc_details['KCal_Min'] = calc_details['BMR_Mifflin']/1440
            #compute Liter per min of Oxygen utilized
            calc_details['Liter_Min'] = calc_details['KCal_Min']/5
            #convert from Liter per min of Oxygen utilized to Milliliter utilized per kg per min
            calc_details['ml_kg_min'] = calc_details['Liter_Min']/calc_details['Weight_kg']*1000
            #compute corrected MET Value
            calc_details['Corr_Met'] = calc_details['Strd_Met'] * 3.5/calc_details['ml_kg_min']
            #compute calories burned per min of this activity
            calc_details['Cals_Per_Min_Act'] = calc_details['Corr_Met']*3.5*calc_details['Weight_kg']/200
            #compute total calories burned for this activity
            calc_details['Total_Cals_Burned'] = round(calc_details['Cals_Per_Min_Act']*calc_details['Duration'],2)
            #present output
            st.subheader(str(calc_details['Total_Cals_Burned'])+" Calories")
        else:
            pass

    

with calculation_detail:
    st.header("Calorie Calculation Details")
    st.subheader("Overall Summary: ")
    st.write("The calculator uses MET values from the 'Compendium of Physical Activities' to compute calories burned per minute of activity adjusted for sex, age, height, and weight.")
    st.write("MET values are representative of the energy cost of activities measured in milliliters of oxygen burned per kilogram of weight per minute. They have been criticized for having a large margin of error when used to compute calories.")
    st.write("The solution for this large margin of error is to correct the MET value by adjusting for the 'Harris-Benedict RMR'; a measure of Resting Metabolic Rate (calories burned at rest).")

    st.subheader("MET Calculation Details: ")
    st.write("Formula to calculate 'Corrected' MET value:")
    st.latex(r'''\text{Corrected MET Value} = \text{MET Value} \times \frac{3.5ml\cdot kg^-1\cdot min^-1}{RMR (ml\cdot kg^-1\cdot min^-1)}) ''')

    st.write("The denominator above (Harris-Benedict RMR) is computed using the 'Mifflin' revision below:")
    st.latex(r'''\text{Male RMR:  } \text{RMR} = (10 \times \text{weight in kg}) + (6.25 \times \text{height in cm}) - (5 \times \text{age in years})+5 ''')
    st.latex(r'''\text{Female RMR:  } \text{RMR} = (10 \times \text{weight in kg}) + (6.25 \times \text{height in cm}) - (5 \times \text{age in years})-161 ''')

    st.subheader("Calorie Burn Computed Using MET Values:")
    st.write("Formula to compute calories burned per minute:")
    st.latex(r'''\text{Calorie Burn Per Minute: } \text{Calories} = \frac{\text{Corrected MET Value} \times 3.5 \times \text{Weight in kg}}{200}''')
    st.write("Formula to compute total calories burned during an activity:")
    st.latex(r'''\text{Total Calories Burned:  } \text{Total Calories} = \text{Calorie Burn Per Minute} \times \text{Activity Duration}''')
    
