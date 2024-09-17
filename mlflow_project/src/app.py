from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
import mlflow
import mlflow.spark

spark = SparkSession.builder.getOrCreate()

# Read the CSV file into a Spark DataFrame
mldataset_path = '../data/laptop_prices.csv'
modelpath = 'model/'

# Set the experiment
mlflow.set_experiment("laptop_prices_prediction_experiment")

laptop_pricesDF = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(mldataset_path) 
    # .withColumnRenamed("RAM (gb)", "ram") \
    # .withColumnRenamed("Weight (kg)", "weight") \
    # .withColumnRenamed("Primary Storage (gb)", "PrimaryStorage") \
    # .withColumnRenamed("Price (Euros)", "Price_euros")

splits = laptop_pricesDF.randomSplit([0.7, 0.3])
train_data = splits[0]
test_data = splits[1]
print("Training Rows:", train_data.count(), "Testing Rows:", test_data.count())


# Prepare features and label columns
feature_cols = ['Ram', 'Weight', 'PrimaryStorage']
assembler = VectorAssembler(inputCols=feature_cols, outputCol='features')

# Define the Linear Regression model
lr = LinearRegression(featuresCol='features', labelCol='Price_euros')

# Define the pipeline
pipeline = Pipeline(stages=[assembler, lr])

# Fit the model
model = pipeline.fit(train_data)

# Evaluate the model on test data
predictions = model.transform(test_data)
evaluator = RegressionEvaluator(labelCol='Price_euros', predictionCol='prediction', metricName='rmse')
rmse = evaluator.evaluate(predictions)

# Log evaluation metric
mlflow.log_metric("rmse", rmse)

# Print RMSE
print("Root Mean Squared Error (RMSE):", rmse)

# Save MLflow run ID for reference
run_id = mlflow.active_run().info.run_id
print("MLflow run completed with ID:", run_id)

# Save the PySpark model using MLflow
mlflow.spark.save_model(model, modelpath)

print("Experiment run complete.")
