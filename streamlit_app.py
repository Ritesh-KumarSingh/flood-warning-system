import os
import sys
import traceback

# Add src and its subdirectories to sys.path for robust imports on Streamlit Cloud
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Add specific subdirectories if needed
for sub in ["backend", "frontend", "ml", "utils"]:
    sub_path = os.path.join(src_path, sub)
    if sub_path not in sys.path:
        sys.path.insert(0, sub_path)

try:
    # Run the main app
    from multi_disaster_app import main
    if __name__ == "__main__":
        main()
except Exception as e:
    import streamlit as st
    st.error("🚨 Critical Application Error on Boot")
    st.exception(e)
    st.code(traceback.format_exc())

