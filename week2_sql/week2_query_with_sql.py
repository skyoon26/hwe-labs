from pyspark.sql import SparkSession

### Setup: Create a SparkSession
spark = SparkSession.builder.appName("Week2SQL").master("local[1]").getOrCreate()

# For Windows users, quiet errors about not being able to delete temporary directories which make your logs impossible to read...
logger = spark.sparkContext._jvm.org.apache.log4j
logger.LogManager.getLogger("org.apache.spark.util.ShutdownHookManager").setLevel(
    logger.Level.OFF
)
logger.LogManager.getLogger("org.apache.spark.SparkEnv").setLevel(logger.Level.ERROR)

### Questions

# Question 1: Read the tab separated file named "resources/reviews.tsv.gz" into a dataframe. Call it "reviews".
reviews = spark.read.csv("resources/reviews.tsv.gz", sep="\t", header=True)
reviews.printSchema()

# Question 2: Create a virtual view on top of the reviews dataframe, so that we can query it with Spark SQL.
reviews.createOrReplaceTempView("reviews")

# Question 3: Add a column to the dataframe named "review_timestamp", representing the current time on your computer.
df_with_timestamp = spark.sql(
    "SELECT *, current_timestamp() AS review_timestamp FROM reviews"
)

# Question 4: How many records are in the reviews dataframe?
spark.sql("SELECT count(*) AS total_records FROM reviews").show()

# Question 5: Print the first 5 rows of the dataframe.
# Some of the columns are long - print the entire record, regardless of length.
spark.sql("SELECT * FROM reviews LIMIT 5").show(truncate=True)

# Question 6: Create a new dataframe based on "reviews" with exactly 1 column: the value of the product category field.
# Look at the first 50 rows of that dataframe.
# Which value appears to be the most common? Digital_Video_Games
spark.sql("SELECT product_category FROM reviews").show(n=50, truncate=False)

# Question 7: Find the most helpful review in the dataframe - the one with the highest number of helpful votes.
# What is the product title for that review? How many helpful votes did it have?
spark.sql(
    "SELECT product_title, helpful_votes FROM reviews ORDER BY helpful_votes DESC"
).show(n=1, truncate=False)

# Question 8: How many reviews exist in the dataframe with a 5 star rating?
spark.sql("SELECT count(*) AS five_stars FROM reviews WHERE star_rating = 5").show()

# Question 9: Currently every field in the data file is interpreted as a string, but there are 3 that should really be numbers.
# Create a new dataframe with just those 3 columns, except cast them as "int"s.
# Look at 10 rows from this dataframe.
spark.sql(
    "SELECT \
        cast(star_rating as int) AS star_rating, \
        cast(helpful_votes as int) AS helpful_votes, \
        cast(total_votes as int) AS total_votes \
    FROM reviews"
).show(n=10)

# Question 10: Find the date with the most purchases.
# Print the date and total count of the date which had the most purchases.
spark.sql(
    "SELECT purchase_date, count(*) AS total_purchases \
    FROM reviews \
    GROUP BY purchase_date \
    ORDER BY total_purchases DESC"
).show(n=1)

##Question 11: Write the dataframe from Question 3 to your drive in JSON format.
##Feel free to pick any directory on your computer.
##Use overwrite mode.
df_with_timestamp.write.mode("overwrite").json("resources/reviews_json")

### Teardown
# Stop the SparkSession
spark.stop()
