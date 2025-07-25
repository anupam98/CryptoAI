import streamlit as st
import json

import sys
import os
import pysqlite3 as sqlite3

sys.modules['sqlite3'] = sqlite3
# Add the src directory to Python path
# Now your imports should work
from src.cli_server.main import main, get_user_portfolios  # Also fixed the typo














st.set_page_config(page_title="Crypto Portfolio Advisor", page_icon="📊")
st.title("📊 Crypto Portfolio Advisor")

# Initialize session state for better state management
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'current_result' not in st.session_state:
    st.session_state.current_result = None
if 'selected_portfolio_id' not in st.session_state:
    st.session_state.selected_portfolio_id = None
if 'show_history_mode' not in st.session_state:
    st.session_state.show_history_mode = False

# Input field for new portfolio
holdings_input = st.text_input(
    "Your Portfolio", 
    placeholder="e.g., BTC:1.5, ETH:10, ADA:1000",
    help="Enter your cryptocurrency holdings in the format: SYMBOL:AMOUNT"
)

# Action buttons
col1, col2, col3 = st.columns(3)
analyze = col1.button("🔍 Analyze Portfolio")
show_history = col2.button("📚 Show History")
clear_results = col3.button("🔄 Clear Results")

# Clear results
if clear_results:
    st.session_state.analysis_complete = False
    st.session_state.current_result = None
    st.session_state.show_history_mode = False
    st.session_state.selected_portfolio_id = None
    st.rerun()

# Show history flow - FIXED VERSION
if show_history:
    st.session_state.show_history_mode = True
    st.session_state.analysis_complete = False
    st.session_state.current_result = None

if st.session_state.show_history_mode:
    user_id = "1"  # replace with dynamic user context if available
    portfolios = get_user_portfolios(user_id)
    
    if not portfolios:
        st.info("No saved portfolios found.")
    else:
        st.subheader("📊 Portfolio History")
        
        # Build options map for selectbox
        options = {}
        for p in portfolios:
            try:
                holdings_data = json.loads(p.holdings)
                holdings_str = ", ".join([f"{h.get('crypto', 'N/A')}:{h.get('quantity', 0)}" for h in holdings_data])
                date_str = p.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(p, 'created_at') and p.created_at else "Unknown"
                options[p.id] = f"ID {p.id} - ${p.total_val:.2f} - {date_str}"
            except (json.JSONDecodeError, AttributeError):
                options[p.id] = f"ID {p.id} - ${p.total_val:.2f} - Invalid data"
        
        # Initialize selected portfolio if not set
        if st.session_state.selected_portfolio_id is None or st.session_state.selected_portfolio_id not in options:
            st.session_state.selected_portfolio_id = list(options.keys())[0]
        
        sel_id = st.selectbox(
            "Select a past portfolio:", 
            list(options.keys()), 
            format_func=lambda x: options[x],
            key="portfolio_selector",
            index=list(options.keys()).index(st.session_state.selected_portfolio_id) if st.session_state.selected_portfolio_id in options else 0
        )
        
        # Update session state when selection changes
        if sel_id != st.session_state.selected_portfolio_id:
            st.session_state.selected_portfolio_id = sel_id
            st.rerun()
        
        # Find selected portfolio
        try:
            sel = next(p for p in portfolios if p.id == sel_id)
        except StopIteration:
            st.error("Selected portfolio not found.")
            st.stop()
        
        # Debug information (remove in production)
        # st.write(f"Selected ID: {sel_id}")
        # st.write(f"Portfolio found: {sel.id}")
        # st.write(f"Analysis length: {len(sel.analysis) if sel.analysis else 0}")
        
        # Display portfolio details
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Portfolio Value", f"${sel.total_val:.2f}")
            try:
                holdings_data = json.loads(sel.holdings)
                st.subheader("Holdings:")
                for holding in holdings_data:
                    crypto = holding.get('crypto', 'N/A')
                    quantity = holding.get('quantity', 0)
                    value = holding.get('value', 0)
                    st.write(f"• {crypto}: {quantity} units (${value:.2f})")
            except (json.JSONDecodeError, KeyError):
                st.write("Holdings data unavailable")
        
        with col2:
            if hasattr(sel, 'created_at') and sel.created_at:
                st.write(f"**Created:** {sel.created_at.strftime('%Y-%m-%d %H:%M')}")
            else:
                st.write("**Created:** Unknown")
        
        # Display analysis results in tabs
        tab1, tab2, tab3 = st.tabs(["📈 Analysis", "💡 Recommendations", "⚠️ Risk Assessment"])
        
        with tab1:
            if sel.analysis and sel.analysis.strip():
                st.markdown(sel.analysis)
            else:
                st.info("No analysis available for this portfolio.")
        
        with tab2:
            if sel.recommendation and sel.recommendation.strip():
                st.markdown(sel.recommendation)
            else:
                st.info("No recommendations available for this portfolio.")
        
        with tab3:
            if sel.risk and sel.risk.strip():
                st.markdown(sel.risk)
            else:
                st.info("No risk assessment available for this portfolio.")
            
            # Display further reading for historical portfolios
            st.subheader("📚 Further Reading")
            if sel.further_reading and sel.further_reading.strip():
                try:
                    further_reading = json.loads(sel.further_reading)
                    if further_reading:
                        for art in further_reading:
                            title = art.get("title", "No title")
                            link = art.get("link", "#")
                            st.markdown(f"- [{title}]({link})")
                    else:
                        st.info("No articles available.")
                except json.JSONDecodeError:
                    st.warning("Unable to parse further reading data.")
            else:
                st.info("No further reading available for this portfolio.")

# Analyze new portfolio
if analyze:
    if not holdings_input.strip():
        st.warning("⚠️ Please enter your portfolio first.")
    else:
        # Reset history mode when analyzing new portfolio
        st.session_state.show_history_mode = False
        st.session_state.selected_portfolio_id = None
        
        with st.spinner("🔄 Analyzing your portfolio... This may take a few minutes."):
            try:
                result = main(holdings_input)
                
                if result:
                    st.session_state.analysis_complete = True
                    st.session_state.current_result = result
                    st.success("✅ Portfolio analysis complete!")
                else:
                    st.error("❌ Analysis failed. Please check your input and try again.")
            except Exception as e:
                st.error(f"⚠️ An error occurred during analysis: {str(e)}")
                st.info("Please check your portfolio format and try again.")

# Display current analysis results (only if not in history mode)
if st.session_state.analysis_complete and st.session_state.current_result and not st.session_state.show_history_mode:
    result = st.session_state.current_result
    
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Portfolio summary
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Total Portfolio Value", f"${result['total_value']:.2f}")
    with col2:
        if 'portfolio_id' in result:
            st.info(f"📝 Saved as Portfolio #{result['portfolio_id']}")
    
    # Holdings breakdown
    if 'holdings' in result:
        st.subheader("📋 Holdings Breakdown")
        for holding in result['holdings']:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**{holding['crypto']}**")
            with col2:
                st.write(f"{holding['quantity']} units")
            with col3:
                st.write(f"${holding['value']:.2f}")
    
    # Analysis results in tabs
    tab1, tab2, tab3 = st.tabs(["📈 Analysis", "💡 Recommendations", "⚠️ Risk Assessment"])
    
    with tab1:
        st.markdown(result['analysis'])
    
    with tab2:
        st.markdown(result['recommendation'])
    
    with tab3:
        st.markdown(result['risk'])
        
        # Fixed further reading section for new portfolios
        st.subheader("📚 Further Reading")
        further_reading = result.get("further_reading", [])
        if further_reading:
            for art in further_reading:
                title = art.get("title", "No title")
                link = art.get("link", "#")
                st.markdown(f"- [{title}]({link})")
        else:
            st.info("No articles available.")

# Sidebar with instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.write("""
    1. **Enter your portfolio** in the format: `NAME:AMOUNT`
    2. **Separate multiple holdings** with commas
    3. **Click "Analyze Portfolio"** to get AI-powered insights
    4. **View past analyses** with "Show History"
    
    **Example:**
    ```
    bitcoin:1.5, Ethereum:10, ADA:1000
    ```
    """)
    
    st.header("ℹ️ Features")
    st.write("""
    • Real-time price fetching
    • AI-powered portfolio analysis
    • Investment recommendations
    • Risk assessment
    • Portfolio history tracking
    """)
    
    st.header("⚠️ Disclaimer")
    st.write("""
    This tool provides educational insights only. 
    Always do your own research before making 
    investment decisions.
    """)
    
    # Debug section (remove in production)
    if st.checkbox("Show Debug Info"):
        st.write("**Session State:**")
        st.write(f"- show_history_mode: {st.session_state.show_history_mode}")
        st.write(f"- analysis_complete: {st.session_state.analysis_complete}")
        st.write(f"- selected_portfolio_id: {st.session_state.selected_portfolio_id}")
        st.write(f"- current_result: {st.session_state.current_result is not None}")