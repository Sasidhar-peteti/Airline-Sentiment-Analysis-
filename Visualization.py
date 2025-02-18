
# Query 1: Count sentiment distribution
query1 = '''
SELECT airline_sentiment, COUNT(*) AS sentiment_count
FROM airport_sample
GROUP BY airline_sentiment;
'''
sentiment_dist = pd.read_sql(query1, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='airline_sentiment', y='sentiment_count', data=sentiment_dist)
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

# Query 2: Find top airlines with the most positive tweets
query2 = '''
SELECT airline, COUNT(*) AS positive_count
FROM airport_sample
WHERE airline_sentiment = 'positive'
GROUP BY airline
ORDER BY positive_count DESC
LIMIT 3;
'''
top_positive_airlines = pd.read_sql(query2, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='positive_count', y='airline', data=top_positive_airlines)
plt.title('Top Airlines with Most Positive Tweets')
plt.xlabel('Positive Tweet Count')
plt.ylabel('Airline')
plt.show()

# Query 3: Top 5 reasons for negative sentiment
query3 = '''
SELECT negativereason, COUNT(*) AS reason_count
FROM airport_sample
WHERE airline_sentiment = 'negative'
GROUP BY negativereason
ORDER BY reason_count DESC
LIMIT 5;
'''
top_negative_reasons = pd.read_sql(query3, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='reason_count', y='negativereason', data=top_negative_reasons)
plt.title('Top 5 Reasons for Negative Sentiment')
plt.xlabel('Reason Count')
plt.ylabel('Negative Reason')
plt.show()

# Query 4: Average retweets per sentiment type
query4 = '''
SELECT airline_sentiment, AVG(retweet_count) AS avg_retweets
FROM airport_sample
GROUP BY airline_sentiment;
'''
avg_retweets = pd.read_sql(query4, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='airline_sentiment', y='avg_retweets', data=avg_retweets)
plt.title('Average Retweets per Sentiment Type')
plt.xlabel('Sentiment')
plt.ylabel('Average Retweets')
plt.show()

# Query 5: Sentiment percentage per airline
query5 = '''
SELECT airline, airline_sentiment,
       COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY airline) AS sentiment_percentage
FROM airport_sample
GROUP BY airline, airline_sentiment;
'''
sentiment_percentage = pd.read_sql(query5, conn)

plt.figure(figsize=(10, 8))
sns.barplot(x='sentiment_percentage', y='airline', hue='airline_sentiment', data=sentiment_percentage)
plt.title('Sentiment Percentage per Airline')
plt.xlabel('Sentiment Percentage')
plt.ylabel('Airline')
plt.show()

# Query 6: Airlines with the worst negative sentiment ratio
query6 = '''
SELECT airline,
       COUNT(CASE WHEN airline_sentiment = 'negative' THEN 1 ELSE NULL END) * 100.0 / COUNT(*) AS negative_ratio
FROM airport_sample
GROUP BY airline
ORDER BY negative_ratio DESC;
'''
negative_ratio = pd.read_sql(query6, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='negative_ratio', y='airline', data=negative_ratio)
plt.title('Airlines with Worst Negative Sentiment Ratio')
plt.xlabel('Negative Sentiment Ratio (%)')
plt.ylabel('Airline')
plt.show()

# Query 7: Identify airlines with the highest customer engagement
query7 = '''
SELECT airline, SUM(retweet_count) AS total_retweets
FROM airport_sample
GROUP BY airline
ORDER BY total_retweets DESC
LIMIT 5;
'''
top_engaged_airlines = pd.read_sql(query7, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='total_retweets', y='airline', data=top_engaged_airlines)
plt.title('Airlines with Highest Customer Engagement')
plt.xlabel('Total Retweets')
plt.ylabel('Airline')
plt.show()

# Query 8: Identify most frequently mentioned airlines
query8 = '''
SELECT airline, COUNT(*) AS mention_count
FROM airport_sample
GROUP BY airline
ORDER BY mention_count DESC
LIMIT 5;
'''
most_mentioned_airlines = pd.read_sql(query8, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='mention_count', y='airline', data=most_mentioned_airlines)
plt.title('Most Frequently Mentioned Airlines')
plt.xlabel('Mention Count')
plt.ylabel('Airline')
plt.show()

# Query 9: Find the most common words in negative feedback
query9 = '''
SELECT negativereason, COUNT(*) AS frequency
FROM airport_sample
WHERE airline_sentiment = 'negative'
GROUP BY negativereason
ORDER BY frequency DESC
LIMIT 10;
'''
common_negative_words = pd.read_sql(query9, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='frequency', y='negativereason', data=common_negative_words)
plt.title('Most Common Words in Negative Feedback')
plt.xlabel('Frequency')
plt.ylabel('Negative Reason')
plt.show()

# Query 10: Sentiment trend over time (if timestamp data is available)
query10 = '''
SELECT strftime('%Y-%m', timestamp) AS month, airline_sentiment, COUNT(*) AS sentiment_count
FROM airport_sample
GROUP BY strftime('%Y-%m', timestamp), airline_sentiment
ORDER BY month ASC;
'''
sentiment_trend = pd.read_sql(query10, conn)

plt.figure(figsize=(10, 6))
sns.lineplot(x='month', y='sentiment_count', hue='airline_sentiment', data=sentiment_trend)
plt.title('Sentiment Trend Over Time')
plt.xlabel('Month')
plt.ylabel('Sentiment Count')
plt.xticks(rotation=45)
plt.show()

# Query 11: Peak hours for negative sentiment (if timestamp data is available)
query11 = '''
SELECT strftime('%H', timestamp) AS hour, COUNT(*) AS negative_count
FROM airport_sample
WHERE airline_sentiment = 'negative'
GROUP BY strftime('%H', timestamp)
ORDER BY negative_count DESC
LIMIT 5;
'''
peak_negative_hours = pd.read_sql(query11, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='hour', y='negative_count', data=peak_negative_hours)
plt.title('Peak Hours for Negative Sentiment')
plt.xlabel('Hour')
plt.ylabel('Negative Sentiment Count')
plt.show()

# Query 12: Airline with highest neutral feedback percentage
query12 = '''
SELECT airline,
       COUNT(CASE WHEN airline_sentiment = 'neutral' THEN 1 ELSE NULL END) * 100.0 / COUNT(*) AS neutral_ratio
FROM airport_sample
GROUP BY airline
ORDER BY neutral_ratio DESC
LIMIT 1;
'''
highest_neutral_ratio = pd.read_sql(query12, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='neutral_ratio', y='airline', data=highest_neutral_ratio)
plt.title('Airline with Highest Neutral Feedback Percentage')
plt.xlabel('Neutral Feedback Ratio (%)')
plt.ylabel('Airline')
plt.show()

# Query 13: Airlines with most complaints about delays
query13 = '''
SELECT airline, COUNT(*) AS delay_complaints
FROM airport_sample
WHERE negativereason = 'Flight Delay'
GROUP BY airline
ORDER BY delay_complaints DESC
LIMIT 5;
'''
delay_complaints = pd.read_sql(query13, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='delay_complaints', y='airline', data=delay_complaints)
plt.title('Airlines with Most Complaints About Delays')
plt.xlabel('Delay Complaints')
plt.ylabel('Airline')
plt.show()

# Query 14: Sentiment trends by day of the week (if timestamp data is available)
query14 = '''
SELECT strftime('%w', timestamp) AS day, airline_sentiment, COUNT(*) AS sentiment_count
FROM airport_sample
GROUP BY strftime('%w', timestamp), airline_sentiment
ORDER BY day ASC;
'''
sentiment_by_day = pd.read_sql(query14, conn)

plt.figure(figsize=(10, 6))
sns.lineplot(x='day', y='sentiment_count', hue='airline_sentiment', data=sentiment_by_day)
plt.title('Sentiment Trends by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Sentiment Count')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
plt.show()

# Query 15: Airlines with consistently positive feedback
query15 = '''
SELECT airline, COUNT(*) AS positive_tweets
FROM airport_sample
WHERE airline_sentiment = 'positive'
GROUP BY airline
HAVING COUNT(*) > (SELECT AVG(positive_count) FROM (SELECT airline, COUNT(*) AS positive_count FROM airport_sample WHERE airline_sentiment = 'positive' GROUP BY airline) subquery)
ORDER BY positive_tweets DESC;
'''
consistent_positive_feedback = pd.read_sql(query15, conn)

plt.figure(figsize=(8, 6))
sns.barplot(x='positive_tweets', y='airline', data=consistent_positive_feedback)
plt.title('Airlines with Consistently Positive Feedback')
plt.xlabel('Positive Tweet Count')
plt.ylabel('Airline')
plt.show()

# Close the connection after use
conn.close()
