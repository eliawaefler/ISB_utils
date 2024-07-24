import streamlit as st
import subprocess
import os

# Function to get all python scripts from the utils directory
def get_scripts(repo_path='utils'):
    scripts = [f for f in os.listdir(repo_path) if f.endswith('.py')]
    return scripts

# Function to run the selected script
def run_script(script, args):
    command = f"python {os.path.join('utils', script)} {args}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

# Streamlit UI
st.title('Utils Scripts Runner')

scripts = get_scripts()

selected_script = st.selectbox('Select a script to run', scripts)

args = st.text_input('Enter arguments for the script (optional)')

if st.button('Run'):
    with st.spinner('Running the script...'):
        stdout, stderr = run_script(selected_script, args)
        if stdout:
            st.subheader('Output:')
            st.text(stdout)
        if stderr:
            st.subheader('Error:')
            st.text(stderr)
