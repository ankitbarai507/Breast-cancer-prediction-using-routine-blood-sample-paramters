from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
from wtforms.validators import NumberRange

import numpy as np  
from tensorflow.keras.models import load_model
import joblib


def return_prediction(model,sample_json):
    
    # For larger data features, you should probably write a for loop
    # That builds out this array for you
    
    f1 = sample_json['Age']
    f2 = sample_json['BMI']
    f3 = sample_json['Glucose']
    f4 = sample_json['Insulin']
    f5 = sample_json['HOMA']
    f6 = sample_json['Leptin']
    f7 = sample_json['Adiponectin']
    f8 = sample_json['Resistin']
    f9 = sample_json['MCP_1']
    
    
    flower = [[f1,f2,f3,f4,f5,f6,f7,f8,f9]]
    
    classes = np.array(['Benign', 'Malignant'])

    class_ind = model.predict(df1[features].iloc[0].values.reshape(1,-1))[0]
    
    return classes[class_ind][0]



app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'someRandomKey'


# REMEMBER TO LOAD THE MODEL 
rf_model = joblib.load("rf.pkl")

# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
class breast_cancer_Form(FlaskForm):
    Age = TextField('Age')
    BMI = TextField('BMI')
    Glucose = TextField('Glucose')
    Insulin = TextField('Insulin')
    HOMA = TextField('HOMA')
    Leptin = TextField('Leptin')
    Adiponectin = TextField('Adiponectin')
    Resistin = TextField('Resistin')
    MCP_1 = TextField('MCP.1')

    submit = SubmitField('Get Prediction')



@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = breast_cancer_Form()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.

        session['Age'] = form.Age.data
        session['BMI'] = form.BMI.data
        session['Glucose'] = form.Glucose.data
        session['Insulin'] = form.Insulin.data
        session['HOMA'] = form.HOMA.data
        session['Leptin'] = form.Leptin.data
        session['Adiponectin'] = form.Adiponectin.data
        session['Resistin'] = form.Resistin.data
        session['MCP_1'] = form.MCP_1.data

        return redirect(url_for("prediction"))


    return render_template('home.html', form=form)


@app.route('/prediction')
def prediction():

    content = {}

    content['Age'] = float(session['Age'])
    content['BMI'] = float(session['BMI'])
    content['Glucose'] = float(session['Glucose'])
    content['Insulin'] = float(session['Insulin'])
    content['HOMA'] = float(session['HOMA'])
    content['Leptin'] = float(session['Leptin'])
    content['Adiponectin'] = float(session['Adiponectin'])
    content['Resistin'] = float(session['Resistin'])
    content['MCP_1'] = float(session['MCP_1'])

    results = return_prediction(model=rf_model,sample_json=content)

    return render_template('prediction.html',results=results)


if __name__ == '__main__':
    app.run(debug=True)
