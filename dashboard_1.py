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

import streamlit as tf
import pandas as pd
import plotly.express as px

# ... (Your existing code to load your dataset 'df') ...

st.title("Welcome to my Dashboard")
st.write("This is my first time using streamlit.")

# --- RAW DATA SECTION ---
st.subheader("Raw Data")
st.dataframe(df.head()) # Keeps your data table neat

# --- INTERACTIVE HISTOGRAM SECTION ---
st.header("📊 Histogram Analysis")

# Your existing dropdown selector
hist_col = st.selectbox("Choose a column for the histogram:", options=["Age", "Height", "Weight", "CH2O"])

# Create the interactive Plotly histogram
fig_hist = px.histogram(
    df, 
    x=hist_col, 
    color="Gender",          # Automatically splits data by gender using different colors!
    marginal="box",          # Adds a mini box-plot right on top of the histogram
    hover_data=df.columns,   # Shows all data details when hovering over a bar
    template="plotly_dark"   # Matches Streamlit's dark theme perfectly
)

# Render the Plotly chart in Streamlit
st.plotly_chart(fig_hist, use_container_width=True)


# --- INTERACTIVE SCATTER CHART SECTION ---
st.header("🎯 Scatter Chart Analysis")

# Your existing X and Y axis dropdown selectors
col1, col2 = st.columns(2)
with col1:
    x_axis = st.selectbox("Choose x-axis column:", options=["Age", "Height", "Weight", "CH2O"], index=1) # Default to Height
with col2:
    y_axis = st.selectbox("Choose y-axis column:", options=["Age", "Height", "Weight", "CH2O"], index=2) # Default to Weight

# Create the interactive Plotly scatter plot
fig_scatter = px.scatter(
    df, 
    x=x_axis, 
    y=y_axis, 
    color="SMOKE",           # Colors dots based on smoking status (adds a whole new layer of insight!)
    size="Age",              # Larger dots mean older individuals
    hover_name="Gender",     # Puts Gender right at the top of the hover card
    trendline="ols",      # Optional: uncomment if you install statsmodels to see a trendline
    template="plotly_dark"
)

# Render the Plotly chart in Streamlit
st.plotly_chart(fig_scatter, use_container_width=True)

import streamlit as st
import plotly.express as px

# Assuming 'df' is your loaded DataFrame
# df = pd.read_csv("your_data.csv") 

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