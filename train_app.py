import streamlit as st
import yfinance as yf
import base64
import plotly.express as px
import pandas as pd
from PIL import Image

#st.set_page_config(layout="wide")

#write Title
st.title("Stock Market Scraper Data")

#load and display image
image = Image.open("logo2.jpg")
st.image(image,use_column_width=True)

# expnader bar about data
expander_bar = st.expander("About Data")
expander_bar.markdown("""
* **Python libraries:** Streamlit, yfinance, base64, plotly, pandas, PIL
* **Data companies source detailes:** [500 companies]('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').
""")

# expnader bar about Web App
expander_bar = st.expander("About Web App")
expander_bar.markdown("""
* **1):** you can groupby companies by sector and find the company which you want to know about its price and trend
* **2)** after selected you can select symbol of company and scape data with multi period times and download it as csv file.
* **3)** even you can show plot by click on buttom                      
""")

#header of sidebar
st.sidebar.header("User Input Features")

#web scrapping
@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

#load data
df = load_data()

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, "Energy")

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ].reset_index(drop=True)

st.write("***")

# section one to diplay companies
st.header("Display Componies")
st.write(f"##### Data Shape is : {df_selected_sector.shape[0]} Rows and {df_selected_sector.shape[1]} Columns")
st.dataframe(df_selected_sector)

#helper function to encode and decode data to download it
def download(df,name,index=False):
    csv = df.to_csv(index=index)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{name}.csv">Download CSV File</a>'
    return href

#define a markdown to download companies data
st.markdown(download(df_selected_sector,name="Stockmarket"),unsafe_allow_html=True)
st.write("***")

# user input features
period = st.sidebar.selectbox("Period",["1mo","3mo","6mo","9mo","1y","2y"])
interval = st.sidebar.select_slider("Interval",["1h","1d","1wk","1mo","3mo"])
ticker = st.sidebar.selectbox("Tickers",df.Symbol.unique())

# load data from yfinance
data = yf.download(
        tickers = ticker,
        period = period,
        interval = interval,
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# section two display of data for selected symbol
st.header(f"Data about market of {ticker}")
st.write(f"##### Data Shape is : {data.shape[0]} Rows and {data.shape[1]} Columns")
st.dataframe(data.round(2))

# to donwnload data
st.markdown(download(data.round(2),name=ticker,index=True),unsafe_allow_html=True)

st.write("***")

#section3 to show plots
st.header("Plots of Symbol")

#define a helper funtion to plots charts of Volume and Close Price
def plot_charts(data,ticker,x,y):

    fig = px.line(data_frame=data,x=x,y=y,template="plotly_dark")
    fig.update_layout(
        title = dict(text=ticker,font_color="lightgreen",font_size=25,font_family="Serif"),
        xaxis = dict(titlefont_color="orange",titlefont_size=22,titlefont_family="Serif"),
        yaxis = dict(titlefont_color="orange",titlefont_size=22,titlefont_family="Serif")
    )
    return fig

if st.button('Show Plots'):
    fig = plot_charts(data,ticker,x=data.index,y=data.Close)
    st.plotly_chart(fig)
    fig = plot_charts(data,ticker,x=data.index,y=data.Volume)
    st.plotly_chart(fig)

st.write("***")

st.write("""
### Trained and Developed by [Mahdi Zare](https://www.linkedin.com/in/mahdizare22/)
""")