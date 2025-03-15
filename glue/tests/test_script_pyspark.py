import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
# Importa la clase desde el script. Ajusta la ruta según la estructura de tu proyecto.
from glue.scripts.script_pyspark import TransactionETL

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .master("local[*]") \
        .appName("PySparkTest") \
        .getOrCreate()

def test_transform_data(spark):
    # Datos de ejemplo: incluye una fila con valor nulo en 'amount'
    data = [
        (1, 100.50, "USD", 123, "2023-01-01 10:00:00"),
        (2, None, "USD", 124, "2023-01-02 11:15:00"),
    ]
    columns = ["transaction_id", "amount", "currency", "customer_id", "timestamp"]
    df = spark.createDataFrame(data, columns)
    
    etl = TransactionETL(spark, input_path="", output_path="")  # input/output no se usan en este test
    df_transformed = etl.transform_data(df)
    
    # Verificar que el valor nulo en 'amount' se reemplace por 0.0
    row_with_null = df_transformed.filter(col("transaction_id") == 2).collect()[0]
    assert row_with_null["amount"] == 0.0
