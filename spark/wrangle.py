import pyspark.sql
from pyspark.sql.functions import (
    expr,
    col,
    to_timestamp,
    format_string,
    regexp_extract,
    datediff,
    current_timestamp,
    when,
    max,
    lit,
)


def get_311_data(spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
    print("[wrangle.py] reading case.csv")
    df = spark.read.csv("data/case.csv", header=True, inferSchema=True)
    return df.withColumnRenamed("SLA_due_date", "case_due_date")


def handle_dtypes(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    print("[wrangle.py] handling data types")
    return (
        df.withColumn("case_closed", expr('case_closed == "YES"'))
        .withColumn("case_late", expr('case_late == "YES"'))
        .withColumn("council_district", col("council_district").cast("string"))
    )


def handle_dates(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    print("[wrangle.py] parsing dates")
    fmt = "M/d/yy H:mm"
    return (
        df.withColumn("case_opened_date", to_timestamp("case_opened_date", fmt))
        .withColumn("case_closed_date", to_timestamp("case_closed_date", fmt))
        .withColumn("case_due_date", to_timestamp("case_due_date", fmt))
    )


def add_features(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    print("[wrangle.py] adding features")
    max_date = df.select(max("case_closed_date")).first()[0]
    return (
        df.withColumn("num_weeks_late", expr("num_days_late / 7 AS num_weeks_late"))
        .withColumn(
            "council_district",
            format_string("%03d", col("council_district").cast("int")),
        )
        .withColumn("zipcode", regexp_extract("request_address", r"\d+$", 0))
        .withColumn("case_age", datediff(lit(max_date), "case_opened_date"))
        .withColumn("days_to_closed", datediff("case_closed_date", "case_opened_date"))
        .withColumn(
            "case_lifetime",
            when(expr("! case_closed"), col("case_age")).otherwise(
                col("days_to_closed")
            ),
        )
    )


def join_departments(
    case_df: pyspark.sql.DataFrame, spark: pyspark.sql.SparkSession
) -> pyspark.sql.DataFrame:
    print("[wrangle.py] joining departments")
    dept = spark.read.csv("data/dept.csv", header=True, inferSchema=True)
    return (
        case_df.join(dept, "dept_division", "left")
        # drop all the columns except for standardized name, as it has much fewer unique values
        .drop(dept.dept_division)
        .drop(dept.dept_name)
        .drop(case_df.dept_division)
        .withColumnRenamed("standardized_dept_name", "department")
        # convert to a boolean
        .withColumn("dept_subject_to_SLA", col("dept_subject_to_SLA") == "YES")
    )


def wrangle_311(spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
    df = add_features(handle_dates(handle_dtypes(get_311_data(spark))))
    return join_departments(df, spark)


# # ## Train Test Split
# train, test = df.randomSplit([0.8, 0.2])
# train, validate, test = df.randomSplit([0.6, 0.2, 0.2])

if __name__ == "__main__":
    spark = pyspark.sql.SparkSession.builder.getOrCreate()
    df = wrangle_311(spark)
