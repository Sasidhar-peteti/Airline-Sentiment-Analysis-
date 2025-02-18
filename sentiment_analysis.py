from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Initialize Spark Session
spark = SparkSession.builder.appName("Airline Sentiment Analysis").getOrCreate()

# Load Dataset
data = spark.read.csv("airline_sentiment.csv", header=True, inferSchema=True)

data = data.select("text", "airline_sentiment")

indexer = StringIndexer(inputCol="airline_sentiment", outputCol="label")

# Tokenize text
tokenizer = Tokenizer(inputCol="text", outputCol="words")

# Remove stopwords
remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")

# Convert words to TF-IDF features
hashingTF = HashingTF(inputCol="filtered_words", outputCol="raw_features", numFeatures=10000)
idf = IDF(inputCol="raw_features", outputCol="features")

# Train a Logistic Regression model
lr = LogisticRegression(featuresCol="features", labelCol="label")

# Build pipeline
pipeline = Pipeline(stages=[indexer, tokenizer, remover, hashingTF, idf, lr])

# Split data into training and test sets
train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)

# Train the model
model = pipeline.fit(train_data)

# Make predictions
predictions = model.transform(test_data)

# Evaluate the model
evaluator = MulticlassClassificationEvaluator(labelCol="label", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)

print(f"Model Accuracy: {accuracy:.2f}")

# Save the model
model.save("sentiment_model")

# Stop Spark session
spark.stop()
