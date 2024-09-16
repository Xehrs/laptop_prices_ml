import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from flask import Flask, render_template, request
import joblib

# Data Process
rentalDF = pd.read_csv("data/rental_1000.csv")

# Data Transformation
X = rentalDF[['rooms','sqft']].values #Features
y = rentalDF['price'].values #Label

# Split Data into Training and Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Model Training
model = LinearRegression().fit(X_train,y_train)


# Model Save 
joblib.dump(model,'rental_price_model.joblib')

# Model Load
model = joblib.load('rental_price_model.joblib')

# Init Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    rooms = int(request.form['rooms'])
    sqft = int(request.form['sqft'])

    # Make prediction
    prediction = model.predict(np.array([[rooms,sqft]]))

    return render_template('result.html', prediction=prediction[0])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

# Model Prediction
# y_pred = model.predict(X_test)



# Compute RMSE
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# print(f"RMSE: {rmse}") 

# sample_index =0 # Change this index to test different samples 
# predict_rental_price = model.predict([X_test[sample_index]])[0]

# print(f"The Real Rental Price for Rooms count={X_test[sample_index][0]} and Area in Sqft={X_test[sample_index][1]} is={y_test[sample_index]}")
# print(f"The Predicted Rental Price for Rooms count={X_test[sample_index][0]} and Area in Sqft={X_test[sample_index][1]} is={predict_rental_price}")

# print("The Actual Rental Price for Rooms with Count =",X_test[0][0]," and","Sqft=",X_test[0][1],"is =", y_test[0])
# print("The Predicted Rental Price for Rooms with Count =",X_test[0][0]," and","Area in Sqft=",X_test[0][1],"is =",predict_rental_price)

# Metric -RMSE
# Root Mean Square Error