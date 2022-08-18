import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from streamlit_option_menu import option_menu
st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

logo = Image.open('data/stockcode.jpg')

st.markdown(""" <style> .font {
font-size:35px ; font-family: 'Cooper Black'; color: #000000;} 
</style> """, unsafe_allow_html=True)
st.title('나와 함께 반포 자이에 살아보지 않겠어요?')    

st.markdown('<p class="font">Hello!\n\n저희는 **반포자이까지 한걸음** 입니다.\n\n저희는 *부족한 투자 지식*으로 인한 *투자손실*을 예방하고자 최적의 **포트폴리오**를 제공하고, 내일 예상 **주가를 예측**할 수 있는 사이트입니다.\n\n많이 부족하지만 **재미로만** 봐주시기를 부탁드립니다.</p>', unsafe_allow_html=True)
st.markdown('투자하시기 전에 [유의사항](https://map-jo-stock-predict-stock-73rqcb.streamlitapp.com/#https://map-jo-stock-predict-stock-73rqcb.streamlitapp.com/Caution)을 꼭 읽어주시길 바랍니다!')
image = Image.open('data/stockcode.jpg')
st.image(image, width=800, caption= 'The Great GATSBY')