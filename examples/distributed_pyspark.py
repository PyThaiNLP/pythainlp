# SPDX-FileCopyrightText: 2016-2026 PyThaiNLP Project
# SPDX-FileType: DOCUMENTATION
# SPDX-License-Identifier: CC0-1.0
"""
Example: Using PyThaiNLP in PySpark Distributed Environment

This example demonstrates how to use PyThaiNLP in a distributed environment
like Apache Spark. The key is to set the PYTHAINLP_DATA_DIR environment
variable inside the function that will be distributed to executor nodes.

For more information, see:
https://github.com/PyThaiNLP/pythainlp/issues/475
"""

# Example 1: Basic PySpark setup with PyThaiNLP
def example_basic_spark():
    """
    Basic example showing how to tokenize Thai text in PySpark.
    """
    from pyspark import SparkContext

    sc = SparkContext("local[*]", "PyThaiNLP Example")

    # Sample Thai text data
    thai_texts = [
        "สวัสดีครับ ผมชื่อจอห์น",
        "ภาษาไทยเป็นภาษาที่สวยงาม",
        "PyThaiNLP ช่วยประมวลผลภาษาไทย",
    ]

    rdd = sc.parallelize(thai_texts)

    def tokenize_thai(text):
        """
        Tokenize Thai text using PyThaiNLP.

        IMPORTANT: Import and configure environment variables INSIDE the function
        that will be distributed to executor nodes.
        """
        import os

        # Set PYTHAINLP_DATA_DIR before importing pythainlp
        # Use './pythainlp-data' to store data in current working directory
        os.environ["PYTHAINLP_DATA_DIR"] = "./pythainlp-data"

        # Now import pythainlp modules
        from pythainlp.tokenize import word_tokenize

        # Perform tokenization
        return word_tokenize(text)

    # Apply tokenization to all texts in parallel
    tokenized_rdd = rdd.map(tokenize_thai)

    # Collect results
    results = tokenized_rdd.collect()
    for text, tokens in zip(thai_texts, results):
        print(f"Text: {text}")
        print(f"Tokens: {tokens}\n")

    sc.stop()


# Example 2: Using DataFrame API
def example_dataframe_api():
    """
    Example using PySpark DataFrame API with PyThaiNLP.
    """
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import udf
    from pyspark.sql.types import ArrayType, StringType

    spark = SparkSession.builder.appName("PyThaiNLP DataFrame Example").getOrCreate()

    # Create sample DataFrame
    data = [
        (1, "สวัสดีครับ ผมชื่อจอห์น"),
        (2, "ภาษาไทยเป็นภาษาที่สวยงาม"),
        (3, "PyThaiNLP ช่วยประมวลผลภาษาไทย"),
    ]
    df = spark.createDataFrame(data, ["id", "text"])

    # Define UDF for tokenization
    @udf(returnType=ArrayType(StringType()))
    def tokenize_udf(text):
        """
        UDF for tokenizing Thai text.

        IMPORTANT: Set environment variable and import inside the UDF.
        """
        import os

        os.environ["PYTHAINLP_DATA_DIR"] = "./pythainlp-data"

        from pythainlp.tokenize import word_tokenize

        return word_tokenize(text)

    # Apply tokenization
    result_df = df.withColumn("tokens", tokenize_udf(df.text))

    # Show results
    result_df.show(truncate=False)

    spark.stop()


# Example 3: Advanced configuration with multiple PyThaiNLP features
def example_advanced():
    """
    Advanced example using multiple PyThaiNLP features in PySpark.
    """
    from pyspark import SparkContext

    sc = SparkContext("local[*]", "PyThaiNLP Advanced Example")

    thai_texts = [
        "สวัสดีครับ ผมชื่อจอห์น",
        "ภาษาไทยเป็นภาษาที่สวยงาม",
    ]

    rdd = sc.parallelize(thai_texts)

    def process_thai_text(text):
        """
        Process Thai text with multiple PyThaiNLP features.
        """
        import os

        # Configure data directory
        os.environ["PYTHAINLP_DATA_DIR"] = "./pythainlp-data"

        # Import required modules
        from pythainlp.tokenize import word_tokenize
        from pythainlp.tag import pos_tag
        from pythainlp.util import normalize

        # Normalize text
        normalized = normalize(text)

        # Tokenize
        tokens = word_tokenize(normalized)

        # POS tagging
        tagged = pos_tag(tokens)

        return {
            "original": text,
            "normalized": normalized,
            "tokens": tokens,
            "pos_tags": tagged,
        }

    # Process all texts
    results = rdd.map(process_thai_text).collect()

    for result in results:
        print(f"Original: {result['original']}")
        print(f"Normalized: {result['normalized']}")
        print(f"Tokens: {result['tokens']}")
        print(f"POS Tags: {result['pos_tags']}\n")

    sc.stop()


# Example 4: Best practices for production environments
def example_production_best_practices():
    """
    Production-ready example with error handling and logging.
    """
    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder.appName("PyThaiNLP Production Example")
        .config("spark.python.worker.reuse", "true")  # Reuse Python workers
        .getOrCreate()
    )

    data = [
        (1, "สวัสดีครับ ผมชื่อจอห์น"),
        (2, "ภาษาไทยเป็นภาษาที่สวยงาม"),
        (3, None),  # Test handling of None
    ]
    df = spark.createDataFrame(data, ["id", "text"])

    def safe_tokenize(text):
        """
        Tokenize with error handling for production use.
        """
        import os

        try:
            # Set environment variables
            os.environ["PYTHAINLP_DATA_DIR"] = "./pythainlp-data"

            # Import modules
            from pythainlp.tokenize import word_tokenize

            # Handle None or empty strings
            if not text:
                return []

            return word_tokenize(text)

        except Exception as e:
            # Log error (in production, use proper logging)
            print(f"Error tokenizing text: {text}, Error: {str(e)}")
            return []

    # Register UDF
    from pyspark.sql.functions import udf
    from pyspark.sql.types import ArrayType, StringType

    tokenize_udf = udf(safe_tokenize, ArrayType(StringType()))

    # Apply tokenization
    result_df = df.withColumn("tokens", tokenize_udf(df.text))
    result_df.show(truncate=False)

    spark.stop()


if __name__ == "__main__":
    print("=" * 70)
    print("PyThaiNLP in PySpark - Examples")
    print("=" * 70)
    print("\nNote: These examples require Apache Spark to be installed:")
    print("  pip install pyspark")
    print("\nChoose an example to run:")
    print("1. Basic Spark example")
    print("2. DataFrame API example")
    print("3. Advanced features example")
    print("4. Production best practices example")
    print("\nTo run a specific example, uncomment the corresponding line below:")
    print("=" * 70)

    # Uncomment one of these to run:
    # example_basic_spark()
    # example_dataframe_api()
    # example_advanced()
    # example_production_best_practices()

    print("\n✓ Examples loaded successfully!")
    print("Uncomment an example function call to run it.")
