import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from flask import Flask, render_template, request
import joblib

# Data Process
laptopDF = pd.read_csv("data/laptop_prices.csv")

# Data Transformation
# X = laptopDF[['Company','Product','TypeName','Inches','Ram','OS','Weight','Screen','ScreenW','ScreenH','Touchscreen','IPSpanel','RetinaDisplay','CPU_company','CPU_freq','CPU_model','PrimaryStorage','SecondaryStorage','PrimaryStorageType','SecondaryStorageType','GPU_company','GPU_model']].values #Features

# x_features = laptopDF[['Ram','Weight','GPU_model']].values # Features for RAM, weight, and GPU model
x_features = laptopDF[['Ram','Weight','PrimaryStorage']].values # Features for RAM, weight, and GPU model
y = laptopDF['Price_euros'].values # Label

# Split Data into Training and Testing
X_train, X_test, y_train, y_test = train_test_split(x_features, y, test_size=0.20)

# Model Training
model = LinearRegression().fit(X_train,y_train)


# Model Save 
joblib.dump(model,'laptop_price_model.joblib')

# Model Load
model = joblib.load('laptop_price_model.joblib')

# Init Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    ram = int(request.form['ram'])
    weight = float(request.form['weight'])
    # gpu_model = string(request.form['GPU_model'])
    primaryStorage = int(request.form['PrimaryStorage'])

    # Make prediction
    prediction = model.predict(np.array([[ram,weight,primaryStorage]]))

    return render_template('result.html', prediction=prediction[0])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

# Model Prediction
# y_pred = model.predict(X_test)



# Compute RMSE
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# print(f"RMSE: {rmse}") 

# sample_index =0 # Change this index to test different samples 
# predict_laptop_price = model.predict([X_test[sample_index]])[0]

# print(f"The Real laptop Price for ram count={X_test[sample_index][0]} and Area in weight={X_test[sample_index][1]} is={y_test[sample_index]}")
# print(f"The Predicted laptop Price for ram count={X_test[sample_index][0]} and Area in weight={X_test[sample_index][1]} is={predict_laptop_price}")

# print("The Actual laptop Price for ram with Count =",X_test[0][0]," and","weight=",X_test[0][1],"is =", y_test[0])
# print("The Predicted laptop Price for ram with Count =",X_test[0][0]," and","Area in weight=",X_test[0][1],"is =",predict_laptop_price)

# Metric -RMSE
# Root Mean Square Error