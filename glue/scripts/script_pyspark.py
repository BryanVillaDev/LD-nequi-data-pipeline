import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

class TransactionETL:
    def __init__(self, spark, input_path, output_path):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path

    def load_data(self):
        """
        Carga el CSV desde S3 (o ruta dfinida) en un DataFrame.
        """
        return self.spark.read.csv(self.input_path, header=True, inferSchema=True)

    def transform_data(self, df):
        """
        Aplica transformaciones y limpieza, por ejemplo:
        reemplaza valores nulos en 'amount' por 0.0.
        """
        return df.withColumn(
            "amount",
            when(col("amount").isNull(), 0.0).otherwise(col("amount"))
        )

    def save_data(self, df):
        """
        Escribe el DataFrame transformado a un destino.
        Se utiliza Parquet como ejemplo, aunque en producción se podría usar Apache Hudi.
        """
        df.write.mode("overwrite").parquet(self.output_path)

    def run(self):
        """
        Ejecuta el proceso ETL completo.
        """
        df = self.load_data()
        df_clean = self.transform_data(df)
        self.save_data(df_clean)
        print("ETL completado exitosamente.")

def main():
    spark = SparkSession.builder.appName("TransactionsETL").getOrCreate()
    
    # Obtener rutas desde variables de entorno; si no existen, se usan valores por defecto.
    input_path = os.environ.get("INPUT_PATH", "s3://ld-poc-nequi/transactions.csv")
    output_path = os.environ.get("OUTPUT_PATH", "s3://ld-poc-nequit/output/transactions_parquet/")
    
    etl = TransactionETL(spark, input_path, output_path)
    etl.run()
    spark.stop()

if __name__ == "__main__":
    main()
