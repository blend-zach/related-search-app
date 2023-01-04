import streamlit as st
import pandas as pd

# import numpy as np
# import os
# from sklearn import metrics
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
# import plotly.express as px
# import json

st.set_page_config(
    page_title="Chewy Related Search Opportunities",
    page_icon="✅",
    layout="wide",
)

# Load data
df = pd.read_csv('related_search_full_run.csv')
df['H1_BC1'] = df['H1 Breadcrumb Structure'].apply(lambda x: x.split("->")[0] if len(x.split("->")) > 0 else '')
df['H1_BC2'] = df['H1 Breadcrumb Structure'].apply(lambda x: x.split("->")[1] if len(x.split("->")) > 1 else '')
df['H1_BC3'] = df['H1 Breadcrumb Structure'].apply(lambda x: x.split("->")[2] if len(x.split("->")) > 2 else '')
df['H1_BC4'] = df['H1 Breadcrumb Structure'].apply(lambda x: x.split("->")[3] if len(x.split("->")) > 3 else '')
df['H1_BC5'] = df['H1 Breadcrumb Structure'].apply(lambda x: x.split("->")[4] if len(x.split("->")) > 4 else '')
df['Edited Related H1'] = df['Related H1']

# Create a list of all the columns
cols = df.columns.tolist()


# Collects user input features into dataframe
def user_input_features():
    # keyword filter
    keyword = st.sidebar.text_input(label="Keyword", placeholder="Search by Keywords...")
    # category filter
    category = []
    breadcrumb_1 = st.sidebar.selectbox(label="Breadcrumb 1",
                                        options=["Choose ..."] + sorted(df['H1_BC1'].unique().tolist()))
    if breadcrumb_1 and breadcrumb_1 != "Choose ...":
        category.append(breadcrumb_1)
        df_breadcrumb_1 = df[df['H1_BC1'] == breadcrumb_1]
        bc2_list = df_breadcrumb_1['H1_BC2'].unique().tolist()
        if '' in bc2_list:
            bc2_list.remove('')
        bc2_list = ["Choose ..."] + sorted(list(set(bc2_list)))
        if bc2_list != ['Choose ...']:
            breadcrumb_2 = st.sidebar.selectbox(label="Breadcrumb 2", options=bc2_list)
        else:
            breadcrumb_2 = st.sidebar.selectbox(disabled=True, options=bc2_list, label="Breadcrumb 2")
        if breadcrumb_2 and breadcrumb_2 != 'Choose ...':
            category.append(breadcrumb_2)
            df_breadcrumb_2 = df_breadcrumb_1[df_breadcrumb_1['H1_BC2'] == breadcrumb_2]
            bc3_list = df_breadcrumb_2['H1_BC3'].unique().tolist()
            if '' in bc3_list:
                bc3_list.remove('')
            bc3_list = ["Choose ..."] + sorted(list(set(bc3_list)))
            if bc3_list != ['Choose ...']:
                breadcrumb_3 = st.sidebar.selectbox(label="Breadcrumb 3", options=bc3_list)
            else:
                breadcrumb_3 = st.sidebar.selectbox(disabled=True, options=bc3_list, label="Breadcrumb 3")
            if breadcrumb_3 and breadcrumb_3 != 'Choose ...':
                category.append(breadcrumb_3)
                df_breadcrumb_3 = df_breadcrumb_2[df_breadcrumb_2['H1_BC3'] == breadcrumb_3]
                bc4_list = df_breadcrumb_3['H1_BC4'].unique().tolist()
                if '' in bc4_list:
                    bc4_list.remove('')
                bc4_list = ["Choose ..."] + sorted(list(set(bc4_list)))
                if bc4_list != ['Choose ...']:
                    breadcrumb_4 = st.sidebar.selectbox(label="Breadcrumb 4", options=bc4_list)
                else:
                    breadcrumb_4 = st.sidebar.selectbox(disabled=True, label="Breadcrumb 4", options=bc4_list)

                if breadcrumb_4 and breadcrumb_4 != 'Choose ...':
                    category.append(breadcrumb_4)
                    df_breadcrumb_4 = df_breadcrumb_3[df_breadcrumb_3['H1_BC4'] == breadcrumb_4]
                    bc5_list = df_breadcrumb_4['H1_BC5'].unique().tolist()
                    if '' in bc5_list:
                        bc5_list.remove('')
                    bc5_list = ["Choose ..."] + sorted(list(set(bc5_list)))
                    if bc5_list != ['Choose ...']:
                        breadcrumb_5 = st.sidebar.selectbox(label="Breadcrumb 5", options=bc5_list)
                    else:
                        breadcrumb_5 = st.sidebar.selectbox(disabled=True, options=bc5_list, label="Breadcrumb 5")
                    if breadcrumb_5 and breadcrumb_5 != 'Choose ...':
                        category.append(breadcrumb_5)
                        df_breadcrumb_5 = df_breadcrumb_4[df_breadcrumb_4['H1_BC5'] == breadcrumb_5]
                        data = df_breadcrumb_5
                    else:
                        data = df_breadcrumb_4
                else:
                    data = df_breadcrumb_3
            else:
                data = df_breadcrumb_2
        else:
            data = df_breadcrumb_1
    else:
        data = df
    h1_selection = st.sidebar.selectbox(label="Selected H1", options=["Choose..."] + data['H1'].unique().tolist())
    return keyword, category, h1_selection, data


filter_bar = user_input_features()
keyword_filter = filter_bar[0]
breadcrumb_filter = filter_bar[1]
h1_selected = filter_bar[2]
filtered_data = filter_bar[3]


def make_grid(cols, rows):
    grid = [0] * cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid


# Content of the page
if h1_selected != 'Choose...':
    st.subheader(h1_selected)
    # st.write(filtered_data[filtered_data['H1'] == h1_selected]['Related H1'].values[0])
    for i, row in filtered_data[filtered_data['H1'] == h1_selected].reset_index().iterrows():
        label = f"{i + 1} - {row['Related H1']}"
        with st.expander(label=label, expanded=False):
            url = row['Related Search URL']
            breadcrumb = [row['Related Breadcrumb Depth 1'], row['Related Breadcrumb Depth 2'],
                          row['Related Breadcrumb Depth 3'], row['Related Breadcrumb Depth 4'],
                          row['Related Breadcrumb Depth 5']]
            breadcrumb = [x for x in breadcrumb if str(x) != 'nan']
            mygrid = make_grid(2, 2)
            mygrid[0][0].write(f"- Breadcrumb: {' -> '.join(breadcrumb)}")
            mygrid[0][1].write(f"- Similarity: {row['Similarity']}")
            mygrid[1][0].write(f"- Related URL: {url}")
            mygrid[1][1].write(f"- Page Type: {row['page_type']}")
            # st.write(f"{i + 1}. {row['Related H1']}")
            edit_anchor_text = st.text_input(label="Edit Anchor Text", value='', placeholder=row['Related H1'])
            if edit_anchor_text:
                tmp_idx = df[(df['H1'] == h1_selected) & (df['Related H1'] == row['Related H1'])].index[0]
                df.loc[tmp_idx, 'Edited Related H1'] = edit_anchor_text

st.sidebar.download_button('Download Current Dataframe', df.to_csv(), 'related-search-full-run.csv')
