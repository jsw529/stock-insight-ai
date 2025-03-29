
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Insight AI", layout="wide")

st.title("📊 Stock Insight AI")
ticker = st.text_input("종목 코드 입력 (예: AAPL, TSLA, 005930.KQ, 005930.KS)", value="AAPL")

def get_buy_sell_timing(df):
    timing = ""
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()

    if df['MA5'].iloc[-1] > df['MA20'].iloc[-1] and df['MA5'].iloc[-2] <= df['MA20'].iloc[-2]:
        timing = "📌 최근 골든크로스 발생 – 매수 진입 시점으로 볼 수 있습니다."
    elif df['MA5'].iloc[-1] < df['MA20'].iloc[-1] and df['MA5'].iloc[-2] >= df['MA20'].iloc[-2]:
        timing = "⚠️ 데드크로스 발생 – 매도 시점 또는 주의가 필요합니다."
    else:
        timing = "⏳ 명확한 매수/매도 신호는 없습니다. 추세를 지켜보세요."
    return timing

if st.button("분석하기") and ticker:
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="3mo")  # 더 많은 데이터를 보기 위해 3개월

        if df is None or df.empty or 'Close' not in df:
            st.error("데이터가 없습니다. 종목 코드를 다시 확인해주세요.")
        else:
            df = df.reset_index()
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

            st.subheader("📈 주가 차트 (최근 3개월)")
            fig, ax = plt.subplots()
            ax.plot(df["Date"], df["Close"], label="종가", color='blue')
            ax.set_xlabel("날짜")
            ax.set_ylabel("가격")
            ax.legend()
            st.pyplot(fig)

            # 수익률 분석
            change = (df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0] * 100
            if change > 5:
                rec = "📈 매수 추천 (상승세)"
                advice = "📌 상승 추세입니다. 장기 보유를 고려해볼 만합니다. 추가 매수는 분할로 접근하세요."
            elif change < -5:
                rec = "📉 매도 고려 (하락세)"
                advice = "📌 하락세입니다. 손절이나 일부 매도를 고려해보세요. 반등을 기다릴 수도 있습니다."
            else:
                rec = "🤔 관망 추천 (변동성 낮음)"
                advice = "📌 뚜렷한 방향성이 없어 보입니다. 추세 확인 후 대응하는 것이 좋습니다."

            st.subheader("🧠 AI 추천 결과")
            st.success(f"{rec}\n\n1개월 수익률 변화: {change:.2f}%")
            st.info(advice)

            # 매수/매도 시점 추천
            st.subheader("⏰ 매수/매도 타이밍 제안")
            timing_suggestion = get_buy_sell_timing(df)
            st.warning(timing_suggestion)

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
