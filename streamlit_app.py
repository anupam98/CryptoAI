import streamlit as st
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
from crypto_project.app import *

# This file serves as the entry point for Streamlit Cloud deployment 