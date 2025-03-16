# Modelo Operativo para LD-nequi-data-pipeline

## 1. Introducción

Este modelo operativo define cómo vamos a manejar el pipeline de datos, asegurando que todo funcione de forma automática, segura y con alta calidad. Desde que llegan los archivos a S3 hasta que los analizamos en herramientas de BI. Se basa en prácticas como **TDD, SOLID y Clean Architecture**, y el uso de **CI/CD** para los despliegues.

## 2. Componentes del Modelo Operativo

### 2.1. Ingesta y Trigger
- **Qué pasa**:  
  - Se configuran **hooks en Airflow** para extraer datos desde bases de datos **SQL**.  
  - Se programan queries automatizadas que extraen y cargan los datos a un **bucket S3** o los procesan directamente en AWS Glue.  
  - También se cargan archivos **CSV** en un bucket de **S3** desde fuentes externas.  
  - La llegada de archivos o la ejecución programada de queries dispara un DAG en **Airflow**.  

- **Orígenes de datos**:  
  - Bases de datos relacionales (**PostgreSQL, MySQL, SQL Server, Oracle**).  
  - Archivos en formato **CSV, JSON o Parquet** desde sistemas externos.  
  - APIs o servicios de terceros que envían datos en tiempo programado.  

- **Quién lo cuida**:  
  - El equipo de **DataOps**, que monitorea la ingesta de datos y mantiene los pipelines funcionando correctamente.  

- **Métricas a seguir**:  
  - **Tiempo de ingesta**: cuánto tarda en extraerse y cargarse la data.  
  - **Porcentaje de éxito**: cantidad de archivos o queries completadas vs. fallidas.  
  - **Volumen de datos**: cantidad de registros procesados por ejecución.  


### 2.2. Procesamiento y Curado
- **Qué pasa**:  
  - **Airflow** orquesta jobs en **AWS Glue**.  
  - **PySpark** procesa los CSV, aplicando transformaciones, validaciones y curado con **Apache Hudi**.  
- **Quién lo cuida**:  
  - Equipo de ETL / Ingeniería de datos.  
- **Métricas a seguir**:  
  - Tiempo de procesamiento.  
  - Tasa de éxito en las transformaciones.  
  - Versionado correcto de los datos con Hudi.  

### 2.3. Notificaciones y Monitoreo
- **Qué pasa**:  
  - Alertas automáticas vía **SES, Slack y Teams**.  
  - **CloudWatch y Grafana** para logs y métricas.  
- **Quién lo cuida**:  
  - DevOps / Operaciones.  
- **Métricas a seguir**:  
  - Tiempo de respuesta ante incidentes.  
  - Número de alertas críticas resueltas.  

### 2.4. Almacenamiento y Análisis
- **Qué pasa**:  
  - Datos en **S3** y carga en **Snowflake** si es necesario.  
  - Conexión con herramientas de BI como **QuickSight** o **Grafana**.  
- **Quién lo cuida**:  
  - Equipo de BI y Data Analysts.  
- **Métricas a seguir**:  
  - Latencia en la carga a Snowflake.  
  - Calidad de los dashboards generados.  

### 2.5. CI/CD y Despliegue
- **Qué pasa**:  
  - **Terraform** maneja la infraestructura.  
  - **GitHub Actions** ejecuta validaciones cuando hay cambios en el código.  
  - Flujo de revisión con Pull Requests y code review.  
- **Quién lo cuida**:  
  - DevOps y desarrollo.  
- **Métricas a seguir**:  
  - Tiempo de despliegue.  
  - Cobertura de pruebas automatizadas.  

## 3. Roles y Responsabilidades

- **Líder de Datos**: Supervisa, revisa y aprueba el código.  
- **Desarrolladores/Ingenieros de Datos**: Desarrollan y mantienen el pipeline.  
- **DevOps/Operaciones**: Gestionan la infraestructura y monitoreo.  
- **Equipo de BI**: Crean y mantienen dashboards y análisis.  

## 4. Procesos y Flujos de Trabajo

### 4.1. Flujo de Datos
1. **Ingesta**: Llega un archivo a S3 → Se dispara un DAG en Airflow.  
2. **Procesamiento**: Airflow ejecuta Glue → PySpark transforma y cura los datos con Hudi.  
3. **Carga y Análisis**: Datos almacenados en S3 → Se cargan en Snowflake → Se analizan con BI.  

### 4.2. Flujo de Desarrollo y Despliegue
1. **Commit & Push**: El desarrollador sube cambios.  
2. **Pull Request & CI/CD**: Se ejecutan tests y validaciones.  
3. **Code Review**: El líder revisa y aprueba o pide cambios.  
4. **Merge & Despliegue**: Se integran los cambios y se despliegan con Terraform.  

## 5. Gestión de Incidencias y Soporte

- **Plan de Respuesta**: Se definen tiempos y responsables por tipo de incidente.  
- **Herramientas**: CloudWatch y alertas en Slack para monitoreo en tiempo real.  
- **Registro de Incidentes**: Documentación de cada fallo y mejoras postmortem.  

## 6. Mantenimiento y Mejora Continua

- **Revisiones Periódicas**: Se analizan logs y métricas para optimizar procesos.  
- **Capacitaciones**: Entrenamientos regulares para el equipo.  
- **Feedback y Ajustes**: Se toman acciones con base en métricas y retroalimentación.  

## 7. Seguridad y Cumplimiento

- **Cifrado de Datos**: Encriptación en reposo y en tránsito.  
- **Gestión de Accesos**: Roles y permisos en AWS IAM con privilegios mínimos.  
- **Auditoría**: CloudTrail y AWS Config para seguimiento de cambios.  

## 8. Documentación y Capacitación

- **Repositorio de Documentación**: En el directorio `docs/` (diagramas, manuales, etc.).  
- **Capacitaciones**: Formación periódica para nuevos integrantes.  
- **Protocolos Documentados**: Guías de operación, despliegue y manejo de incidencias.  

## 9. Conclusión

Este modelo operativo nos permite tener control total sobre el pipeline, asegurando que todo fluya sin problemas, con buenas prácticas, monitoreo y automatización. La clave está en la mejora continua, con revisiones regulares y optimización en cada etapa.

