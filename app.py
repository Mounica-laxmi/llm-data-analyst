import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

st.title("📊 LLM Data Analyst Assistant")

# Upload file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df)

    question = st.text_input("Ask a question about your data:")

    if question:
        prompt = f"""
        You are a data analyst. Given this dataset columns: {list(df.columns)},
        convert the user question into a pandas query.

        Question: {question}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        code = response.choices[0].message.content

        st.write("### Generated Code")
        st.code(code)

        try:
            result = eval(code)
            st.write("### Result")
            st.write(result)

            # Plot if possible
            if isinstance(result, pd.Series):
                result.plot(kind='bar')
                st.pyplot(plt)

        except Exception as e:
            st.error(f"Error executing code: {e}")
