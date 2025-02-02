import streamlit as st


st.set_page_config(
    page_title="Security, Networking, & Engineering Kit (SNEK)",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Security, Networking, & Engineering Kit (SNEK)")
st.write("""

## Objective of Project

SNEK (Software, Networking, & Engineering Kit) is a curated suite of 
cybersecurity, Python utilities, and database tools designed to 
streamline daily development tasks, enhance security, and simplify 
workflow management. This README covers setup, usage, and best 
practices for getting the most out of SNEK’s integrated toolset.
""")
st.sidebar.info("Select one of the tools to use.")

# add a divider 
st.divider()

footer="""<style>
.footer {
display: block;
padding: 10px;
padding-top: 20px;
border-top: 1px solid #333;
position: fixed;
left: 0;
bottom: 0;
width: 100%;
text-align: center;
font-weight: bold;
}

.footer a {
    color: white;
    text-decoration: none;
}
</style>
<div class="footer">
<p>
    &copy; 2025 - A project by <a style='text-align: center;' href="https://www.github.com/davydany" target="_blank">David Daniel (davydany)</a>
    <br/>
    
</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)