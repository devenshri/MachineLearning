from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open('car_price.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    year = int(request.form['Year'])
    Num_Year = 2020 - year
    
    Present_Price = float(request.form['Present_Price'])
    
    Kms_Driven = int(request.form['Kms_Driven'])
    
    Owner = int(request.form['Owner'])
    
    fuel_type_petrol = request.form['Fuel_Type_Petrol']
    if fuel_type_petrol == 'Petrol':
        Fuel_Type_Petrol = 1
        Fuel_Type_Diesel = 0
    else:
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 1       
    seller_type = request.form['Seller_Type_Individual']
    if seller_type == 'Individual':
        Seller_Type_Individual = 1
    else:
        Seller_Type_Individual = 0
    
    trans_manual = request.form['Transmission_Mannual']
    if trans_manual == 'Mannual':
        Transmission_Manual = 1
    else:
        Transmission_Manual = 0
    
    
#    #'Present_Price', 'Kms_Driven', 'Owner', 'Num_Year', 'Fuel_Type_Diesel',
#    #'Fuel_Type_Petrol', 'Seller_Type_Individual', 'Transmission_Manual'
    prediction = model.predict([[Present_Price, Kms_Driven, Owner, Num_Year, Fuel_Type_Diesel,
       Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
    price = round(prediction[0],2)
    if price<0:
        return render_template('index.html',prediction_text="Sorry you cannot sell this car")
    else:
        return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(price)) 
    

if __name__ == "__main__":
    app.run(debug=True)