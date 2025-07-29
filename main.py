
import streamlit as st
import openai
import yfinance as yf
import pandas_ta as ta

st.set_page_config(page_title="Olymp Trade GPT Analyst", layout="centered")

st.title("🤖 Olymp Trade Market Analyst")
st.write("Ask about trading strategies, indicators, and candlestick analysis for any asset.")

# User inputs
asset = st.text_input("Enter Asset Symbol (e.g., BTC-USD, EURUSD=X, AAPL)", value="BTC-USD")
timeframe = st.selectbox("Select timeframe", ["1m","2m","5m","10m","15m","30m"])
user_msg = st.text_area("💬 Your Question", value="What’s the best strategy now?")
submit = st.button("Analyze")

def get_analysis(symbol):
    df = yf.download(symbol, period="7d", interval="1h")
    df['RSI'] = ta.rsi(df['Close'])
    macd = ta.macd(df['Close'])
    df['MACD'] = macd['MACD_12_26_9']
    df['Signal'] = macd['MACDs_12_26_9']
    latest = df.iloc[-1]
    summary = f"""📈 {symbol} Summary:
    - Price: {latest['Close']:.2f}
    - RSI: {latest['RSI']:.2f}
    - MACD: {latest['MACD']:.2f}
    - Signal Line: {latest['Signal']:.2f}
    """
    return summary

def get_response(user_msg, analysis):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    prompt = f"You are a professional trading assistant. Use this analysis to suggest strategies.\n{analysis}\nUser: {user_msg}"
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5
    )
    return res['choices'][0]['message']['content'].strip()

if submit:
    try:
        analysis = get_analysis(asset)
        st.text(analysis)
        st.markdown("### 💡 Bot Recommendation")
        st.write(get_response(user_msg, analysis))
    except Exception as e:
        st.error(e)
