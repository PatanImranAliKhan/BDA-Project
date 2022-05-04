from flask import Flask, render_template, request

import pandas as pd
import pickle

app = Flask(__name__)

data=pd.read_csv('house_price_prediction_data.csv')
pipe = pickle.load(open("Model.pkl", 'rb'))

@app.route('/')
def HomePage():
    locations=data['location'].unique()
    # print(data['location'].unique())
    # print(location)
    return render_template('index.html',locations=locations)

@app.route('/predict',methods = ['POST'])
def Prediction():
    try:
        bhk=request.form.get('bhk')
        bath=request.form.get('bath')
        location=request.form.get('location')
        sqft=request.form.get('feet')
        print(bhk)
        print(bath,location,sqft)
        data = pd.DataFrame([[location,bhk,sqft,bath]],columns=['location','size','total_sqft','bath'])
        pred = pipe.predict(data)[0]
        if(pred<0):
            pred=pred*-1
        print(pred)
        pred=pred*100000
        pred=round(pred)
        return render_template('result.html',data = {'bhk':bhk,'bath':bath,'location':location,'sqft':sqft,'result':pred})


    except Exception as e:
        print(e)

if __name__ == '__main__':
   app.run(debug=True)