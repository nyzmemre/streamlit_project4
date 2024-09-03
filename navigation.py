import streamlit as st

pages = st.navigation({
    "Project": [
        st.Page("pages/Charts.py", title="Charts"),
        st.Page("pages/Results.py", title="Results"),
        st.Page("pages/About_Us.py", title="About Us"),
    ],
 #   "Modeling": [
 #       st.Page("pages/evaluation.py", title="Evaluation", icon="🔍"),
 #       st.Page("pages/predict.py", title="Prediction", icon="🤖")
 #   ],
})

pages.run()