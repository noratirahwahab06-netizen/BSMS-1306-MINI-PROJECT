import streamlit as st #important 
import pandas as pd
import matplotlib.pyplot as plt #graph
import plotly.express as px

st.image('obesity_2.jpg')

st.date_input("Select a date")

st.title("""Welcome to my Dashboard
This is my first time using streamlit.""")

#upload data
#upload_file = st.file_uploader("Please upload here:", type = 'csv')


#df = pd.read_csv(r"C:\Users\welcome\Desktop\BSMS1306\streamlit\Tips.csv")
df = pd.read_csv("obesity_level_rawdata.csv")
#df = pd.read_csv(upload_file)

#show data
st.subheader("Raw Data")
st.write(df)

#histogram
st.subheader("Histogram")
column = st.selectbox("Choose a column",df.columns)
fig, ax = plt.subplots(figsize = (10,6))
df[column].plot(kind = 'hist', ax =ax)
st.pyplot(fig)
#fig = px.histogram(df, x=column)
#fig.update_traces( marker = {"color":"purple", "line":{"color":"black","width":2}})
#st.plotly_chart(fig)

#Scatter chart
st.subheader("Scatter Chart")
x_column = st.selectbox("Choose x-axis column",df.columns)
y_column = st.selectbox("Choose y-axis column",df.columns)
fig, ax = plt.subplots(figsize = (10,6))
df.plot(kind = 'scatter', x=x_column, y=y_column, ax =ax)
st.pyplot(fig)

#fig = px.scatter(df, x=x_column, y = y_column,color ='sex' , color_discrete_sequence= ['yellow', 'red'])
#st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Data Preparation ---
# (Make sure 'df' is the name of your loaded DataFrame)

# Calculate BMI if it doesn't already exist
if 'BMI' not in df.columns and 'Weight' in df.columns and 'Height' in df.columns:
    df['BMI'] = df['Weight'] / (df['Height'] ** 2)

# Create Age Groups
if 'Age' in df.columns:
    # Define the boundaries and names for your age groups
    bins = [0, 29, 39, 49, 59, 100]
    labels = ['Under 30', '30-39', '40-49', '50-59', '60+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

    # --- 2. Interactive Bar Chart Section ---
    st.header("📊 Age Group vs. Average BMI")
    st.write("This interactive chart displays the calculated average Body Mass Index (BMI) across different age demographics.")

    # Calculate the average BMI for each age group
    df_avg_bmi = df.groupby('Age Group', as_index=False)['BMI'].mean()

    # Build the interactive bar chart using Plotly Express
    fig = px.bar(
        df_avg_bmi,
        x='Age Group',
        y='BMI',
        title='Average BMI by Age Group',
        labels={'BMI': 'Average BMI', 'Age Group': 'Age Cohort'},
        color='Age Group',             # Colors each bar differently
        text_auto='.2f',               # Displays the exact BMI value on top of each bar
        template='plotly_dark'         # Matches your dark theme dashboard
    )

    # Clean up layout appearance
    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Average BMI",
        showlegend=False               # Disables redundant legend since X-axis has labels
    )

    # Display the chart dynamically inside Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Could not find the 'Age' column in your dataset to generate age groups.")
import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Data Preparation & Classification ---
# (Assumes 'df' is your existing DataFrame)

# 1a. Ensure BMI is calculated
if 'BMI' not in df.columns and 'Weight' in df.columns and 'Height' in df.columns:
    df['BMI'] = df['Weight'] / (df['Height'] ** 2)

# 1b. Create Age Groups (if not already created)
if 'Age Group' not in df.columns and 'Age' in df.columns:
    bins = [0, 29, 39, 49, 59, 100]
    labels = ['Under 30', '30-39', '40-49', '50-59', '60+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

# 1c. Create Obesity Categories based on standard medical thresholds
if 'BMI' in df.columns and 'Age Group' in df.columns:
    bmi_bins = [0, 18.5, 24.9, 29.9, float('inf')]
    bmi_labels = ['Underweight', 'Normal weight', 'Overweight', 'Obese']
    df['Obesity Category'] = pd.cut(df['BMI'], bins=bmi_bins, labels=bmi_labels, right=True)

    # --- 2. Aggregating the Data ---
    # Group by Age Group and Obesity Category to get total counts for each stack
    df_counts = df.groupby(['Age Group', 'Obesity Category'], as_index=False).size()
    df_counts.rename(columns={'size': 'Count'}, inplace=True)

    # --- 3. Interactive Stacked Bar Chart ---
    st.header("📊 Age Group vs. Obesity Distribution")
    st.write("This interactive stacked bar chart illustrates how different weight status categories are distributed across age demographics.")

    fig = px.bar(
        df_counts,
        x='Age Group',
        y='Count',
        color='Obesity Category',
        title='Distribution of Obesity Categories by Age Group',
        labels={'Count': 'Number of People', 'Age Group': 'Age Cohort', 'Obesity Category': 'Weight Category'},
        # This forces the legend order to look professional (from Underweight up to Obese)
        category_orders={'Obesity Category': ['Underweight', 'Normal weight', 'Overweight', 'Obese']},
        template='plotly_dark',       # Matches your dark UI dashboard theme
        color_discrete_sequence=px.colors.qualitative.Pastel # Smooth, legible color palette
    )

    # Customize layout settings
    fig.update_layout(
        barmode='stack',              # Stacks the categories on top of each other
        xaxis_title="Age Group",
        yaxis_title="Number of Individuals",
        legend_title="Weight Status",
        hovermode="x unified"         # Merges hover text to see all categories at once per age group
    )

    # Render inside Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Required data columns ('Age', 'Weight', or 'Height') are missing from the dataset.")

st.header("📊 Bar Chart Analysis")

# 1. Let the user select the columns for the axes
# Grouping by a categorical column (like Gender or Smoke) works best for bar charts
x_axis_bar = st.selectbox("Choose X-axis (Categorical):", options=df.columns, index=0)
y_axis_bar = st.selectbox("Choose Y-axis (Numerical):", options=df.columns, index=1)

# 2. Let the user choose an aggregation method
aggr_func = st.selectbox("Aggregation Method:", ["Mean", "Sum", "Count"])

# 3. Process data based on selection
if aggr_func == "Mean":
    df_grouped = df.groupby(x_axis_bar)[y_axis_bar].mean().reset_index()
elif aggr_func == "Sum":
    df_grouped = df.groupby(x_axis_bar)[y_axis_bar].sum().reset_index()
else:
    df_grouped = df.groupby(x_axis_bar)[y_axis_bar].count().reset_index()
    df_grouped.rename(columns={y_axis_bar: "Count"}, inplace=True)
    y_axis_bar = "Count"

# 4. Create and display the Plotly Bar Chart
fig_bar = px.bar(
    df_grouped, 
    x=x_axis_bar, 
    y=y_axis_bar, 
    color=x_axis_bar,
    title=f"{aggr_func} of {y_axis_bar} by {x_axis_bar}"
)

st.plotly_chart(fig_bar, use_container_width=True)