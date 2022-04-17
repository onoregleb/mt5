from datetime import datetime
import pytz
import MetaTrader5 as mt5
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

st.set_page_config(page_title = 'ecView', layout="wide")

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

series = pd.Series(['Investing', 'Financial Times', 'Market Beats'])
st.title('Ананлиз выбранной ценной бумаги')
st.sidebar.header('Выбор даты')
start_date = st.sidebar.date_input("Начало", value=pd.to_datetime("2022-04-01", format="%Y-%m-%d"))
end_date = st.sidebar.date_input("Конец", value=pd.to_datetime("today", format="%Y-%m-%d"))

choice = st.selectbox('Тикер', ('AAPL', 'TSLA', 'AI', 'AMD', 'FB'))


if 'AAPL' in choice:
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2022, 2, 7, tzinfo=timezone)
    utc_to = datetime(2022, 2, 21, tzinfo=timezone)
    eurusd_ticks = mt5.copy_rates_range("AAPL", mt5.TIMEFRAME_M10, utc_from, utc_to)
    mt5.shutdown()

    ticks_frame = pd.DataFrame(eurusd_ticks)
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')

    ticks_frame['MA5'] = ticks_frame.close.rolling(5).mean()
    ticks_frame['MA10'] = ticks_frame.close.rolling(10).mean()
    
    window = 14
    no_of_std = 2
    rolling_mean = ticks_frame['open'].rolling(window).mean()
    rolling_std = ticks_frame['open'].rolling(window).std()
    
    ticks_frame['RollingMean'] = rolling_mean
    ticks_frame['BollingerHigh'] = rolling_mean + (rolling_std * no_of_std)
    ticks_frame['BollingerLow'] = rolling_mean - (rolling_std * no_of_std)
   

    fig = go.Figure(data=[go.Candlestick(x=ticks_frame['time'],
                                         open=ticks_frame['open'],
                                         high=ticks_frame['high'],
                                         low=ticks_frame['low'],
                                         close=ticks_frame['close'],
                                         name='AAPL'),
                          go.Scatter(x=ticks_frame.time, y=ticks_frame.MA5, name='MA5',
                                     line=dict(color='orange', width=1)),
                          go.Scatter(x=ticks_frame.time, y=ticks_frame.MA10, name='MA10',
                                     line=dict(color='red', width=1)),
                          go.Scatter(x=ticks_frame.time, y=ticks_frame.RollingMean, name='RM',
                                     line=dict(color='green', width=1)),
                          go.Scatter(x=ticks_frame.time, y=ticks_frame.BollingerHigh, name='BH',
                                     line=dict(color='brown', width=1, dash='dash')),
                          go.Scatter(x=ticks_frame.time, y=ticks_frame.BollingerLow, name='BL',
                                     line=dict(color='blue', width=1, dash = 'dash'))])
    
    fig.layout = dict(xaxis = dict(type="category", constrain = 'domain', 
                                   showgrid = False))
    fig.update_layout(
        autosize=False,
        width=950,
        height=920)
    
    st.plotly_chart(fig)

if 'TSLA' in choice:
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2022, 1, 10, tzinfo=timezone)
    utc_to = datetime(2022, 2, 12, tzinfo=timezone)
    eurusd_ticks = mt5.copy_rates_range("TSLA", mt5.TIMEFRAME_M1, utc_from, utc_to)

    mt5.shutdown()

    ticks_frame = pd.DataFrame(eurusd_ticks)
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')

    ticks_frame['MA5'] = ticks_frame.close.rolling(5).mean()
    ticks_frame['MA20'] = ticks_frame.close.rolling(20).mean()
    fig = go.Figure(data=[go.Candlestick(x=ticks_frame['time'],
                                         open=ticks_frame['open'],
                                         high=ticks_frame['high'],
                                         low=ticks_frame['low'],
                                         close=ticks_frame['close'],
                                         name='TSLA'),
                          go.Scatter(x=ticks_frame.time, y=ticks_frame.MA5, name='MA5',
                                     line=dict(color='orange', width=1)),
                          go.Scatter(x=ticks_frame.time, y=ticks_frame.MA20, name='MA20',
                                     line=dict(color='red', width=1))])
    st.plotly_chart(fig)

