import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime
import test

st.set_page_config(page_title="Recent Games Tracker", layout="wide")

# def updater() :
#      st.write(datetime.now())
#      st.dataframe(content)
#      time.sleep(5)
#      st.rerun()

def load_css():
    with open('frontend/static/style.css', 'r') as f:
        return f.read()

def load_js():
    with open('frontend/static/script.js', 'r') as f:
        return f.read()
    
def load_html_template():
    with open('frontend/templates/game_tracker.html', 'r') as f:
        return f.read()

css_string = f"""
<style>
 {load_css()}
</style>
"""

js_string = f"""
<script>
 {load_js()}
</script>
"""

html_content = load_html_template().replace('<!-- CSS_PLACEHOLDER -->', css_string)
html_content = html_content.replace('<!-- JS_PLACEHOLDER -->',js_string)

def st_sidebar():
     with st.sidebar:
          player_name_input = st.text_input("Enter player name")
          if player_name_input : 
               st.write("The player name is: ", player_name_input)


def html_component():
     components.html(html_content, height=1100, scrolling=True)



# st_sidebar()
# html_component()