import pandas as pd

def load_data(uploaded_file):
    """
    Loads CSV or XLSX file securely.
    """
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file format")
