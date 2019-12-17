# Spark API Mini Exercises

Copy the code below to create a pandas dataframe with 20 rows and 3 columns:

```python
import pandas as pd
import numpy as np

np.random.seed(13)

pandas_dataframe = pd.DataFrame(
    {
        "n": np.random.randn(20),
        "group": np.random.choice(list("xyz"), 20),
        "abool": np.random.choice([True, False], 20),
    }
)
```

1. Spark Dataframe Basics

    1. Use the starter code above to create a pandas dataframe.
    1. Convert the pandas dataframe to a spark dataframe. From this point
       forward, do all of your work with the spark dataframe, not the pandas
       dataframe.
    1. Show the first 3 rows of the dataframe.
    1. Show the first 7 rows of the dataframe.
    1. View a summary of the data using `.describe`.
    1. Use `.select` to create a new dataframe with just the `n` and `abool`
       columns. View the first 5 rows of this dataframe.
    1. Use `.select` to create a new dataframe with just the `group` and `abool`
       columns. View the first 5 rows of this dataframe.
    1. Use `.select` to create a new dataframe with the `group` column and the
       `abool` column renamed to `a_boolean_value`. Show the first 3 rows of
       this dataframe.
    1. Use `.select` to create a new dataframe with the `group` column and the
       `n` column renamed to `a_numeric_value`. Show the first 6 rows of this
       dataframe.

1. Column Manipulation

    1. Use the starter code above to re-create a spark dataframe. Store the
       spark dataframe in a varaible named `df`

    1. Use `.select` to add 4 to the `n` column. Show the results.

    1. Subtract 5 from the `n` column and view the results.

    1. Multiply the `n` column by 2. View the results along with the original
       numbers.

    1. Add a new column named `n2` that is the `n` value multiplied by -1. Show
       the first 4 rows of your dataframe. You should see the original `n` value
       as well as `n2`.

    1. Add a new column named `n3` that is the n value squared. Show the first 5
       rows of your dataframe. You should see both `n`, `n2`, and `n3`.

    1. What happens when you run the code below?

        ```python
        df.group + df.abool
        ```

    1. What happens when you run the code below? What is the difference between
       this and the previous code sample?

        ```python
        df.select(df.group + df.abool)
        ```

    1. Try adding various other columns together. What are the results of
       combining the different data types?

1. Spark SQL

    1. Use the starter code above to re-create a spark dataframe.
    1. Turn your dataframe into a table that can be queried with spark SQL. Name
       the table `my_df`. Answer the rest of the questions in this section with
       a spark sql query (`spark.sql`) against `my_df`. After each step, view
       the first 7 records from the dataframe.
    1. Write a query that shows all of the columns from your dataframe.
    1. Write a query that shows just the `n` and `abool` columns from the
       dataframe.
    1. Write a query that shows just the `n` and `group` columns. Rename the
       `group` column to `g`.
    1. Write a query that selects `n`, and creates two new columns: `n2`, the
       original `n` values halved, and `n3`: the original n values minus 1.
    1. What happens if you make a SQL syntax error in your query?

1. Type casting

    1. Use the starter code above to re-create a spark dataframe.

    1. Use `.printSchema` to view the datatypes in your dataframe.

    1. Use `.dtypes` to view the datatypes in your dataframe.

    1. What is the difference between the two code samples below?

        ```python
        df.abool.cast('int')
        ```

        ```python
        df.select(df.abool.cast('int')).show()
        ```

    1. Use `.select` and `.cast` to convert the `abool` column to an integer
       type. View the results.
    1. Convert the `group` column to a integer data type and view the results.
       What happens?
    1. Convert the `n` column to a integer data type and view the results. What
       happens?
    1. Convert the `abool` column to a string data type and view the results.
       What happens?

1. Built-in Functions

    1. Use the starter code above to re-create a spark dataframe.
    1. Import the necessary functions from `pyspark.sql.functions`
    1. Find the highest `n` value.
    1. Find the lowest `n` value.
    1. Find the average `n` value.
    1. Use `concat` to change the `group` column to say, e.g. "Group: x" or
       "Group: y"
    1. Use `concat` to combine the `n` and `group` columns to produce results
       that look like this: "x: -1.432" or "z: 2.352"

1. Filter / Where

    1. Use the starter code above to re-create a spark dataframe.
    1. Use `.filter` or `.where` to select just the rows where the group is `y`
       and view the results.
    1. Select just the columns where the `abool` column is false and view the
       results.
    1. Find the columns where the `group` column is *not* `y`.
    1. Find the columns where `n` is positive.
    1. Find the columns where `abool` is true and the `group` column is `z`.
    1. Find the columns where `abool` is true or the `group` column is `z`.
    1. Find the columns where `abool` is false and `n` is less than 1
    1. Find the columns where `abool` is false or `n` is less than 1

1. When / Otherwise

    1. Use the starter code above to re-create a spark dataframe.
    1. Use `when` and `.otherwise` to create a column that contains the text "It
       is true" when `abool` is true and "It is false"" when `abool` is false.
    1. Create a column that contains 0 if n is less than 0, otherwise, the
       original n value.

1. Sorting

    1. Use the starter code above to re-create a spark dataframe.
    1. Sort by the `n` value.
    1. Sort by the `group` value, both ascending and descending.
    1. Sort by the group value first, then, within each group, sort by `n`
       value.
    1. Sort by `abool`, `group`, and `n`. Does it matter in what order you
       specify the columns when sorting?

1. Aggregating

    1. What is the average `n` value for each group in the `group` column?
    1. What is the maximum `n` value for each group in the `group` column?
    1. What is the minimum `n` value by `abool`?
    1. What is the average `n` value for each unique combination of the `group`
       and `abool` column?

1. Explain

1. Joins
