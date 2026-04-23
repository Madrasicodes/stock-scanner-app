import streamlit as st
from scanner import scan_market

st.title("AI Stock Scanner")

capital = st.number_input("Enter Capital", value=100000)
risk_percent = st.slider("Risk %", 1, 10, 5)
trade_type = st.selectbox("Trade Type", ["Intraday", "Swing"])

if st.button("Scan Market"):
    results = scan_market(trade_type)

    for r in results:
        risk_amount = capital * (risk_percent / 100)
        stop_loss = r['price'] * 0.98
        target = r['price'] * 1.04

        position_size = int(risk_amount / (r['price'] - stop_loss))

        st.write(r['stock'], r['signal'], r['price'], position_size)
