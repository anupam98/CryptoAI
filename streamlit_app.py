import streamlit as st
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

# Import and run the main app
from crypto_project.app import *

# This file serves as the entry point for Streamlit Cloud deployment 