# Dash_App.py
### Import Packages ########################################
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import pickle

### Setup ###################################################
app = dash.Dash(__name__)
app.title = 'Machine Learning Model Deployment'
server = app.server
### load ML model & Respective files ###########################################
with open('rf_model.pkl', 'rb') as f:
    clf = pickle.load(f)






person_home_ownership_items = ['RENT', 'MORTGAGE', 'OWN', 'OTHER']
grade_items = [
    # TASK please fill the grade items with all the possible based on our data
]

app.layout = html.Div([
    dbc.Row([html.H2(children='Predict Loan Status')]),


# person_income
    dbc.Row([
        dbc.Col(html.Label(children='person_income'), width={"order": "first"}),
        dbc.Col(dcc.Input(type="text", placeholder="", id='person_income'))
    ]),

# loan_percent_income
    dbc.Row([
        dbc.Col(html.Label(children='loan_percent_income'), width={"order": "first"}),
        dbc.Col(dcc.Input(type="text", placeholder="", id='loan_percent_income'))
    ]),


# TASK : please create a drop down code loan_int_rate,  Please refer to the Above


#=======================

# person_home_ownership
html.Br(),
    dbc.Row([
        dbc.Col(html.Label(children='person_home_ownership'), width={"order": "first"}),
        dbc.Col(dcc.Dropdown(person_home_ownership_items, person_home_ownership_items[0], id='person_home_ownership'))
    ]),

# TASK : please create a drop down code 'loan_grade', Please refer to the Above


#=======================


html.Br(),
html.Br(),
    dbc.Row([dbc.Button('Submit', id='submit-val', n_clicks=0, color="primary")]),
    html.Br(),
    dbc.Row([html.Div(id='prediction output')])

    ], style = {'padding': '0px 0px 0px 150px', 'width': '50%'})


### Callback to produce the prediction ######################### 
@app.callback(
    Output('prediction output', 'children'),
    Input('submit-val', 'n_clicks'),
    # TASK: please define the state for each input you want to capture
    State('person_income', 'value'), # it is an example and please replicate for other columns
#       --
#       --
#       --
#       --
)
   
def update_output(n_clicks, person_income, loan_percent_income, loan_int_rate, loan_grade,  person_home_ownership, ):

    df = pd.DataFrame({'loan_percent_income': loan_percent_income,
                     'loan_grade': loan_grade,
                     'person_income': person_income,
                     'person_home_ownership': person_home_ownership,
                     'loan_int_rate': loan_int_rate,
                     }, index=[0])

    df = df.replace(to_replace={'person_home_ownership': {'RENT': 0,
                                                     'MORTGAGE': 1,
                                                     'OWN': 2,
                                                     'OTHER': 3},
                           'loan_grade': {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}})

    df['loan_grade'].fillna(3, inplace=True)
    df['person_home_ownership'].fillna(3, inplace=True)
    df['loan_int_rate'].fillna(11.07, inplace=True)
    df.fillna(0, inplace=True)
    print(df)



    prediction = clf.predict(df)[0]
    if prediction == 0:
        output = "Loan Status is '0'"
    else:
        output = "Loan Status is '1'"

    return f'The model predicted {output}.'



### Run the App ###############################################
if __name__ == '__main__':
    app.run_server(debug=True)