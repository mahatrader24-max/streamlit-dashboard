import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Paper Trading Dashboard", layout="wide")
st.title("📈 Paper Trading + Stock Screening + Learning")

TRADES_CSV = "paper_trades.csv"

# --- Load trades from CSV ---
def load_trades():
    if os.path.exists(TRADES_CSV):
        df = pd.read_csv(TRADES_CSV)
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        return df
    return pd.DataFrame(columns=["Date", "Stock", "Entry", "Qty", "SL", "Target", "Notes"])

# --- Save trades to CSV ---
def save_trades(df):
    df.to_csv(TRADES_CSV, index=False)

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
tabs = st.tabs(["🧾 Screener", "💼 Paper Trading", "📚 Learning Zone", "🗓️ Learning Plan"])

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
    trades_df = load_trades()

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
        new_trade = pd.DataFrame([{
            "Date": datetime.date.today(),
            "Stock": trade_stock,
            "Entry": entry_price,
            "Qty": qty,
            "SL": stop_loss,
            "Target": target,
            "Notes": notes
        }])
        trades_df = pd.concat([trades_df, new_trade], ignore_index=True)
        save_trades(trades_df)
        st.success("Trade added successfully!")
        st.experimental_rerun()

    if not trades_df.empty:
        for i, trade in trades_df.iterrows():
            with st.expander(f"🧾 {trade['Stock']} | {trade['Date']} | Entry: {trade['Entry']}, SL: {trade['SL']}, Target: {trade['Target']}"):
                st.write(trade.to_dict())
                delete_button = st.button(f"❌ Delete Trade #{i}")
                if delete_button:
                    trades_df = trades_df.drop(i).reset_index(drop=True)
                    save_trades(trades_df)
                    st.success(f"Deleted trade: {trade['Stock']} on {trade['Date']}")
                    st.experimental_rerun()

        st.download_button("📥 Download Trades", trades_df.to_csv(index=False), file_name="paper_trades.csv")

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

# --- TAB 4: Learning Plan ---
with tabs[3]:
    st.subheader("🗓️ Monthly Learning Plan (Aug–Dec 2025)")

    learning_plan = {
        "August": [
            "Price action basics (support, resistance, trend, VRZ)",
            "Learn TradingView tools (multi-timeframe use)",
            "Study BOL, BOF, BOS from your strategy",
            "Chart reading practice on Nifty 100"
        ],
        "September": [
            "Paper trade 5 setups (BOF/BOL)",
            "Learn risk:reward (1:2 minimum)",
            "Create your own checklist",
            "Start journaling entries in Excel sheet"
        ],
        "October": [
            "Backtest 50–100 historical setups (TradingView replay mode)",
            "Refine entry/exit logic, confirm performance stats"
        ],
        "November": [
            "Trade with small capital ₹25K–₹50K",
            "Run weekly review (P&L, mistakes, learnings)"
        ],
        "December": [
            "Finalize strategy, VRZ indicator, capital plan",
            "Set Jan 2026 trade launch goals",
            "Prepare 1-year growth tracking Excel"
        ]
    }

    for month, tasks in learning_plan.items():
        st.markdown(f"### {month}")
        for task in tasks:
            st.markdown(f"- {task}")
