import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Paper Trading Dashboard", layout="wide")
st.title("📈 Paper Trading + Stock Screening + Learning")

# --- SIDEBAR: USER INPUT ---
st.sidebar.header("🔍 Stock Screener")
stocks_input = st.sidebar.text_area("Enter Stock Symbols (comma-separated)", "TCS.NS,INFY.NS,RELIANCE.NS")
stocks = [x.strip() for x in stocks_input.upper().split(",") if x.strip()]

start_date = st.sidebar.date_input("From Date", datetime.date.today() - datetime.timedelta(days=30))
end_date = st.sidebar.date_input("To Date", datetime.date.today())

# --- MAIN: DATA FETCHING ---
@st.cache_data
def fetch_data(symbol):
    return yf.download(symbol, start=start_date, end=end_date)

# --- TABS ---
tabs = st.tabs(["🧾 Screener", "💼 Paper Trading", "📚 Learning Zone"])

# --- TAB 1: Screener ---
with tabs[0]:
    st.subheader("🧾 Stock Screener Results")
    for stock in stocks:
        df = fetch_data(stock)
        if not df.empty:
            st.markdown(f"### {stock}")
            st.line_chart(df['Close'])
            st.write(df.tail())
        else:
            st.warning(f"No data for {stock}")

# --- TAB 2: Paper Trading Journal ---
with tabs[1]:
    st.subheader("💼 Paper Trading Journal")
    if "trades" not in st.session_state:
        st.session_state.trades = []

    with st.form("paper_trade_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            trade_stock = st.selectbox("Stock", stocks)
        with col2:
            entry_price = st.number_input("Entry Price", value=0.0)
        with col3:
            qty = st.number_input("Quantity", value=0, step=1)

        col4, col5 = st.columns(2)
        with col4:
            stop_loss = st.number_input("Stop Loss", value=0.0)
        with col5:
            target = st.number_input("Target Price", value=0.0)

        notes = st.text_area("Trade Notes")
        submit = st.form_submit_button("Add Trade")

    if submit:
        trade = {
            "Date": datetime.date.today(),
            "Stock": trade_stock,
            "Entry": entry_price,
            "Qty": qty,
            "SL": stop_loss,
            "Target": target,
            "Notes": notes
        }
        st.session_state.trades.append(trade)
        st.success("Trade added successfully!")

    trade_df = pd.DataFrame(st.session_state.trades)
    if not trade_df.empty:
        st.dataframe(trade_df)
        st.download_button("📥 Download Trades", trade_df.to_csv(index=False), file_name="paper_trades.csv")

# --- TAB 3: Learning Zone ---
with tabs[2]:
    st.subheader("📚 Learning Resources")
    st.markdown("""
    - 📘 [Trading in the Zone - Mark Douglas](https://www.amazon.in/Trading-Zone-Mark-Douglas/dp/0735201447)
    - 📘 [Technical Analysis Explained - Martin Pring](https://www.amazon.in/Technical-Analysis-Explained-Martin-Pring/dp/0071825177)
    - 🎥 [TradingRush (YouTube)](https://www.youtube.com/c/TradingRush)
    - 🎥 [The Financial Analyst (YouTube)](https://www.youtube.com/@thefinancialanalyst)
    - 📊 [Chartink Screener](https://chartink.com/screener/)
    """)
