-- Create database
CREATE DATABASE sasi;

-- Use the created database
USE sasi;

-- Create table for storing airline sentiment data
CREATE TABLE airport_sample (
    airline STRING,
    airline_sentiment STRING,
    negativereason STRING,
    retweet_count INT
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE;

-- Load data into the table
LOAD DATA INPATH '/path/to/your/dataset.csv' INTO TABLE airport_sample;

-- Query 1: Count sentiment distribution
SELECT airline_sentiment, COUNT(*) AS sentiment_count 
FROM airport_sample 
GROUP BY airline_sentiment;

-- Query 2: Find top airlines with the most positive tweets
SELECT airline, COUNT(*) AS positive_count 
FROM airport_sample 
WHERE airline_sentiment = 'positive' 
GROUP BY airline 
ORDER BY positive_count DESC 
LIMIT 3;

-- Query 3: Top 5 reasons for negative sentiment
SELECT negativereason, COUNT(*) AS reason_count 
FROM airport_sample 
WHERE airline_sentiment = 'negative' 
GROUP BY negativereason 
ORDER BY reason_count DESC 
LIMIT 5;

-- Query 4: Average retweets per sentiment type
SELECT airline_sentiment, AVG(retweet_count) AS avg_retweets 
FROM airport_sample 
GROUP BY airline_sentiment;

-- Query 5: Sentiment percentage per airline
SELECT airline, airline_sentiment, 
       COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY airline) AS sentiment_percentage 
FROM airport_sample 
GROUP BY airline, airline_sentiment;

-- Query 6: Airlines with the worst negative sentiment ratio
SELECT airline, 
       COUNT(CASE WHEN airline_sentiment = 'negative' THEN 1 ELSE NULL END) * 100.0 / COUNT(*) AS negative_ratio 
FROM airport_sample 
GROUP BY airline 
ORDER BY negative_ratio DESC;

-- Query 7: Identify airlines with the highest customer engagement
SELECT airline, SUM(retweet_count) AS total_retweets
FROM airport_sample
GROUP BY airline
ORDER BY total_retweets DESC
LIMIT 5;

-- Query 8: Identify most frequently mentioned airlines
SELECT airline, COUNT(*) AS mention_count
FROM airport_sample
GROUP BY airline
ORDER BY mention_count DESC
LIMIT 5;

-- Query 9: Find the most common words in negative feedback
SELECT negativereason, COUNT(*) AS frequency
FROM airport_sample
WHERE airline_sentiment = 'negative'
GROUP BY negativereason
ORDER BY frequency DESC
LIMIT 10;

-- Query 10: Find the sentiment trend over time (if timestamp data is available)
SELECT DATE_FORMAT(timestamp, 'yyyy-MM') AS month, airline_sentiment, COUNT(*) AS sentiment_count
FROM airport_sample
GROUP BY DATE_FORMAT(timestamp, 'yyyy-MM'), airline_sentiment
ORDER BY month ASC;

-- Query 11: Identify peak hours for negative sentiment (if timestamp data is available)
SELECT HOUR(timestamp) AS hour, COUNT(*) AS negative_count
FROM airport_sample
WHERE airline_sentiment = 'negative'
GROUP BY HOUR(timestamp)
ORDER BY negative_count DESC
LIMIT 5;

-- Query 12: Determine the airline with the highest percentage of neutral feedback
SELECT airline, 
       COUNT(CASE WHEN airline_sentiment = 'neutral' THEN 1 ELSE NULL END) * 100.0 / COUNT(*) AS neutral_ratio
FROM airport_sample
GROUP BY airline
ORDER BY neutral_ratio DESC
LIMIT 1;

-- Query 13: Find airlines with the most complaints about delays
SELECT airline, COUNT(*) AS delay_complaints
FROM airport_sample
WHERE negativereason = 'Flight Delay'
GROUP BY airline
ORDER BY delay_complaints DESC
LIMIT 5;

-- Query 14: Analyze sentiment trends by day of the week (if timestamp data is available)
SELECT DAYOFWEEK(timestamp) AS day, airline_sentiment, COUNT(*) AS sentiment_count
FROM airport_sample
GROUP BY DAYOFWEEK(timestamp), airline_sentiment
ORDER BY day ASC;

-- Query 15: Identify airlines with consistently positive feedback
SELECT airline, COUNT(*) AS positive_tweets
FROM airport_sample
WHERE airline_sentiment = 'positive'
GROUP BY airline
HAVING COUNT(*) > (SELECT AVG(positive_count) FROM (SELECT airline, COUNT(*) AS positive_count FROM airport_sample WHERE airline_sentiment = 'positive' GROUP BY airline) subquery)
ORDER BY positive_tweets DESC;
