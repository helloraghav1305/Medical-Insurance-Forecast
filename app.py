from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn

app = Flask(__name__)
model = pickle.load(open('insurance_rf.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    northwest=0
    southeast=0
    southwest=0
    if request.method == 'POST':
        Age = int(request.form['age'])
        Gender=request.form['gender']
        BMI=float(request.form['bmi'])
        Children=int(request.form['children'])
        Smoker=request.form['smoker']
        Region=request.form['region']
        if(Gender=='male'):
            Gender=1
        else:
            Gender=0
        if(Smoker=='yes'):
            Smoker=1
        else:
            Smoker=0    
        if(Region=='northwest'):
            northwest=1
            southeast=0
            southwest=0
        elif(Region=='southeast'):
            northwest=0
            southeast=1
            southwest=0    
        elif(Region=='southwest'):
            northwest=0
            southeast=0
            southwest=1    
        else: 
            northwest=0
            southeast=0
            southwest=0   
     
        prediction=model.predict([[Age,BMI,Children,Gender,Smoker,northwest,southeast,southwest]])
        output=round(prediction[0],2)
        return render_template('index.html',prediction_text="INSURANCE CHARGES- {}".format(output))
        

if __name__=="__main__":
    app.run(debug=True)