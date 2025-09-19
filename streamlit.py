import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

# Function to extract text from PDF
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except:
        return ""

# Function to extract data from Excel
def extract_data_from_excel(file):
    try:
        xls = pd.ExcelFile(file)
        data = {}
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            data[sheet_name] = df
        return data
    except:
        return {}

# Streamlit UI
st.title("Financial Document Q&A Assistant")

uploaded_file = st.file_uploader("Upload PDF or Excel", type=["pdf","xlsx"])

if uploaded_file:
    text_data = ""
    excel_data = {}

    if uploaded_file.name.endswith(".pdf"):
        text_data = extract_text_from_pdf(uploaded_file)
        st.success("PDF extracted successfully!")
        st.text_area("PDF Content Preview", text_data[:500], height=200)
    
    elif uploaded_file.name.endswith(".xlsx"):
        excel_data = extract_data_from_excel(uploaded_file)
        st.success("Excel extracted successfully!")
        for sheet, df in excel_data.items():
            st.write(f"Sheet: {sheet}")
            st.dataframe(df.head())

    # Question input
    question = st.text_input("Ask a question about Revenue, Profit, or Expenses")

    if question:
        q = question.lower()
        if "revenue" in q:
            if text_data:
                lines = [l for l in text_data.split("\n") if "revenue" in l.lower()]
                st.write("Revenue info from PDF:", lines[:5] if lines else "No revenue info found")
            elif excel_data:
                for sheet, df in excel_data.items():
                    rows = df[df.apply(lambda row: row.astype(str).str.contains('revenue', case=False).any(), axis=1)]
                    if not rows.empty:
                        st.write(f"Revenue info from sheet: {sheet}")
                        st.dataframe(rows)
        elif "profit" in q:
            if text_data:
                lines = [l for l in text_data.split("\n") if "profit" in l.lower()]
                st.write("Profit info from PDF:", lines[:5] if lines else "No profit info found")
            elif excel_data:
                for sheet, df in excel_data.items():
                    rows = df[df.apply(lambda row: row.astype(str).str.contains('profit', case=False).any(), axis=1)]
                    if not rows.empty:
                        st.write(f"Profit info from sheet: {sheet}")
                        st.dataframe(rows)
        elif "expense" in q:
            if text_data:
                lines = [l for l in text_data.split("\n") if "expense" in l.lower()]
                st.write("Expenses info from PDF:", lines[:5] if lines else "No expense info found")
            elif excel_data:
                for sheet, df in excel_data.items():
                    rows = df[df.apply(lambda row: row.astype(str).str.contains('expense', case=False).any(), axis=1)]
                    if not rows.empty:
                        st.write(f"Expenses info from sheet: {sheet}")
                        st.dataframe(rows)
        else:
            st.write("Sorry, I can only answer questions about Revenue, Profit, or Expenses.")
