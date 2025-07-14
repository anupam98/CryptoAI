import streamlit as st
from main import main  # your CrewAI entrypoint

st.set_page_config(page_title="Crypto Portfolio Advisor", page_icon="📊")
st.title("📊 Crypto Portfolio Advisor")

holdings_input = st.text_input("Your Portfolio", placeholder="e.g., bitcoin:3, ethereum:2.5")

if st.button("Analyze Portfolio"):
    if not holdings_input.strip():
        st.warning("Please enter your portfolio first.")
    else:
        st.write("🛠️ Reached before kickoff")   # ← debug here
        with st.spinner("Analyzing your portfolio..."):
            try:
                # If your main() is async, wrap it:
                # result = asyncio.run(main(holdings_input))
                result = main(holdings_input)

                # st.write("✅ Got back result:", result)  # ← debug here

                st.success("✅ Portfolio analysis complete!")
                st.subheader("💰 Total Portfolio Value")
                st.write(f"${result['total_value']:.2f}")
                st.subheader("📈 Portfolio Analysis")
                st.markdown(result["analysis"])
                st.subheader("🔁 Recommendations ")
                st.markdown(result["recommendation"])
                st.subheader("🔁 risk recommendations ")
                st.markdown(result["risk"])
                

            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")
