from IPython.display import display, HTML

def display_df(df):
    display(HTML(df.to_html()))