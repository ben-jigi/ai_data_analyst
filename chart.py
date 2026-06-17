import streamlit as st


def charts(chart,result):

    if chart=="BAR":
        st.bar_chart(
            result.set_index(result.columns[0])        )
        
    else:
        st.line_chart(
            result.set_index(result.columns[0]) 

        )
        