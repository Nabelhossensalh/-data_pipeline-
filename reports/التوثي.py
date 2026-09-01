Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\WINDOWS\system32> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> python src\main.py `
>>   --step quality `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "tools\mongo-spark-connector_2.12-10.7.0-all.jar" `
>>   --reports-dir "reports" `
>>   --limit 10000
>>
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 05:04:25 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
26/08/24 05:04:25 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
duplicate order_id keys: 207689
{
  "step": "quality",
  "input": null,
  "error_type": "Py4JJavaError",
  "error_message": "An error occurred while calling o68.load.\n: org.apache.spark.SparkClassNotFoundException: [DATA_SOURCE_NOT_FOUND] Failed to find the data source: mongodb. Please find packages at `https://spark.apache.org/third-party-projects.html`.\r\n\tat org.apache.spark.sql.errors.QueryExecutionErrors$.dataSourceNotFoundError(QueryExecutionErrors.scala:725)\r\n\tat org.apache.spark.sql.execution.datasources.DataSource$.lookupDataSource(DataSource.scala:647)\r\n\tat org.apache.spark.sql.execution.datasources.DataSource$.lookupDataSourceV2(DataSource.scala:697)\r\n\tat org.apache.spark.sql.DataFrameReader.load(DataFrameReader.scala:208)\r\n\tat org.apache.spark.sql.DataFrameReader.load(DataFrameReader.scala:172)\r\n\tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)\r\n\tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)\r\n\tat java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\r\n\tat java.base/java.lang.reflect.Method.invoke(Method.java:568)\r\n\tat py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)\r\n\tat py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)\r\n\tat py4j.Gateway.invoke(Gateway.java:282)\r\n\tat py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)\r\n\tat py4j.commands.CallCommand.execute(CallCommand.java:79)\r\n\tat py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)\r\n\tat py4j.ClientServerConnection.run(ClientServerConnection.java:106)\r\n\tat java.base/java.lang.Thread.run(Thread.java:842)\r\nCaused by: java.lang.ClassNotFoundException: mongodb.DefaultSource\r\n\tat java.base/java.net.URLClassLoader.findClass(URLClassLoader.java:445)\r\n\tat java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:587)\r\n\tat java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:520)\r\n\tat org.apache.spark.sql.execution.datasources.DataSource$.$anonfun$lookupDataSource$5(DataSource.scala:633)\r\n\tat scala.util.Try$.apply(Try.scala:213)\r\n\tat org.apache.spark.sql.execution.datasources.DataSource$.$anonfun$lookupDataSource$4(DataSource.scala:633)\r\n\tat scala.util.Failure.orElse(Try.scala:224)\r\n\tat org.apache.spark.sql.execution.datasources.DataSource$.lookupDataSource(DataSource.scala:633)\r\n\t... 15 more\r\n",
  "recovery": "Check the reported resource, path, schema, MongoDB, Java, or Connector requirement; no partial JSON result is treated as successful."
}
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> SUCCESS: The process with PID 25516 (child process of PIPS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>  has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> if (-not (Test-Path $Jar)) {
>>     throw "Connector JAR غير موجود: $Jar"
>> }
>>
>> Write-Host "Connector:" $Jar
>> Get-Item $Jar | Select-Object FullName,Length
>>
>> # إجبار Spark JVM على تحميل Connector قبل إنشاء SparkSession
>> $env:PYSPARK_SUBMIT_ARGS = "--jars `"$Jar`" pyspark-shell"
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step quality `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 10000
>>
Resolve-Path : Cannot find path
'C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\tools\mongo-spark-connector_2.12-10.7.0-all.jar' because
it does not exist.
At line:3 char:9
+ $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.j ...
+         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (C:\Users\PC\Des...-10.7.0-all.jar:String) [Resolve-Path], ItemNotFoundE
   xception
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.ResolvePathCommand

Test-Path : Cannot bind argument to parameter 'Path' because it is null.
At line:5 char:21
+ if (-not (Test-Path $Jar)) {
+                     ~~~~
    + CategoryInfo          : InvalidData: (:) [Test-Path], ParameterBindingValidationException
    + FullyQualifiedErrorId : ParameterArgumentValidationErrorNullNotAllowed,Microsoft.PowerShell.Commands.TestPathCom
   mand

Connector:
Get-Item : Cannot bind argument to parameter 'Path' because it is null.
At line:10 char:10
+ Get-Item $Jar | Select-Object FullName,Length
+          ~~~~
    + CategoryInfo          : InvalidData: (:) [Get-Item], ParameterBindingValidationException
    + FullyQualifiedErrorId : ParameterArgumentValidationErrorNullNotAllowed,Microsoft.PowerShell.Commands.GetItemComm
   and

usage: main.py [-h] [--step {discover,raw-load,quality,cleaning,all,quarantine-view}] [--input INPUT]
               [--run-id RUN_ID] [--engine {auto,python_batch,pyspark}] [--threshold-mb THRESHOLD_MB]
               [--mongo-uri MONGO_URI] [--database DATABASE] [--partitions PARTITIONS] [--batch-size BATCH_SIZE]
               [--master MASTER] [--connector-jar CONNECTOR_JAR] [--limit LIMIT] [--reports-dir REPORTS_DIR]
               [--local-store LOCAL_STORE] [--view-limit VIEW_LIMIT] [--storage-backend {auto,mongo,local}]
main.py: error: argument --connector-jar: expected one argument
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> $Base = "C:\Users\PC\Desktop\big_data_progect"
>> $Project = Join-Path $Base "midterm1-data-pipeline"
>> $Tools = Join-Path $Project "tools"
>> $JarName = "mongo-spark-connector_2.12-10.7.0-all.jar"
>> $TargetJar = Join-Path $Tools $JarName
>>
>> New-Item -ItemType Directory -Force -Path $Tools | Out-Null
>>
>> $SourceJar = Get-ChildItem `
>>     -LiteralPath $Base `
>>     -Recurse `
>>     -File `
>>     -Filter $JarName `
>>     -ErrorAction SilentlyContinue |
>>     Where-Object { $_.FullName -ne $TargetJar } |
>>     Select-Object -First 1
>>
>> if (-not $SourceJar) {
>>     throw "لم أجد $JarName داخل $Base"
>> }
>>
>> Copy-Item -LiteralPath $SourceJar.FullName -Destination $TargetJar -Force
>>
>> if (-not (Test-Path $TargetJar)) {
>>     throw "فشل نسخ Connector إلى $TargetJar"
>> }
>>
>> $Jar = (Resolve-Path $TargetJar).Path
>> Write-Host "Connector installed:" $Jar
>> Get-Item $Jar | Select-Object FullName,Length
>>
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>> $env:PYSPARK_SUBMIT_ARGS = "--jars `"$Jar`" pyspark-shell"
>>
>> Set-Location $Project
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step quality `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 10000
>>
Connector installed: C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\tools\mongo-spark-connector_2.12-10.7.0-all.jar

26/08/24 05:26:49 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 05:26:49 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
duplicate order_id keys: 207689
26/08/24 11:49:19 WARN SparkEnv: Exception while deleting Spark temp dir: E:\spark-tmp\spark-ace1ee43-85f1-4979-a922-d50a92213f3e\userFiles-052a89d9-2a2b-423c-a4bf-7d30d0dce66f
java.io.IOException: Failed to delete: E:\spark-tmp\spark-ace1ee43-85f1-4979-a922-d50a92213f3e\userFiles-052a89d9-2a2b-423c-a4bf-7d30d0dce66f\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:108)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
{
  "raw_classification": {
    "step": "data_quality",
    "mode": "bounded_pyspark_direct_partition_upsert",
    "run_id": "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5",
    "classification_order": "raw_validated_before_raw_quarantine",
    "cleaning_applied": false,
    "partitions": 2,
    "requested_partitions": 2,
    "batch_size": 500,
    "raw_loaded": 10000,
    "raw_valid_count": 7705,
    "raw_invalid_count": 2295,
    "initial_valid_count": 7705,
    "initial_invalid_count": 2295,
    "valid_count": 7705,
    "corrected_count": 0,
    "quarantine_count": 2295,
    "inserted_count": 10000,
    "updated_count": 0,
    "unchanged_count": 0,
    "error_case_counts": {
      "AMBIGUOUS_NEGATIVE_VALUE": 152,
      "UNKNOWN_PRICE": 862,
      "MULTIPLE_CONFLICTING_ERRORS": 109,
      "MISSING_CUSTOMER_ID": 145,
      "INVALID_EMAIL": 137,
      "CORRUPTED_ITEMS_JSON": 136,
      "DUPLICATE_ORDER_ID": 335,
      "INVALID_IMPOSSIBLE_DATE": 325,
      "INVALID_CURRENCY": 64,
      "INVALID_PAYMENT_STATUS": 83,
      "MISSING_ORDER_ID": 81,
      "INVALID_PHONE": 66,
      "INVALID_STATUS": 62,
      "EMPTY_ITEMS": 83
    },
    "elapsed_seconds": 22947.541833,
    "throughput_rows_per_second": 0.44,
    "reconciliation_ok": true,
    "next_stage": "cleaning_after_raw_classification",
    "write_mode": "spark_partition_bounded_mongodb_upsert"
  }
}
26/08/24 11:49:19 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-ace1ee43-85f1-4979-a922-d50a92213f3e
java.io.IOException: Failed to delete: E:\spark-tmp\spark-ace1ee43-85f1-4979-a922-d50a92213f3e\userFiles-052a89d9-2a2b-423c-a4bf-7d30d0dce66f\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 11:49:19 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-ace1ee43-85f1-4979-a922-d50a92213f3e\userFiles-052a89d9-2a2b-423c-a4bf-7d30d0dce66f
java.io.IOException: Failed to delete: E:\spark-tmp\spark-ace1ee43-85f1-4979-a922-d50a92213f3e\userFiles-052a89d9-2a2b-423c-a4bf-7d30d0dce66f\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
FullName                                                                                                     Length
--------                                                                                                     ------
C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\tools\mongo-spark-connector_2.12-10.7.0-all.jar 2567848


SUCCESS: The process with PID 15364 (child process of PID 14680) has been terminated.
SUCCESS: The process with PID 14680 (child process of PID 1428) has been terminated.
SUCCESS: The process with PID 1428 (child process of PID 24344) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -m py_compile src\main.py
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> # حذف نتائج Quality لهذا التشغيل فقط، مع إبقاء orders_raw دون لمس
>> @'
>> from pymongo import MongoClient
>>
>> run_id = "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5"
>> client = MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=10000)
>> db = client["ecommerce_store"]
>>
>> raw_count = db["orders_raw"].count_documents({"run_id": run_id})
>> print("orders_raw before:", raw_count)
>>
>> if raw_count != 30_000_000:
>>     raise RuntimeError("orders_raw ليس 30 مليون؛ تم إيقاف التشغيل")
>>
>> for name in ["orders_validated", "orders_quarantine"]:
>>     result = db[name].delete_many({"run_id": run_id})
>>     print(name, "deleted:", result.deleted_count)
>>
>> result = db["quality_partition_metrics"].delete_many({"run_id": run_id})
>> print("quality_partition_metrics deleted:", result.deleted_count)
>>
>> print("QUALITY TARGET RESET: PASS")
>> client.close()
>> '@ | & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step quality `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 10000
>>
orders_raw before: 30000000
orders_validated deleted: 7705
orders_quarantine deleted: 2295
quality_partition_metrics deleted: 1
QUALITY TARGET RESET: PASS
26/08/24 16:24:42 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 16:24:42 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
duplicate order_id keys: 207689
26/08/24 16:40:10 WARN SparkEnv: Exception while deleting Spark temp dir: E:\spark-tmp\spark-f6afa4ed-99f7-4d5c-a19d-541014408186\userFiles-3b57666b-9153-4097-82d6-e2aa984bea0f
java.io.IOException: Failed to delete: E:\spark-tmp\spark-f6afa4ed-99f7-4d5c-a19d-541014408186\userFiles-3b57666b-9153-4097-82d6-e2aa984bea0f\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:108)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
{
  "raw_classification": {
    "step": "data_quality",
    "mode": "bounded_pyspark_direct_partition_upsert",
    "run_id": "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5",
    "classification_order": "raw_validated_before_raw_quarantine",
    "cleaning_applied": false,
    "partitions": 2,
    "requested_partitions": 2,
    "batch_size": 500,
    "raw_loaded": 10000,
    "raw_valid_count": 7705,
    "raw_invalid_count": 2295,
    "initial_valid_count": 7705,
    "initial_invalid_count": 2295,
    "valid_count": 7705,
    "corrected_count": 0,
    "quarantine_count": 2295,
    "inserted_count": 10000,
    "updated_count": 0,
    "unchanged_count": 0,
    "error_case_counts": {
      "AMBIGUOUS_NEGATIVE_VALUE": 152,
      "UNKNOWN_PRICE": 862,
      "MULTIPLE_CONFLICTING_ERRORS": 109,
      "MISSING_CUSTOMER_ID": 145,
      "INVALID_EMAIL": 137,
      "CORRUPTED_ITEMS_JSON": 136,
      "DUPLICATE_ORDER_ID": 335,
      "INVALID_IMPOSSIBLE_DATE": 325,
      "INVALID_CURRENCY": 64,
      "INVALID_PAYMENT_STATUS": 83,
      "MISSING_ORDER_ID": 81,
      "INVALID_PHONE": 66,
      "INVALID_STATUS": 62,
      "EMPTY_ITEMS": 83
    },
    "elapsed_seconds": 925.211574,
    "throughput_rows_per_second": 10.81,
    "reconciliation_ok": true,
    "next_stage": "cleaning_after_raw_classification",
    "write_mode": "spark_partition_bounded_mongodb_upsert"
  }
}
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> 26/08/24 16:40:11 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-f6afa4ed-99f7-4d5c-a19d-541014408186
java.io.IOException: Failed to delete: E:\spark-tmp\spark-f6afa4ed-99f7-4d5c-a19d-541014408186\userFiles-3b57666b-9153-4097-82d6-e2aa984bea0f\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 16:40:11 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-f6afa4ed-99f7-4d5c-a19d-541014408186\userFiles-3b57666b-9153-4097-82d6-e2aa984bea0f
java.io.IOException: Failed to delete: E:\spark-tmp\spark-f6afa4ed-99f7-4d5c-a19d-541014408186\userFiles-3b57666b-9153-4097-82d6-e2aa984bea0f\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline" has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -m py_compile src\main.py (child process of PID 12640) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -m py_compile src\main.py
>>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> Select-String -Path .\src\main.py -Pattern `
>>   "duplicate_pipeline.append",`
>>   "quality_pipeline.append",`
>>   "spark_partition_bounded_mongodb_upsert"
>>

src\main.py:4646:#             quality_pipeline.append({"$limit": int(limit)})
src\main.py:4770:            duplicate_pipeline.append({"$limit": int(limit)})
src\main.py:4806:        quality_pipeline.append({"$limit": int(limit)})
src\main.py:5043:        "write_mode": "spark_partition_bounded_mongodb_upsert",
src\main.py:5230:        "write_mode": "spark_partition_bounded_mongodb_upsert",


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step quality `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 10000
>>
26/08/24 16:53:59 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 16:54:00 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
{
  "step": "quality",
  "input": null,
  "error_type": "NameError",
  "error_message": "name 'duplicate_ids' is not defined",
  "recovery": "Check the reported resource, path, schema, MongoDB, Java, or Connector requirement; no partial JSON result is treated as successful."
}
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"has been terminated.
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -m py_compile src\main.py
>>                                             ss of PID 15796) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> Select-String -Path .\src\main.py -Pattern `
>>   "duplicate_pipeline",`
>>   "duplicate_ids",`
>>   "duplicate_broadcast",`
>>   "quality_pipeline" |
>>   Select-Object LineNumber,Line
>>

LineNumber Line
---------- ----
      4628 #         duplicate_ids = {str(item["_id"]) for item in duplicate_rows}
      4632 #     print("duplicate order_id keys:", len(duplicate_ids))
      4644 #         quality_pipeline = [{"$match": {"run_id": run_id}}]
      4646 #             quality_pipeline.append({"$limit": int(limit)})
      4654 #             .option("aggregation.pipeline", json.dumps(quality_pipeline))
      4693 #     duplicate_broadcast = spark.sparkContext.broadcast(duplicate_ids)
      4702 #         "duplicate_ids": duplicate_broadcast,
      4759         duplicate_ids = {str(item["_id"]) for item in duplicate_rows}
      4763     print("duplicate order_id keys:", len(duplicate_ids))
      4767     quality_pipeline = [
      4771         quality_pipeline.append({"$limit": int(limit)})
      4781             json.dumps(quality_pipeline),
      4823     duplicate_broadcast = spark.sparkContext.broadcast(duplicate_ids)
      4832         "duplicate_ids": duplicate_broadcast,
      4848         duplicate_ids_local = config["duplicate_ids"].value
      4895                     and str(order_id) in duplicate_ids_local
      4948         duplicate_broadcast.destroy()
      5040         duplicate_ids_local = config["duplicate_ids"].value
      5081                     and str(order_id) in duplicate_ids_local
      5134         duplicate_broadcast.destroy()


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -m py_compile src\main.py
>>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step quality `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 10000
>>
26/08/24 17:03:15 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 17:03:16 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
duplicate order_id keys: 207689
26/08/24 17:15:58 WARN SparkEnv: Exception while deleting Spark temp dir: E:\spark-tmp\spark-1ff4f02c-adf6-4424-b681-353fdf7c27f9\userFiles-a4fe2277-eb71-4c37-945e-0825e498e1f9
java.io.IOException: Failed to delete: E:\spark-tmp\spark-1ff4f02c-adf6-4424-b681-353fdf7c27f9\userFiles-a4fe2277-eb71-4c37-945e-0825e498e1f9\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:108)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
{
  "raw_classification": {
    "step": "data_quality",
    "mode": "bounded_pyspark_direct_partition_upsert",
    "run_id": "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5",
    "classification_order": "raw_validated_before_raw_quarantine",
    "cleaning_applied": false,
    "partitions": 2,
    "requested_partitions": 2,
    "batch_size": 500,
    "raw_loaded": 10000,
    "raw_valid_count": 7705,
    "raw_invalid_count": 2295,
    "initial_valid_count": 7705,
    "initial_invalid_count": 2295,
    "valid_count": 7705,
    "corrected_count": 0,
    "quarantine_count": 2295,
    "inserted_count": 0,
    "updated_count": 7705,
    "unchanged_count": 2295,
    "error_case_counts": {
      "AMBIGUOUS_NEGATIVE_VALUE": 152,
      "UNKNOWN_PRICE": 862,
      "MULTIPLE_CONFLICTING_ERRORS": 109,
      "MISSING_CUSTOMER_ID": 145,
      "INVALID_EMAIL": 137,
      "CORRUPTED_ITEMS_JSON": 136,
      "DUPLICATE_ORDER_ID": 335,
      "INVALID_IMPOSSIBLE_DATE": 325,
      "INVALID_CURRENCY": 64,
      "INVALID_PAYMENT_STATUS": 83,
      "MISSING_ORDER_ID": 81,
      "INVALID_PHONE": 66,
      "INVALID_STATUS": 62,
      "EMPTY_ITEMS": 83
    },
    "elapsed_seconds": 758.196433,
    "throughput_rows_per_second": 13.19,
    "reconciliation_ok": true,
    "next_stage": "cleaning_after_raw_classification",
    "write_mode": "spark_partition_bounded_mongodb_upsert"
  }
}
26/08/24 17:15:59 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-1ff4f02c-adf6-4424-b681-353fdf7c27f9\userFiles-a4fe2277-eb71-4c37-945e-0825e498e1f9
java.io.IOException: Failed to delete: E:\spark-tmp\spark-1ff4f02c-adf6-4424-b681-353fdf7c27f9\userFiles-a4fe2277-eb71-4c37-945e-0825e498e1f9\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 17:15:59 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-1ff4f02c-adf6-4424-b681-353fdf7c27f9
java.io.IOException: Failed to delete: E:\spark-tmp\spark-1ff4f02c-adf6-4424-b681-353fdf7c27f9\userFiles-a4fe2277-eb71-4c37-945e-0825e498e1f9\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> SUCCESS: The process with PID 25508 (child process of PID 24504) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>  has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> Select-String -Path .\src\main.py -Pattern '^def _run_quality_pyspark_dataframe|^def run_quality_pyspark' |
>>     Select-Object LineNumber,Line
>>

LineNumber Line
---------- ----
      4705 def _run_quality_pyspark_dataframe(
      5213 def run_quality_pyspark(


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>> Get-Content .\src\main.py | Select-Object -Skip 4738 -First 55
>>
    try:
        duplicate_rows = probe[database][raw_collection].aggregate(
            [
                {"$match": {"run_id": run_id}},
                {
                    "$group": {
                        "_id": "$order_id",
                        "n": {"$sum": 1},
                    }
                },
                {
                    "$match": {
                        "_id": {"$nin": [None, ""]},
                        "n": {"$gt": 1},
                    }
                },
                {"$project": {"_id": 1}},
            ],
            allowDiskUse=True,
        )
        duplicate_ids = {str(item["_id"]) for item in duplicate_rows}
    finally:
        probe.close()

    print("duplicate order_id keys:", len(duplicate_ids))

    # IMPORTANT: put $limit inside MongoDB's aggregation pipeline. The second
    # DataFrame-side limit below remains as a safety guard.
    quality_pipeline = [
        {"$match": {"run_id": run_id}},
    ]
    if limit:
        quality_pipeline.append({"$limit": int(limit)})

    reader = (
        spark.read
        .format("mongodb")
        .option("connection.uri", mongo_uri)
        .option("database", database)
        .option("collection", raw_collection)
        .option(
            "aggregation.pipeline",
            json.dumps(quality_pipeline),
        )
    )

    # A bounded smoke test must use one connector partition so the limit is
    # global rather than independently applied by several partitions.
    if limit:
        reader = reader.option(
            "partitioner",
            "com.mongodb.spark.sql.connector.read.partitioner.SinglePartitionPartitioner",
        )

    raw = reader.load().drop("_id")
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -m py_compile src\main.py
>>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step quality `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 10000
>>
26/08/24 17:25:28 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 17:25:29 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
duplicate order_id keys: 83
26/08/24 17:25:47 WARN SparkEnv: Exception while deleting Spark temp dir: E:\spark-tmp\spark-48ea4edc-8017-4fb5-a585-27c1977d2a62\userFiles-a7453cf2-3b6a-44d6-9964-8f884bd9a5bd
java.io.IOException: Failed to delete: E:\spark-tmp\spark-48ea4edc-8017-4fb5-a585-27c1977d2a62\userFiles-a7453cf2-3b6a-44d6-9964-8f884bd9a5bd\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:108)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
{
  "raw_classification": {
    "step": "data_quality",
    "mode": "bounded_pyspark_direct_partition_upsert",
    "run_id": "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5",
    "classification_order": "raw_validated_before_raw_quarantine",
    "cleaning_applied": false,
    "partitions": 2,
    "requested_partitions": 2,
    "batch_size": 500,
    "raw_loaded": 10000,
    "raw_valid_count": 7841,
    "raw_invalid_count": 2159,
    "initial_valid_count": 7841,
    "initial_invalid_count": 2159,
    "valid_count": 7841,
    "corrected_count": 0,
    "quarantine_count": 2159,
    "inserted_count": 136,
    "updated_count": 7737,
    "unchanged_count": 2127,
    "error_case_counts": {
      "AMBIGUOUS_NEGATIVE_VALUE": 152,
      "UNKNOWN_PRICE": 862,
      "MULTIPLE_CONFLICTING_ERRORS": 78,
      "MISSING_CUSTOMER_ID": 145,
      "INVALID_EMAIL": 137,
      "CORRUPTED_ITEMS_JSON": 136,
      "DUPLICATE_ORDER_ID": 167,
      "INVALID_IMPOSSIBLE_DATE": 325,
      "INVALID_CURRENCY": 64,
      "INVALID_PAYMENT_STATUS": 83,
      "MISSING_ORDER_ID": 81,
      "INVALID_PHONE": 66,
      "INVALID_STATUS": 62,
      "EMPTY_ITEMS": 83
    },
    "elapsed_seconds": 15.103811,
    "throughput_rows_per_second": 662.08,
    "reconciliation_ok": true,
    "next_stage": "cleaning_after_raw_classification",
    "write_mode": "spark_partition_bounded_mongodb_upsert"
  }
}
26/08/24 17:25:48 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-48ea4edc-8017-4fb5-a585-27c1977d2a62
java.io.IOException: Failed to delete: E:\spark-tmp\spark-48ea4edc-8017-4fb5-a585-27c1977d2a62\userFiles-a7453cf2-3b6a-44d6-9964-8f884bd9a5bd\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 17:25:48 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-48ea4edc-8017-4fb5-a585-27c1977d2a62\userFiles-a7453cf2-3b6a-44d6-9964-8f884bd9a5bd
java.io.IOException: Failed to delete: E:\spark-tmp\spark-48ea4edc-8017-4fb5-a585-27c1977d2a62\userFiles-a7453cf2-3b6a-44d6-9964-8f884bd9a5bd\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"4544 (child process of PID 18544) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> # التأكد من أن القرص E لديه مساحة مناسبة قبل التشغيل
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> Get-PSDrive E | Select-Object Name,
>>     @{Name="FreeGB";Expression={[math]::Round($_.Free / 1GB, 2)}}

Name FreeGB
---- ------
E      24.6


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:SPARK_LOCAL_IP = "127.0.0.1"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> # تصفير مخرجات Quality لهذا run_id فقط؛ orders_raw لا يُلمس
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> @'
>> from pymongo import MongoClient
>>
>> run_id = "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5"
>> client = MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=10000)
>> db = client["ecommerce_store"]
>>
>> raw_count = db["orders_raw"].count_documents({"run_id": run_id})
>> print("orders_raw:", raw_count)
>> if raw_count != 30_000_000:
>>     raise RuntimeError("orders_raw ليس 30 مليونًا؛ تم إيقاف التشغيل")
>>
>> for name in ["orders_validated", "orders_quarantine"]:
>>     result = db[name].delete_many({"run_id": run_id})
>>     print(name, "deleted:", result.deleted_count)
>>
>> result = db["quality_partition_metrics"].delete_many({"run_id": run_id})
>> print("quality_partition_metrics deleted:", result.deleted_count)
>> print("FULL QUALITY TARGET RESET: PASS")
>> client.close()
>> '@ | & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -
orders_raw: 30000000
orders_validated deleted: 7841
orders_quarantine deleted: 2295
quality_partition_metrics deleted: 1
FULL QUALITY TARGET RESET: PASS
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> # Quality الكامل: limit=0 يعني كل 30 مليون سجل
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step quality `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 0
26/08/24 17:28:00 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 17:28:00 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
duplicate order_id keys: 207689
26/08/24 20:42:17 WARN SparkEnv: Exception while deleting Spark temp dir: E:\spark-tmp\spark-d3cf5896-8c60-4bdc-9d8d-68d54170b714\userFiles-8b2051b9-c26e-492d-b2c5-33c5a54326d0
java.io.IOException: Failed to delete: E:\spark-tmp\spark-d3cf5896-8c60-4bdc-9d8d-68d54170b714\userFiles-8b2051b9-c26e-492d-b2c5-33c5a54326d0\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:108)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
{
  "raw_classification": {
    "step": "data_quality",
    "mode": "full_pyspark_direct_partition_upsert",
    "run_id": "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5",
    "classification_order": "raw_validated_before_raw_quarantine",
    "cleaning_applied": false,
    "partitions": 2,
    "requested_partitions": 2,
    "batch_size": 500,
    "raw_loaded": 30000000,
    "raw_valid_count": 23664580,
    "raw_invalid_count": 6335420,
    "initial_valid_count": 23664580,
    "initial_invalid_count": 6335420,
    "valid_count": 23664580,
    "corrected_count": 0,
    "quarantine_count": 6335420,
    "inserted_count": 30000000,
    "updated_count": 0,
    "unchanged_count": 0,
    "error_case_counts": {
      "AMBIGUOUS_NEGATIVE_VALUE": 419135,
      "UNKNOWN_PRICE": 2757819,
      "DUPLICATE_ORDER_ID": 417584,
      "INVALID_IMPOSSIBLE_DATE": 878675,
      "MULTIPLE_CONFLICTING_ERRORS": 248008,
      "MISSING_CUSTOMER_ID": 419474,
      "INVALID_EMAIL": 418709,
      "CORRUPTED_ITEMS_JSON": 419906,
      "MISSING_ORDER_ID": 209392,
      "EMPTY_ITEMS": 209934,
      "INVALID_STATUS": 210194,
      "INVALID_CURRENCY": 210190,
      "INVALID_PHONE": 210042,
      "INVALID_PAYMENT_STATUS": 222692
    },
    "elapsed_seconds": 11654.803943,
    "throughput_rows_per_second": 2574.05,
    "reconciliation_ok": true,
    "next_stage": "cleaning_after_raw_classification",
    "write_mode": "spark_partition_bounded_mongodb_upsert"
  }
}
26/08/24 20:42:18 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-d3cf5896-8c60-4bdc-9d8d-68d54170b714
java.io.IOException: Failed to delete: E:\spark-tmp\spark-d3cf5896-8c60-4bdc-9d8d-68d54170b714\userFiles-8b2051b9-c26e-492d-b2c5-33c5a54326d0\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 20:42:18 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-d3cf5896-8c60-4bdc-9d8d-68d54170b714\userFiles-8b2051b9-c26e-492d-b2c5-33c5a54326d0
java.io.IOException: Failed to delete: E:\spark-tmp\spark-d3cf5896-8c60-4bdc-9d8d-68d54170b714\userFiles-8b2051b9-c26e-492d-b2c5-33c5a54326d0\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> SUCCESS: The process with PID 24796 (child process of PID 14452) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>  has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>  has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> @'
>> from pymongo import MongoClient
>>
>> run_id = "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5"
>> client = MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=10000)
>> db = client["ecommerce_store"]
>>
>> for name in ["orders_raw", "orders_validated", "orders_quarantine"]:
>>     print(name, db[name].count_documents({"run_id": run_id}))
>>
>> print("metrics:", db["quality_partition_metrics"].count_documents({"run_id": run_id}))
>> client.close()
>> '@ | & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -
>>
orders_raw 30000000
orders_validated 23664580
orders_quarantine 6335420
metrics: 1
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -m py_compile src\main.py
>>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -m py_compile src\main.py
>>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step cleaning `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 0
>>
26/08/24 21:02:42 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 21:02:43 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
26/08/24 21:12:28 ERROR Executor: Exception in task 0.0 in stage 2.0 (TID 338)2]
org.apache.spark.api.python.PythonException: Traceback (most recent call last):
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 456, in receive_message
    return receive_message(self, request_id, self.max_message_size)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\network_layer.py", line 759, in receive_message
    length, _, response_to, op_code = _UNPACK_HEADER(receive_data(conn, 16, deadline))
                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\network_layer.py", line 353, in receive_data
    chunk_length = conn.conn.recv_into(mv[bytes_read:])
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\network_layer.py", line 469, in recv_into
    return self.conn.recv_into(buffer)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip\pyspark\worker.py", line 1247, in main
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip\pyspark\worker.py", line 1237, in process
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 840, in func
    return f(iterator)
           ^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 1795, in func
    r = f(it)
        ^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 5708, in <lambda>
    lambda rows: _write_quarantine_cleaning_partition(rows, config)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 4565, in _write_quarantine_cleaning_partition
    counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 4346, in _bulk_upsert_quarantine
    result = collection.bulk_write(operations, ordered=False)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\collection.py", line 790, in bulk_write
    bulk_api_result = blk.execute(write_concern, session, _Op.INSERT)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 751, in execute
    return self.execute_command(generator, write_concern, session, operation)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 604, in execute_command
    _ = client._retryable_write(
        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2113, in _retryable_write
    return self._retry_with_session(retryable, func, s, bulk, operation, operation_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 1986, in _retry_with_session
    return self._retry_internal(
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2038, in _retry_internal
    ).run()
      ^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2811, in run
    res = self._read() if self._is_read else self._write()
                                             ^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 3014, in _write
    return self._func(self._session, conn, self._retryable)  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 593, in retryable_bulk
    self._execute_command(
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 538, in _execute_command
    result, to_send = self._execute_batch(bwc, cmd, ops, client)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 462, in _execute_batch
    result = self.write_command(bwc, cmd, request_id, msg, to_send, client)  # type: ignore[arg-type]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\helpers.py", line 53, in inner
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 274, in write_command
    reply = bwc.conn.write_command(request_id, msg, bwc.codec)  # type: ignore[misc]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 491, in write_command
    reply = self.receive_message(request_id)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 459, in receive_message
    self._raise_connection_failure(error)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 633, in _raise_connection_failure
    _raise_connection_failure(self.address, error, timeout_details=details)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\pool_shared.py", line 148, in _raise_connection_failure
    raise AutoReconnect(msg) from error
pymongo.errors.AutoReconnect: 127.0.0.1:27017: [WinError 10054] An existing connection was forcibly closed by the remote host (configured timeouts: connectTimeoutMS: 20000.0ms)

        at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:572)
        at org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:784)
        at org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:766)
        at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:525)
        at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
        at scala.collection.Iterator.foreach(Iterator.scala:943)
        at scala.collection.Iterator.foreach$(Iterator.scala:943)
        at org.apache.spark.InterruptibleIterator.foreach(InterruptibleIterator.scala:28)
        at scala.collection.generic.Growable.$plus$plus$eq(Growable.scala:62)
        at scala.collection.generic.Growable.$plus$plus$eq$(Growable.scala:53)
        at scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:105)
        at scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:49)
        at scala.collection.TraversableOnce.to(TraversableOnce.scala:366)
        at scala.collection.TraversableOnce.to$(TraversableOnce.scala:364)
        at org.apache.spark.InterruptibleIterator.to(InterruptibleIterator.scala:28)
        at scala.collection.TraversableOnce.toBuffer(TraversableOnce.scala:358)
        at scala.collection.TraversableOnce.toBuffer$(TraversableOnce.scala:358)
        at org.apache.spark.InterruptibleIterator.toBuffer(InterruptibleIterator.scala:28)
        at scala.collection.TraversableOnce.toArray(TraversableOnce.scala:345)
        at scala.collection.TraversableOnce.toArray$(TraversableOnce.scala:339)
        at org.apache.spark.InterruptibleIterator.toArray(InterruptibleIterator.scala:28)
        at org.apache.spark.rdd.RDD.$anonfun$collect$2(RDD.scala:1049)
        at org.apache.spark.SparkContext.$anonfun$runJob$5(SparkContext.scala:2433)
        at org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)
        at org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)
        at org.apache.spark.scheduler.Task.run(Task.scala:141)
        at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)
        at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)
        at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 21:12:28 WARN TaskSetManager: Lost task 0.0 in stage 2.0 (TID 338) (127.0.0.1 executor driver): org.apache.spark.api.python.PythonException: Traceback (most recent call last):
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 456, in receive_message
    return receive_message(self, request_id, self.max_message_size)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\network_layer.py", line 759, in receive_message
    length, _, response_to, op_code = _UNPACK_HEADER(receive_data(conn, 16, deadline))
                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\network_layer.py", line 353, in receive_data
    chunk_length = conn.conn.recv_into(mv[bytes_read:])
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\network_layer.py", line 469, in recv_into
    return self.conn.recv_into(buffer)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip\pyspark\worker.py", line 1247, in main
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip\pyspark\worker.py", line 1237, in process
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 840, in func
    return f(iterator)
           ^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 1795, in func
    r = f(it)
        ^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 5708, in <lambda>
    lambda rows: _write_quarantine_cleaning_partition(rows, config)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 4565, in _write_quarantine_cleaning_partition
    counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 4346, in _bulk_upsert_quarantine
    result = collection.bulk_write(operations, ordered=False)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\collection.py", line 790, in bulk_write
    bulk_api_result = blk.execute(write_concern, session, _Op.INSERT)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 751, in execute
    return self.execute_command(generator, write_concern, session, operation)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 604, in execute_command
    _ = client._retryable_write(
        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2113, in _retryable_write
    return self._retry_with_session(retryable, func, s, bulk, operation, operation_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 1986, in _retry_with_session
    return self._retry_internal(
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2038, in _retry_internal
    ).run()
      ^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2811, in run
    res = self._read() if self._is_read else self._write()
                                             ^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 3014, in _write
    return self._func(self._session, conn, self._retryable)  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 593, in retryable_bulk
    self._execute_command(
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 538, in _execute_command
    result, to_send = self._execute_batch(bwc, cmd, ops, client)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 462, in _execute_batch
    result = self.write_command(bwc, cmd, request_id, msg, to_send, client)  # type: ignore[arg-type]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\helpers.py", line 53, in inner
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 274, in write_command
    reply = bwc.conn.write_command(request_id, msg, bwc.codec)  # type: ignore[misc]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 491, in write_command
    reply = self.receive_message(request_id)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 459, in receive_message
    self._raise_connection_failure(error)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 633, in _raise_connection_failure
    _raise_connection_failure(self.address, error, timeout_details=details)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\pool_shared.py", line 148, in _raise_connection_failure
    raise AutoReconnect(msg) from error
pymongo.errors.AutoReconnect: 127.0.0.1:27017: [WinError 10054] An existing connection was forcibly closed by the remote host (configured timeouts: connectTimeoutMS: 20000.0ms)

        at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:572)
        at org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:784)
        at org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:766)
        at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:525)
        at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
        at scala.collection.Iterator.foreach(Iterator.scala:943)
        at scala.collection.Iterator.foreach$(Iterator.scala:943)
        at org.apache.spark.InterruptibleIterator.foreach(InterruptibleIterator.scala:28)
        at scala.collection.generic.Growable.$plus$plus$eq(Growable.scala:62)
        at scala.collection.generic.Growable.$plus$plus$eq$(Growable.scala:53)
        at scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:105)
        at scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:49)
        at scala.collection.TraversableOnce.to(TraversableOnce.scala:366)
        at scala.collection.TraversableOnce.to$(TraversableOnce.scala:364)
        at org.apache.spark.InterruptibleIterator.to(InterruptibleIterator.scala:28)
        at scala.collection.TraversableOnce.toBuffer(TraversableOnce.scala:358)
        at scala.collection.TraversableOnce.toBuffer$(TraversableOnce.scala:358)
        at org.apache.spark.InterruptibleIterator.toBuffer(InterruptibleIterator.scala:28)
        at scala.collection.TraversableOnce.toArray(TraversableOnce.scala:345)
        at scala.collection.TraversableOnce.toArray$(TraversableOnce.scala:339)
        at org.apache.spark.InterruptibleIterator.toArray(InterruptibleIterator.scala:28)
        at org.apache.spark.rdd.RDD.$anonfun$collect$2(RDD.scala:1049)
        at org.apache.spark.SparkContext.$anonfun$runJob$5(SparkContext.scala:2433)
        at org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)
        at org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)
        at org.apache.spark.scheduler.Task.run(Task.scala:141)
        at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)
        at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)
        at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)

26/08/24 21:12:28 ERROR TaskSetManager: Task 0 in stage 2.0 failed 1 times; aborting job
26/08/24 21:12:29 ERROR DiskBlockManager: Exception while deleting local spark dir: E:\spark-tmp\blockmgr-7ba620a1-6fc8-4fda-9d4a-1702cc641b0c
java.io.IOException: Failed to delete: E:\spark-tmp\blockmgr-7ba620a1-6fc8-4fda-9d4a-1702cc641b0c\31\shuffle_0_12_0.data
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.storage.DiskBlockManager.$anonfun$doStop$1(DiskBlockManager.scala:368)
        at org.apache.spark.storage.DiskBlockManager.$anonfun$doStop$1$adapted(DiskBlockManager.scala:364)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.storage.DiskBlockManager.doStop(DiskBlockManager.scala:364)
        at org.apache.spark.storage.DiskBlockManager.stop(DiskBlockManager.scala:359)
        at org.apache.spark.storage.BlockManager.stop(BlockManager.scala:2120)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:95)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 21:12:29 WARN SparkEnv: Exception while deleting Spark temp dir: E:\spark-tmp\spark-1940f0b1-e4ab-48a3-85a4-d1438f2426e7\userFiles-fd126904-6ccf-4d9f-bf0a-e7d7de8dd4c6
java.io.IOException: Failed to delete: E:\spark-tmp\spark-1940f0b1-e4ab-48a3-85a4-d1438f2426e7\userFiles-fd126904-6ccf-4d9f-bf0a-e7d7de8dd4c6\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:108)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
{
  "step": "cleaning",
  "input": null,
  "error_type": "Py4JJavaError",
  "error_message": "An error occurred while calling z:org.apache.spark.api.python.PythonRDD.collectAndServe.\n: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 2.0 failed 1 times, most recent failure: Lost task 0.0 in stage 2.0 (TID 338) (127.0.0.1 executor driver): org.apache.spark.api.python.PythonException: Traceback (most recent call last):\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 456, in receive_message\n    return receive_message(self, request_id, self.max_message_size)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\network_layer.py\", line 759, in receive_message\n    length, _, response_to, op_code = _UNPACK_HEADER(receive_data(conn, 16, deadline))\n                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\network_layer.py\", line 353, in receive_data\n    chunk_length = conn.conn.recv_into(mv[bytes_read:])\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\network_layer.py\", line 469, in recv_into\n    return self.conn.recv_into(buffer)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\nConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\python\\lib\\pyspark.zip\\pyspark\\worker.py\", line 1247, in main\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\python\\lib\\pyspark.zip\\pyspark\\worker.py\", line 1237, in process\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 840, in func\n    return f(iterator)\n           ^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 1795, in func\n    r = f(it)\n        ^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 5708, in <lambda>\n    lambda rows: _write_quarantine_cleaning_partition(rows, config)\n                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 4565, in _write_quarantine_cleaning_partition\n    counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))\n                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 4346, in _bulk_upsert_quarantine\n    result = collection.bulk_write(operations, ordered=False)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\_csot.py\", line 125, in csot_wrapper\n    return func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\collection.py\", line 790, in bulk_write\n    bulk_api_result = blk.execute(write_concern, session, _Op.INSERT)\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 751, in execute\n    return self.execute_command(generator, write_concern, session, operation)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 604, in execute_command\n    _ = client._retryable_write(\n        ^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2113, in _retryable_write\n    return self._retry_with_session(retryable, func, s, bulk, operation, operation_id)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 1986, in _retry_with_session\n    return self._retry_internal(\n           ^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\_csot.py\", line 125, in csot_wrapper\n    return func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2038, in _retry_internal\n    ).run()\n      ^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2811, in run\n    res = self._read() if self._is_read else self._write()\n                                             ^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 3014, in _write\n    return self._func(self._session, conn, self._retryable)  # type: ignore\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 593, in retryable_bulk\n    self._execute_command(\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 538, in _execute_command\n    result, to_send = self._execute_batch(bwc, cmd, ops, client)\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 462, in _execute_batch\n    result = self.write_command(bwc, cmd, request_id, msg, to_send, client)  # type: ignore[arg-type]\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\helpers.py\", line 53, in inner\n    return func(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 274, in write_command\n    reply = bwc.conn.write_command(request_id, msg, bwc.codec)  # type: ignore[misc]\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 491, in write_command\n    reply = self.receive_message(request_id)\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 459, in receive_message\n    self._raise_connection_failure(error)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 633, in _raise_connection_failure\n    _raise_connection_failure(self.address, error, timeout_details=details)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\pool_shared.py\", line 148, in _raise_connection_failure\n    raise AutoReconnect(msg) from error\npymongo.errors.AutoReconnect: 127.0.0.1:27017: [WinError 10054] An existing connection was forcibly closed by the remote host (configured timeouts: connectTimeoutMS: 20000.0ms)\n\r\n\tat org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:572)\r\n\tat org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:784)\r\n\tat org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:766)\r\n\tat org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:525)\r\n\tat org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)\r\n\tat scala.collection.Iterator.foreach(Iterator.scala:943)\r\n\tat scala.collection.Iterator.foreach$(Iterator.scala:943)\r\n\tat org.apache.spark.InterruptibleIterator.foreach(InterruptibleIterator.scala:28)\r\n\tat scala.collection.generic.Growable.$plus$plus$eq(Growable.scala:62)\r\n\tat scala.collection.generic.Growable.$plus$plus$eq$(Growable.scala:53)\r\n\tat scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:105)\r\n\tat scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:49)\r\n\tat scala.collection.TraversableOnce.to(TraversableOnce.scala:366)\r\n\tat scala.collection.TraversableOnce.to$(TraversableOnce.scala:364)\r\n\tat org.apache.spark.InterruptibleIterator.to(InterruptibleIterator.scala:28)\r\n\tat scala.collection.TraversableOnce.toBuffer(TraversableOnce.scala:358)\r\n\tat scala.collection.TraversableOnce.toBuffer$(TraversableOnce.scala:358)\r\n\tat org.apache.spark.InterruptibleIterator.toBuffer(InterruptibleIterator.scala:28)\r\n\tat scala.collection.TraversableOnce.toArray(TraversableOnce.scala:345)\r\n\tat scala.collection.TraversableOnce.toArray$(TraversableOnce.scala:339)\r\n\tat org.apache.spark.InterruptibleIterator.toArray(InterruptibleIterator.scala:28)\r\n\tat org.apache.spark.rdd.RDD.$anonfun$collect$2(RDD.scala:1049)\r\n\tat org.apache.spark.SparkContext.$anonfun$runJob$5(SparkContext.scala:2433)\r\n\tat org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)\r\n\tat org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)\r\n\tat org.apache.spark.scheduler.Task.run(Task.scala:141)\r\n\tat org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)\r\n\tat org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)\r\n\tat org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)\r\n\tat org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)\r\n\tat org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)\r\n\tat java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)\r\n\tat java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)\r\n\tat java.base/java.lang.Thread.run(Thread.java:842)\r\n\nDriver stacktrace:\r\n\tat org.apache.spark.scheduler.DAGScheduler.failJobAndIndependentStages(DAGScheduler.scala:2856)\r\n\tat org.apache.spark.scheduler.DAGScheduler.$anonfun$abortStage$2(DAGScheduler.scala:2792)\r\n\tat org.apache.spark.scheduler.DAGScheduler.$anonfun$abortStage$2$adapted(DAGScheduler.scala:2791)\r\n\tat scala.collection.mutable.ResizableArray.foreach(ResizableArray.scala:62)\r\n\tat scala.collection.mutable.ResizableArray.foreach$(ResizableArray.scala:55)\r\n\tat scala.collection.mutable.ArrayBuffer.foreach(ArrayBuffer.scala:49)\r\n\tat org.apache.spark.scheduler.DAGScheduler.abortStage(DAGScheduler.scala:2791)\r\n\tat org.apache.spark.scheduler.DAGScheduler.$anonfun$handleTaskSetFailed$1(DAGScheduler.scala:1247)\r\n\tat org.apache.spark.scheduler.DAGScheduler.$anonfun$handleTaskSetFailed$1$adapted(DAGScheduler.scala:1247)\r\n\tat scala.Option.foreach(Option.scala:407)\r\n\tat org.apache.spark.scheduler.DAGScheduler.handleTaskSetFailed(DAGScheduler.scala:1247)\r\n\tat org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.doOnReceive(DAGScheduler.scala:3060)\r\n\tat org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:2994)\r\n\tat org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:2983)\r\n\tat org.apache.spark.util.EventLoop$$anon$1.run(EventLoop.scala:49)\r\n\tat org.apache.spark.scheduler.DAGScheduler.runJob(DAGScheduler.scala:989)\r\n\tat org.apache.spark.SparkContext.runJob(SparkContext.scala:2393)\r\n\tat org.apache.spark.SparkContext.runJob(SparkContext.scala:2414)\r\n\tat org.apache.spark.SparkContext.runJob(SparkContext.scala:2433)\r\n\tat org.apache.spark.SparkContext.runJob(SparkContext.scala:2458)\r\n\tat org.apache.spark.rdd.RDD.$anonfun$collect$1(RDD.scala:1049)\r\n\tat org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:151)\r\n\tat org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:112)\r\n\tat org.apache.spark.rdd.RDD.withScope(RDD.scala:410)\r\n\tat org.apache.spark.rdd.RDD.collect(RDD.scala:1048)\r\n\tat org.apache.spark.api.python.PythonRDD$.collectAndServe(PythonRDD.scala:195)\r\n\tat org.apache.spark.api.python.PythonRDD.collectAndServe(PythonRDD.scala)\r\n\tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)\r\n\tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)\r\n\tat java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\r\n\tat java.base/java.lang.reflect.Method.invoke(Method.java:568)\r\n\tat py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)\r\n\tat py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)\r\n\tat py4j.Gateway.invoke(Gateway.java:282)\r\n\tat py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)\r\n\tat py4j.commands.CallCommand.execute(CallCommand.java:79)\r\n\tat py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)\r\n\tat py4j.ClientServerConnection.run(ClientServerConnection.java:106)\r\n\tat java.base/java.lang.Thread.run(Thread.java:842)\r\nCaused by: org.apache.spark.api.python.PythonException: Traceback (most recent call last):\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 456, in receive_message\n    return receive_message(self, request_id, self.max_message_size)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\network_layer.py\", line 759, in receive_message\n    length, _, response_to, op_code = _UNPACK_HEADER(receive_data(conn, 16, deadline))\n                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\network_layer.py\", line 353, in receive_data\n    chunk_length = conn.conn.recv_into(mv[bytes_read:])\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\network_layer.py\", line 469, in recv_into\n    return self.conn.recv_into(buffer)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\nConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\python\\lib\\pyspark.zip\\pyspark\\worker.py\", line 1247, in main\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\python\\lib\\pyspark.zip\\pyspark\\worker.py\", line 1237, in process\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 840, in func\n    return f(iterator)\n           ^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 1795, in func\n    r = f(it)\n        ^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 5708, in <lambda>\n    lambda rows: _write_quarantine_cleaning_partition(rows, config)\n                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 4565, in _write_quarantine_cleaning_partition\n    counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))\n                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 4346, in _bulk_upsert_quarantine\n    result = collection.bulk_write(operations, ordered=False)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\_csot.py\", line 125, in csot_wrapper\n    return func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\collection.py\", line 790, in bulk_write\n    bulk_api_result = blk.execute(write_concern, session, _Op.INSERT)\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 751, in execute\n    return self.execute_command(generator, write_concern, session, operation)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 604, in execute_command\n    _ = client._retryable_write(\n        ^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2113, in _retryable_write\n    return self._retry_with_session(retryable, func, s, bulk, operation, operation_id)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 1986, in _retry_with_session\n    return self._retry_internal(\n           ^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\_csot.py\", line 125, in csot_wrapper\n    return func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2038, in _retry_internal\n    ).run()\n      ^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2811, in run\n    res = self._read() if self._is_read else self._write()\n                                             ^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 3014, in _write\n    return self._func(self._session, conn, self._retryable)  # type: ignore\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 593, in retryable_bulk\n    self._execute_command(\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 538, in _execute_command\n    result, to_send = self._execute_batch(bwc, cmd, ops, client)\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 462, in _execute_batch\n    result = self.write_command(bwc, cmd, request_id, msg, to_send, client)  # type: ignore[arg-type]\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\helpers.py\", line 53, in inner\n    return func(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 274, in write_command\n    reply = bwc.conn.write_command(request_id, msg, bwc.codec)  # type: ignore[misc]\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 491, in write_command\n    reply = self.receive_message(request_id)\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 459, in receive_message\n    self._raise_connection_failure(error)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 633, in _raise_connection_failure\n    _raise_connection_failure(self.address, error, timeout_details=details)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\pool_shared.py\", line 148, in _raise_connection_failure\n    raise AutoReconnect(msg) from error\npymongo.errors.AutoReconnect: 127.0.0.1:27017: [WinError 10054] An existing connection was forcibly closed by the remote host (configured timeouts: connectTimeoutMS: 20000.0ms)\n\r\n\tat org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:572)\r\n\tat org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:784)\r\n\tat org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:766)\r\n\tat org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:525)\r\n\tat org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)\r\n\tat scala.collection.Iterator.foreach(Iterator.scala:943)\r\n\tat scala.collection.Iterator.foreach$(Iterator.scala:943)\r\n\tat org.apache.spark.InterruptibleIterator.foreach(InterruptibleIterator.scala:28)\r\n\tat scala.collection.generic.Growable.$plus$plus$eq(Growable.scala:62)\r\n\tat scala.collection.generic.Growable.$plus$plus$eq$(Growable.scala:53)\r\n\tat scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:105)\r\n\tat scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:49)\r\n\tat scala.collection.TraversableOnce.to(TraversableOnce.scala:366)\r\n\tat scala.collection.TraversableOnce.to$(TraversableOnce.scala:364)\r\n\tat org.apache.spark.InterruptibleIterator.to(InterruptibleIterator.scala:28)\r\n\tat scala.collection.TraversableOnce.toBuffer(TraversableOnce.scala:358)\r\n\tat scala.collection.TraversableOnce.toBuffer$(TraversableOnce.scala:358)\r\n\tat org.apache.spark.InterruptibleIterator.toBuffer(InterruptibleIterator.scala:28)\r\n\tat scala.collection.TraversableOnce.toArray(TraversableOnce.scala:345)\r\n\tat scala.collection.TraversableOnce.toArray$(TraversableOnce.scala:339)\r\n\tat org.apache.spark.InterruptibleIterator.toArray(InterruptibleIterator.scala:28)\r\n\tat org.apache.spark.rdd.RDD.$anonfun$collect$2(RDD.scala:1049)\r\n\tat org.apache.spark.SparkContext.$anonfun$runJob$5(SparkContext.scala:2433)\r\n\tat org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)\r\n\tat org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)\r\n\tat org.apache.spark.scheduler.Task.run(Task.scala:141)\r\n\tat org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)\r\n\tat org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)\r\n\tat org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)\r\n\tat org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)\r\n\tat org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)\r\n\tat java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)\r\n\tat java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)\r\n\t... 1 more\r\n",
  "recovery": "Check the reported resource, path, schema, MongoDB, Java, or Connector requirement; no partial JSON result is treated as successful."
}
26/08/24 21:12:29 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-1940f0b1-e4ab-48a3-85a4-d1438f2426e7\userFiles-fd126904-6ccf-4d9f-bf0a-e7d7de8dd4c6
java.io.IOException: Failed to delete: E:\spark-tmp\spark-1940f0b1-e4ab-48a3-85a4-d1438f2426e7\userFiles-fd126904-6ccf-4d9f-bf0a-e7d7de8dd4c6\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 21:12:29 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-1940f0b1-e4ab-48a3-85a4-d1438f2426e7
java.io.IOException: Failed to delete: E:\spark-tmp\spark-1940f0b1-e4ab-48a3-85a4-d1438f2426e7\userFiles-fd126904-6ccf-4d9f-bf0a-e7d7de8dd4c6\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"876 (child process of PID 8556) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:SPARK_LOCAL_IP = "127.0.0.1"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step cleaning `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 0
26/08/24 21:15:33 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 21:15:34 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
{
  "step": "cleaning",
  "input": null,
  "error_type": "ServerSelectionTimeoutError",
  "error_message": "127.0.0.1:27017: [WinError 10061] No connection could be made because the target machine actively refused it (configured timeouts: socketTimeoutMS: 20000.0ms, connectTimeoutMS: 20000.0ms), Timeout: 10.0s, Topology Description: <TopologyDescription id: 6a8c8a48ecd4d84221b497ca, topology_type: Unknown, servers: [<ServerDescription ('127.0.0.1', 27017) server_type: Unknown, rtt: None, error=AutoReconnect('127.0.0.1:27017: [WinError 10061] No connection could be made because the target machine actively refused it (configured timeouts: socketTimeoutMS: 20000.0ms, connectTimeoutMS: 20000.0ms)')>]>",
  "recovery": "Check the reported resource, path, schema, MongoDB, Java, or Connector requirement; no partial JSON result is treated as successful."
}
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> SUCCESS: The process with PID 9332 (child process of PID 8308) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>  has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> $MongoBin = "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
>> $DataPath = "E:\mongodb-project-data"
>> $LogPath = "E:\mongodb-project-log"
>>
>> if (-not (Test-Path $MongoBin)) {
>>     throw "mongod.exe غير موجود: $MongoBin"
>> }
>> if (-not (Test-Path $DataPath)) {
>>     throw "مسار بيانات MongoDB غير موجود: $DataPath"
>> }
>>
>> New-Item -ItemType Directory -Force -Path $LogPath | Out-Null
>>
>> $MongoProcess = Get-Process mongod -ErrorAction SilentlyContinue
>> if ($MongoProcess) {
>>     Write-Host "MongoDB process already exists. PID:" $MongoProcess.Id
>> } else {
>>     Start-Process `
>>       -FilePath $MongoBin `
>>       -ArgumentList @(
>>         "--dbpath", $DataPath,
>>         "--logpath", (Join-Path $LogPath "mongod.log"),
>>         "--logappend",
>>         "--bind_ip", "127.0.0.1",
>>         "--port", "27017"
>>       ) `
>>       -WindowStyle Hidden
>>     Write-Host "MongoDB start command sent"
>> }
>>
>> Start-Sleep -Seconds 8
>>
>> @'
>> from pymongo import MongoClient
>>
>> run_id = "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5"
>> client = MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=10000)
>> client.admin.command("ping")
>> db = client["ecommerce_store"]
>>
>> print("MongoDB: PASS")
>> print("orders_raw:", db["orders_raw"].count_documents({"run_id": run_id}))
>> print("orders_validated:", db["orders_validated"].count_documents({"run_id": run_id}))
>> print("orders_quarantine:", db["orders_quarantine"].count_documents({"run_id": run_id}))
>> print("quality metrics:", db["quality_partition_metrics"].count_documents({"run_id": run_id}))
>> client.close()
>> '@ | & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -
>>
MongoDB start command sent
MongoDB: PASS
orders_raw: 30000000
orders_validated: 23664580
orders_quarantine: 6335420
quality metrics: 1
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step cleaning `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 0
26/08/24 21:26:47 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 21:26:47 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
26/08/24 21:49:57 ERROR Executor: Exception in task 0.0 in stage 2.0 (TID 340)2]
org.apache.spark.api.python.PythonException: Traceback (most recent call last):
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 445, in send_message
    sendall(self.conn.get_conn, message)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\network_layer.py", line 239, in sendall
    sock.sendall(buf)
ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip\pyspark\worker.py", line 1247, in main
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip\pyspark\worker.py", line 1237, in process
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 840, in func
    return f(iterator)
           ^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 1795, in func
    r = f(it)
        ^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 5708, in <lambda>
    lambda rows: _write_quarantine_cleaning_partition(rows, config)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 4565, in _write_quarantine_cleaning_partition
    counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 4346, in _bulk_upsert_quarantine
    result = collection.bulk_write(operations, ordered=False)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\collection.py", line 790, in bulk_write
    bulk_api_result = blk.execute(write_concern, session, _Op.INSERT)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 751, in execute
    return self.execute_command(generator, write_concern, session, operation)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 604, in execute_command
    _ = client._retryable_write(
        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2113, in _retryable_write
    return self._retry_with_session(retryable, func, s, bulk, operation, operation_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 1986, in _retry_with_session
    return self._retry_internal(
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2038, in _retry_internal
    ).run()
      ^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2811, in run
    res = self._read() if self._is_read else self._write()
                                             ^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 3014, in _write
    return self._func(self._session, conn, self._retryable)  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 593, in retryable_bulk
    self._execute_command(
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 538, in _execute_command
    result, to_send = self._execute_batch(bwc, cmd, ops, client)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 462, in _execute_batch
    result = self.write_command(bwc, cmd, request_id, msg, to_send, client)  # type: ignore[arg-type]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\helpers.py", line 53, in inner
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 274, in write_command
    reply = bwc.conn.write_command(request_id, msg, bwc.codec)  # type: ignore[misc]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 490, in write_command
    self.send_message(msg, 0)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 448, in send_message
    self._raise_connection_failure(error)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 633, in _raise_connection_failure
    _raise_connection_failure(self.address, error, timeout_details=details)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\pool_shared.py", line 148, in _raise_connection_failure
    raise AutoReconnect(msg) from error
pymongo.errors.AutoReconnect: 127.0.0.1:27017: [WinError 10054] An existing connection was forcibly closed by the remote host (configured timeouts: connectTimeoutMS: 20000.0ms)

        at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:572)
        at org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:784)
        at org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:766)
        at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:525)
        at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
        at scala.collection.Iterator.foreach(Iterator.scala:943)
        at scala.collection.Iterator.foreach$(Iterator.scala:943)
        at org.apache.spark.InterruptibleIterator.foreach(InterruptibleIterator.scala:28)
        at scala.collection.generic.Growable.$plus$plus$eq(Growable.scala:62)
        at scala.collection.generic.Growable.$plus$plus$eq$(Growable.scala:53)
        at scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:105)
        at scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:49)
        at scala.collection.TraversableOnce.to(TraversableOnce.scala:366)
        at scala.collection.TraversableOnce.to$(TraversableOnce.scala:364)
        at org.apache.spark.InterruptibleIterator.to(InterruptibleIterator.scala:28)
        at scala.collection.TraversableOnce.toBuffer(TraversableOnce.scala:358)
        at scala.collection.TraversableOnce.toBuffer$(TraversableOnce.scala:358)
        at org.apache.spark.InterruptibleIterator.toBuffer(InterruptibleIterator.scala:28)
        at scala.collection.TraversableOnce.toArray(TraversableOnce.scala:345)
        at scala.collection.TraversableOnce.toArray$(TraversableOnce.scala:339)
        at org.apache.spark.InterruptibleIterator.toArray(InterruptibleIterator.scala:28)
        at org.apache.spark.rdd.RDD.$anonfun$collect$2(RDD.scala:1049)
        at org.apache.spark.SparkContext.$anonfun$runJob$5(SparkContext.scala:2433)
        at org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)
        at org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)
        at org.apache.spark.scheduler.Task.run(Task.scala:141)
        at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)
        at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)
        at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 21:49:57 WARN TaskSetManager: Lost task 0.0 in stage 2.0 (TID 340) (127.0.0.1 executor driver): org.apache.spark.api.python.PythonException: Traceback (most recent call last):
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 445, in send_message
    sendall(self.conn.get_conn, message)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\network_layer.py", line 239, in sendall
    sock.sendall(buf)
ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip\pyspark\worker.py", line 1247, in main
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip\pyspark\worker.py", line 1237, in process
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 5434, in pipeline_func
    return func(split, prev_func(split, iterator))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 840, in func
    return f(iterator)
           ^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pyspark\rdd.py", line 1795, in func
    r = f(it)
        ^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 5708, in <lambda>
    lambda rows: _write_quarantine_cleaning_partition(rows, config)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 4565, in _write_quarantine_cleaning_partition
    counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline\src\main.py", line 4346, in _bulk_upsert_quarantine
    result = collection.bulk_write(operations, ordered=False)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\collection.py", line 790, in bulk_write
    bulk_api_result = blk.execute(write_concern, session, _Op.INSERT)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 751, in execute
    return self.execute_command(generator, write_concern, session, operation)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 604, in execute_command
    _ = client._retryable_write(
        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2113, in _retryable_write
    return self._retry_with_session(retryable, func, s, bulk, operation, operation_id)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 1986, in _retry_with_session
    return self._retry_internal(
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\_csot.py", line 125, in csot_wrapper
    return func(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2038, in _retry_internal
    ).run()
      ^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 2811, in run
    res = self._read() if self._is_read else self._write()
                                             ^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\mongo_client.py", line 3014, in _write
    return self._func(self._session, conn, self._retryable)  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 593, in retryable_bulk
    self._execute_command(
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 538, in _execute_command
    result, to_send = self._execute_batch(bwc, cmd, ops, client)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 462, in _execute_batch
    result = self.write_command(bwc, cmd, request_id, msg, to_send, client)  # type: ignore[arg-type]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\helpers.py", line 53, in inner
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\bulk.py", line 274, in write_command
    reply = bwc.conn.write_command(request_id, msg, bwc.codec)  # type: ignore[misc]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 490, in write_command
    self.send_message(msg, 0)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 448, in send_message
    self._raise_connection_failure(error)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\synchronous\pool.py", line 633, in _raise_connection_failure
    _raise_connection_failure(self.address, error, timeout_details=details)
  File "C:\Users\PC\Desktop\big_data_progect\.venv\Lib\site-packages\pymongo\pool_shared.py", line 148, in _raise_connection_failure
    raise AutoReconnect(msg) from error
pymongo.errors.AutoReconnect: 127.0.0.1:27017: [WinError 10054] An existing connection was forcibly closed by the remote host (configured timeouts: connectTimeoutMS: 20000.0ms)

        at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:572)
        at org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:784)
        at org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:766)
        at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:525)
        at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
        at scala.collection.Iterator.foreach(Iterator.scala:943)
        at scala.collection.Iterator.foreach$(Iterator.scala:943)
        at org.apache.spark.InterruptibleIterator.foreach(InterruptibleIterator.scala:28)
        at scala.collection.generic.Growable.$plus$plus$eq(Growable.scala:62)
        at scala.collection.generic.Growable.$plus$plus$eq$(Growable.scala:53)
        at scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:105)
        at scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:49)
        at scala.collection.TraversableOnce.to(TraversableOnce.scala:366)
        at scala.collection.TraversableOnce.to$(TraversableOnce.scala:364)
        at org.apache.spark.InterruptibleIterator.to(InterruptibleIterator.scala:28)
        at scala.collection.TraversableOnce.toBuffer(TraversableOnce.scala:358)
        at scala.collection.TraversableOnce.toBuffer$(TraversableOnce.scala:358)
        at org.apache.spark.InterruptibleIterator.toBuffer(InterruptibleIterator.scala:28)
        at scala.collection.TraversableOnce.toArray(TraversableOnce.scala:345)
        at scala.collection.TraversableOnce.toArray$(TraversableOnce.scala:339)
        at org.apache.spark.InterruptibleIterator.toArray(InterruptibleIterator.scala:28)
        at org.apache.spark.rdd.RDD.$anonfun$collect$2(RDD.scala:1049)
        at org.apache.spark.SparkContext.$anonfun$runJob$5(SparkContext.scala:2433)
        at org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)
        at org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)
        at org.apache.spark.scheduler.Task.run(Task.scala:141)
        at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)
        at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)
        at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)

26/08/24 21:49:57 ERROR TaskSetManager: Task 0 in stage 2.0 failed 1 times; aborting job
26/08/24 21:49:58 ERROR DiskBlockManager: Exception while deleting local spark dir: E:\spark-tmp\blockmgr-51b95169-0a34-439f-89b1-1244600fc08a
java.io.IOException: Failed to delete: E:\spark-tmp\blockmgr-51b95169-0a34-439f-89b1-1244600fc08a\27\shuffle_0_5_0.data
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.storage.DiskBlockManager.$anonfun$doStop$1(DiskBlockManager.scala:368)
        at org.apache.spark.storage.DiskBlockManager.$anonfun$doStop$1$adapted(DiskBlockManager.scala:364)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.storage.DiskBlockManager.doStop(DiskBlockManager.scala:364)
        at org.apache.spark.storage.DiskBlockManager.stop(DiskBlockManager.scala:359)
        at org.apache.spark.storage.BlockManager.stop(BlockManager.scala:2120)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:95)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 21:49:58 WARN SparkEnv: Exception while deleting Spark temp dir: E:\spark-tmp\spark-b6b5299d-2d72-4a17-bdca-3ffc19601ae4\userFiles-249233da-d98c-4817-870f-4f6221bc1388
java.io.IOException: Failed to delete: E:\spark-tmp\spark-b6b5299d-2d72-4a17-bdca-3ffc19601ae4\userFiles-249233da-d98c-4817-870f-4f6221bc1388\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:108)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
{
  "step": "cleaning",
  "input": null,
  "error_type": "Py4JJavaError",
  "error_message": "An error occurred while calling z:org.apache.spark.api.python.PythonRDD.collectAndServe.\n: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 2.0 failed 1 times, most recent failure: Lost task 0.0 in stage 2.0 (TID 340) (127.0.0.1 executor driver): org.apache.spark.api.python.PythonException: Traceback (most recent call last):\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 445, in send_message\n    sendall(self.conn.get_conn, message)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\network_layer.py\", line 239, in sendall\n    sock.sendall(buf)\nConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\python\\lib\\pyspark.zip\\pyspark\\worker.py\", line 1247, in main\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\python\\lib\\pyspark.zip\\pyspark\\worker.py\", line 1237, in process\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 840, in func\n    return f(iterator)\n           ^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 1795, in func\n    r = f(it)\n        ^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 5708, in <lambda>\n    lambda rows: _write_quarantine_cleaning_partition(rows, config)\n                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 4565, in _write_quarantine_cleaning_partition\n    counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))\n                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 4346, in _bulk_upsert_quarantine\n    result = collection.bulk_write(operations, ordered=False)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\_csot.py\", line 125, in csot_wrapper\n    return func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\collection.py\", line 790, in bulk_write\n    bulk_api_result = blk.execute(write_concern, session, _Op.INSERT)\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 751, in execute\n    return self.execute_command(generator, write_concern, session, operation)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 604, in execute_command\n    _ = client._retryable_write(\n        ^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2113, in _retryable_write\n    return self._retry_with_session(retryable, func, s, bulk, operation, operation_id)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 1986, in _retry_with_session\n    return self._retry_internal(\n           ^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\_csot.py\", line 125, in csot_wrapper\n    return func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2038, in _retry_internal\n    ).run()\n      ^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2811, in run\n    res = self._read() if self._is_read else self._write()\n                                             ^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 3014, in _write\n    return self._func(self._session, conn, self._retryable)  # type: ignore\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 593, in retryable_bulk\n    self._execute_command(\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 538, in _execute_command\n    result, to_send = self._execute_batch(bwc, cmd, ops, client)\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 462, in _execute_batch\n    result = self.write_command(bwc, cmd, request_id, msg, to_send, client)  # type: ignore[arg-type]\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\helpers.py\", line 53, in inner\n    return func(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 274, in write_command\n    reply = bwc.conn.write_command(request_id, msg, bwc.codec)  # type: ignore[misc]\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 490, in write_command\n    self.send_message(msg, 0)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 448, in send_message\n    self._raise_connection_failure(error)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 633, in _raise_connection_failure\n    _raise_connection_failure(self.address, error, timeout_details=details)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\pool_shared.py\", line 148, in _raise_connection_failure\n    raise AutoReconnect(msg) from error\npymongo.errors.AutoReconnect: 127.0.0.1:27017: [WinError 10054] An existing connection was forcibly closed by the remote host (configured timeouts: connectTimeoutMS: 20000.0ms)\n\r\n\tat org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:572)\r\n\tat org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:784)\r\n\tat org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:766)\r\n\tat org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:525)\r\n\tat org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)\r\n\tat scala.collection.Iterator.foreach(Iterator.scala:943)\r\n\tat scala.collection.Iterator.foreach$(Iterator.scala:943)\r\n\tat org.apache.spark.InterruptibleIterator.foreach(InterruptibleIterator.scala:28)\r\n\tat scala.collection.generic.Growable.$plus$plus$eq(Growable.scala:62)\r\n\tat scala.collection.generic.Growable.$plus$plus$eq$(Growable.scala:53)\r\n\tat scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:105)\r\n\tat scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:49)\r\n\tat scala.collection.TraversableOnce.to(TraversableOnce.scala:366)\r\n\tat scala.collection.TraversableOnce.to$(TraversableOnce.scala:364)\r\n\tat org.apache.spark.InterruptibleIterator.to(InterruptibleIterator.scala:28)\r\n\tat scala.collection.TraversableOnce.toBuffer(TraversableOnce.scala:358)\r\n\tat scala.collection.TraversableOnce.toBuffer$(TraversableOnce.scala:358)\r\n\tat org.apache.spark.InterruptibleIterator.toBuffer(InterruptibleIterator.scala:28)\r\n\tat scala.collection.TraversableOnce.toArray(TraversableOnce.scala:345)\r\n\tat scala.collection.TraversableOnce.toArray$(TraversableOnce.scala:339)\r\n\tat org.apache.spark.InterruptibleIterator.toArray(InterruptibleIterator.scala:28)\r\n\tat org.apache.spark.rdd.RDD.$anonfun$collect$2(RDD.scala:1049)\r\n\tat org.apache.spark.SparkContext.$anonfun$runJob$5(SparkContext.scala:2433)\r\n\tat org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)\r\n\tat org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)\r\n\tat org.apache.spark.scheduler.Task.run(Task.scala:141)\r\n\tat org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)\r\n\tat org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)\r\n\tat org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)\r\n\tat org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)\r\n\tat org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)\r\n\tat java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)\r\n\tat java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)\r\n\tat java.base/java.lang.Thread.run(Thread.java:842)\r\n\nDriver stacktrace:\r\n\tat org.apache.spark.scheduler.DAGScheduler.failJobAndIndependentStages(DAGScheduler.scala:2856)\r\n\tat org.apache.spark.scheduler.DAGScheduler.$anonfun$abortStage$2(DAGScheduler.scala:2792)\r\n\tat org.apache.spark.scheduler.DAGScheduler.$anonfun$abortStage$2$adapted(DAGScheduler.scala:2791)\r\n\tat scala.collection.mutable.ResizableArray.foreach(ResizableArray.scala:62)\r\n\tat scala.collection.mutable.ResizableArray.foreach$(ResizableArray.scala:55)\r\n\tat scala.collection.mutable.ArrayBuffer.foreach(ArrayBuffer.scala:49)\r\n\tat org.apache.spark.scheduler.DAGScheduler.abortStage(DAGScheduler.scala:2791)\r\n\tat org.apache.spark.scheduler.DAGScheduler.$anonfun$handleTaskSetFailed$1(DAGScheduler.scala:1247)\r\n\tat org.apache.spark.scheduler.DAGScheduler.$anonfun$handleTaskSetFailed$1$adapted(DAGScheduler.scala:1247)\r\n\tat scala.Option.foreach(Option.scala:407)\r\n\tat org.apache.spark.scheduler.DAGScheduler.handleTaskSetFailed(DAGScheduler.scala:1247)\r\n\tat org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.doOnReceive(DAGScheduler.scala:3060)\r\n\tat org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:2994)\r\n\tat org.apache.spark.scheduler.DAGSchedulerEventProcessLoop.onReceive(DAGScheduler.scala:2983)\r\n\tat org.apache.spark.util.EventLoop$$anon$1.run(EventLoop.scala:49)\r\n\tat org.apache.spark.scheduler.DAGScheduler.runJob(DAGScheduler.scala:989)\r\n\tat org.apache.spark.SparkContext.runJob(SparkContext.scala:2393)\r\n\tat org.apache.spark.SparkContext.runJob(SparkContext.scala:2414)\r\n\tat org.apache.spark.SparkContext.runJob(SparkContext.scala:2433)\r\n\tat org.apache.spark.SparkContext.runJob(SparkContext.scala:2458)\r\n\tat org.apache.spark.rdd.RDD.$anonfun$collect$1(RDD.scala:1049)\r\n\tat org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:151)\r\n\tat org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:112)\r\n\tat org.apache.spark.rdd.RDD.withScope(RDD.scala:410)\r\n\tat org.apache.spark.rdd.RDD.collect(RDD.scala:1048)\r\n\tat org.apache.spark.api.python.PythonRDD$.collectAndServe(PythonRDD.scala:195)\r\n\tat org.apache.spark.api.python.PythonRDD.collectAndServe(PythonRDD.scala)\r\n\tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)\r\n\tat java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)\r\n\tat java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\r\n\tat java.base/java.lang.reflect.Method.invoke(Method.java:568)\r\n\tat py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)\r\n\tat py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)\r\n\tat py4j.Gateway.invoke(Gateway.java:282)\r\n\tat py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)\r\n\tat py4j.commands.CallCommand.execute(CallCommand.java:79)\r\n\tat py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)\r\n\tat py4j.ClientServerConnection.run(ClientServerConnection.java:106)\r\n\tat java.base/java.lang.Thread.run(Thread.java:842)\r\nCaused by: org.apache.spark.api.python.PythonException: Traceback (most recent call last):\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 445, in send_message\n    sendall(self.conn.get_conn, message)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\network_layer.py\", line 239, in sendall\n    sock.sendall(buf)\nConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\python\\lib\\pyspark.zip\\pyspark\\worker.py\", line 1247, in main\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\python\\lib\\pyspark.zip\\pyspark\\worker.py\", line 1237, in process\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 5434, in pipeline_func\n    return func(split, prev_func(split, iterator))\n                       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 840, in func\n    return f(iterator)\n           ^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pyspark\\rdd.py\", line 1795, in func\n    r = f(it)\n        ^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 5708, in <lambda>\n    lambda rows: _write_quarantine_cleaning_partition(rows, config)\n                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 4565, in _write_quarantine_cleaning_partition\n    counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))\n                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\midterm1-data-pipeline\\src\\main.py\", line 4346, in _bulk_upsert_quarantine\n    result = collection.bulk_write(operations, ordered=False)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\_csot.py\", line 125, in csot_wrapper\n    return func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\collection.py\", line 790, in bulk_write\n    bulk_api_result = blk.execute(write_concern, session, _Op.INSERT)\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 751, in execute\n    return self.execute_command(generator, write_concern, session, operation)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 604, in execute_command\n    _ = client._retryable_write(\n        ^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2113, in _retryable_write\n    return self._retry_with_session(retryable, func, s, bulk, operation, operation_id)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 1986, in _retry_with_session\n    return self._retry_internal(\n           ^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\_csot.py\", line 125, in csot_wrapper\n    return func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2038, in _retry_internal\n    ).run()\n      ^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 2811, in run\n    res = self._read() if self._is_read else self._write()\n                                             ^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\mongo_client.py\", line 3014, in _write\n    return self._func(self._session, conn, self._retryable)  # type: ignore\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 593, in retryable_bulk\n    self._execute_command(\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 538, in _execute_command\n    result, to_send = self._execute_batch(bwc, cmd, ops, client)\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 462, in _execute_batch\n    result = self.write_command(bwc, cmd, request_id, msg, to_send, client)  # type: ignore[arg-type]\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\helpers.py\", line 53, in inner\n    return func(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\bulk.py\", line 274, in write_command\n    reply = bwc.conn.write_command(request_id, msg, bwc.codec)  # type: ignore[misc]\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 490, in write_command\n    self.send_message(msg, 0)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 448, in send_message\n    self._raise_connection_failure(error)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\synchronous\\pool.py\", line 633, in _raise_connection_failure\n    _raise_connection_failure(self.address, error, timeout_details=details)\n  File \"C:\\Users\\PC\\Desktop\\big_data_progect\\.venv\\Lib\\site-packages\\pymongo\\pool_shared.py\", line 148, in _raise_connection_failure\n    raise AutoReconnect(msg) from error\npymongo.errors.AutoReconnect: 127.0.0.1:27017: [WinError 10054] An existing connection was forcibly closed by the remote host (configured timeouts: connectTimeoutMS: 20000.0ms)\n\r\n\tat org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:572)\r\n\tat org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:784)\r\n\tat org.apache.spark.api.python.PythonRunner$$anon$3.read(PythonRunner.scala:766)\r\n\tat org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:525)\r\n\tat org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)\r\n\tat scala.collection.Iterator.foreach(Iterator.scala:943)\r\n\tat scala.collection.Iterator.foreach$(Iterator.scala:943)\r\n\tat org.apache.spark.InterruptibleIterator.foreach(InterruptibleIterator.scala:28)\r\n\tat scala.collection.generic.Growable.$plus$plus$eq(Growable.scala:62)\r\n\tat scala.collection.generic.Growable.$plus$plus$eq$(Growable.scala:53)\r\n\tat scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:105)\r\n\tat scala.collection.mutable.ArrayBuffer.$plus$plus$eq(ArrayBuffer.scala:49)\r\n\tat scala.collection.TraversableOnce.to(TraversableOnce.scala:366)\r\n\tat scala.collection.TraversableOnce.to$(TraversableOnce.scala:364)\r\n\tat org.apache.spark.InterruptibleIterator.to(InterruptibleIterator.scala:28)\r\n\tat scala.collection.TraversableOnce.toBuffer(TraversableOnce.scala:358)\r\n\tat scala.collection.TraversableOnce.toBuffer$(TraversableOnce.scala:358)\r\n\tat org.apache.spark.InterruptibleIterator.toBuffer(InterruptibleIterator.scala:28)\r\n\tat scala.collection.TraversableOnce.toArray(TraversableOnce.scala:345)\r\n\tat scala.collection.TraversableOnce.toArray$(TraversableOnce.scala:339)\r\n\tat org.apache.spark.InterruptibleIterator.toArray(InterruptibleIterator.scala:28)\r\n\tat org.apache.spark.rdd.RDD.$anonfun$collect$2(RDD.scala:1049)\r\n\tat org.apache.spark.SparkContext.$anonfun$runJob$5(SparkContext.scala:2433)\r\n\tat org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)\r\n\tat org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)\r\n\tat org.apache.spark.scheduler.Task.run(Task.scala:141)\r\n\tat org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)\r\n\tat org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)\r\n\tat org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)\r\n\tat org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)\r\n\tat org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)\r\n\tat java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)\r\n\tat java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)\r\n\t... 1 more\r\n",
  "recovery": "Check the reported resource, path, schema, MongoDB, Java, or Connector requirement; no partial JSON result is treated as successful."
}
26/08/24 21:49:58 ERROR TaskContextImpl: Error in TaskCompletionListener
org.apache.spark.SparkException: Block broadcast_1 does not exist
        at org.apache.spark.errors.SparkCoreErrors$.blockDoesNotExistError(SparkCoreErrors.scala:318)
        at org.apache.spark.storage.BlockInfoManager.blockInfo(BlockInfoManager.scala:269)
        at org.apache.spark.storage.BlockInfoManager.unlock(BlockInfoManager.scala:390)
        at org.apache.spark.storage.BlockManager.releaseLock(BlockManager.scala:1309)
        at org.apache.spark.broadcast.TorrentBroadcast.$anonfun$releaseBlockManagerLock$1(TorrentBroadcast.scala:319)
        at org.apache.spark.broadcast.TorrentBroadcast.$anonfun$releaseBlockManagerLock$1$adapted(TorrentBroadcast.scala:319)
        at org.apache.spark.TaskContext$$anon$1.onTaskCompletion(TaskContext.scala:137)
        at org.apache.spark.TaskContextImpl.$anonfun$invokeTaskCompletionListeners$1(TaskContextImpl.scala:144)
        at org.apache.spark.TaskContextImpl.$anonfun$invokeTaskCompletionListeners$1$adapted(TaskContextImpl.scala:144)
        at org.apache.spark.TaskContextImpl.invokeListeners(TaskContextImpl.scala:199)
        at org.apache.spark.TaskContextImpl.invokeTaskCompletionListeners(TaskContextImpl.scala:144)
        at org.apache.spark.TaskContextImpl.markTaskCompleted(TaskContextImpl.scala:137)
        at org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:177)
        at org.apache.spark.scheduler.Task.run(Task.scala:141)
        at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)
        at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)
        at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 21:49:58 ERROR Utils: Uncaught exception in thread Executor task launch worker for task 1.0 in stage 2.0 (TID 341)
java.lang.NullPointerException: Cannot invoke "org.apache.spark.SparkEnv.blockManager()" because the return value of "org.apache.spark.SparkEnv$.get()" is null
        at org.apache.spark.scheduler.Task.$anonfun$run$3(Task.scala:146)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.scheduler.Task.run(Task.scala:144)
        at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:620)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)
        at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)
        at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:94)
        at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:623)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 21:49:59 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-b6b5299d-2d72-4a17-bdca-3ffc19601ae4
java.io.IOException: Failed to delete: E:\spark-tmp\spark-b6b5299d-2d72-4a17-bdca-3ffc19601ae4\userFiles-249233da-d98c-4817-870f-4f6221bc1388\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 21:49:59 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-b6b5299d-2d72-4a17-bdca-3ffc19601ae4\userFiles-249233da-d98c-4817-870f-4f6221bc1388
java.io.IOException: Failed to delete: E:\spark-tmp\spark-b6b5299d-2d72-4a17-bdca-3ffc19601ae4\userFiles-249233da-d98c-4817-870f-4f6221bc1388\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
SUCCESS: The process with PID 13756 (child process of PID 22668) has been terminated.
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> SUCCESS: The process with PID 22668 (child process of PID 10948) has been terminated.
SUCCESS: The process with PID 10948 (child process of PID 24308) has been terminated.

PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step cleaning `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 0
>>
26/08/24 21:56:28 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".                                                                                                                                                                               To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).                                                                                                                       26/08/24 21:56:29 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).               {                                                                                                                                                                                                                    "step": "cleaning",                                                                                                                                                                                                "input": null,                                                                                                                                                                                                     "error_type": "ServerSelectionTimeoutError",                                                                                                                                                                       "error_message": "127.0.0.1:27017: [WinError 10061] No connection could be made because the target machine actively refused it (configured timeouts: socketTimeoutMS: 20000.0ms, connectTimeoutMS: 20000.0ms), Timeout: 10.0s, Topology Description: <TopologyDescription id: 6a8c93e149e6ae0233a4b3b1, topology_type: Unknown, servers: [<ServerDescription ('127.0.0.1', 27017) server_type: Unknown, rtt: None, error=AutoReconnect('127.0.0.1:27017: [WinError 10061] No connection could be made because the target machine actively refused it (configured timeouts: socketTimeoutMS: 20000.0ms, connectTimeoutMS: 20000.0ms)')>]>",               "recovery": "Check the reported resource, path, schema, MongoDB, Java, or Connector requirement; no partial JSON result is treated as successful."                                                               }                                                                                                                                                                                                                  PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> SUCCESS: The process with PID 7972 (child process of PID 2800) has been terminated.                                                                PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $MongoBin = "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"                                                                                   >> $DataPath = "E:\mongodb-project-data"d process of PID 13476) has been terminated.                                                                                                                               >> $LogPath = "E:\mongodb-project-log"                                                                                                                                                                             >> $LogFile = Join-Path $LogPath "mongod.log"
>>
>> New-Item -ItemType Directory -Force -Path $LogPath | Out-Null
>>
>> $MongoProcess = Get-Process mongod -ErrorAction SilentlyContinue
>> if ($MongoProcess) {
>>     Write-Host "mongod is already running. PID:" $MongoProcess.Id
>> } else {
>>     $MongoCommand = "& `"$MongoBin`" --dbpath `"$DataPath`" --logpath `"$LogFile`" --logappend --bind_ip 127.0.0.1 --port 27017"
>>     Start-Process powershell.exe `
>>       -ArgumentList @(
>>         "-NoExit",
>>         "-ExecutionPolicy", "Bypass",
>>         "-Command", $MongoCommand
>>       ) `
>>       -WindowStyle Normal
>>     Write-Host "MongoDB opened in a separate PowerShell window"
>> }
>>
>> Start-Sleep -Seconds 10
>>
>> Get-Process mongod -ErrorAction SilentlyContinue |
>>     Select-Object Id,ProcessName,Path
>>
>> Test-NetConnection 127.0.0.1 -Port 27017 |
>>     Select-Object ComputerName,RemotePort,TcpTestSucceeded
>>
MongoDB opened in a separate PowerShell window
WARNING: TCP connect to (127.0.0.1 : 27017) failed

ComputerName RemotePort TcpTestSucceeded
------------ ---------- ----------------
127.0.0.1         27017            False


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> Write-Host "=== mongod process ==="
>> Get-Process mongod -ErrorAction SilentlyContinue |
>>     Select-Object Id,ProcessName,Path
>>
>> Write-Host "=== MongoDB log ==="
>> $LogFile = "E:\mongodb-project-log\mongod.log"
>> if (Test-Path $LogFile) {
>>     Get-Content -LiteralPath $LogFile -Tail 80
>> } else {
>>     Write-Host "LOG NOT FOUND:" $LogFile
>> }
>>
=== mongod process ===
=== MongoDB log ===
{"t":{"$date":"2026-08-24T21:49:51.759+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn20","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"80502fec-a4e8-4a7d-82e7-bb953dd95b13"}},"$db":"ecommerce_store"},"opid":52320,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":995108,"timeReadingMicros":10150},"timeWaitingMicros":{"storageEngineMicros":21413}},"remote":"127.0.0.1:59065","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":459,"durationMillis":459}}
{"t":{"$date":"2026-08-24T21:49:53.103+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn17","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"4e73c4db-6bba-47e1-af59-1e47c9d92ad7"}},"$db":"ecommerce_store"},"opid":49249,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":485244,"timeReadingMicros":4996},"timeWaitingMicros":{"storageEngineMicros":13459}},"remote":"127.0.0.1:59061","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":266,"durationMillis":266}}
{"t":{"$date":"2026-08-24T21:49:53.229+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn20","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"80502fec-a4e8-4a7d-82e7-bb953dd95b13"}},"$db":"ecommerce_store"},"opid":52321,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":630899,"timeReadingMicros":2990},"timeWaitingMicros":{"storageEngineMicros":15189}},"remote":"127.0.0.1:59065","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":382,"durationMillis":382}}
{"t":{"$date":"2026-08-24T21:49:54.091+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn17","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"4e73c4db-6bba-47e1-af59-1e47c9d92ad7"}},"$db":"ecommerce_store"},"opid":49250,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":152344,"timeReadingMicros":2015},"timeWaitingMicros":{"storageEngineMicros":7095}},"remote":"127.0.0.1:59061","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":139,"durationMillis":139}}
{"t":{"$date":"2026-08-24T21:49:54.134+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn20","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"80502fec-a4e8-4a7d-82e7-bb953dd95b13"}},"$db":"ecommerce_store"},"opid":52322,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":225476},"timeWaitingMicros":{"storageEngineMicros":5678}},"remote":"127.0.0.1:59065","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":127,"durationMillis":127}}
{"t":{"$date":"2026-08-24T21:49:54.410+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn17","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"4e73c4db-6bba-47e1-af59-1e47c9d92ad7"}},"$db":"ecommerce_store"},"opid":49251,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":137195,"timeReadingMicros":1020},"timeWaitingMicros":{"storageEngineMicros":5202}},"remote":"127.0.0.1:59061","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":103,"durationMillis":103}}
{"t":{"$date":"2026-08-24T21:49:54.422+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn20","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"80502fec-a4e8-4a7d-82e7-bb953dd95b13"}},"$db":"ecommerce_store"},"opid":52323,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":186112,"timeReadingMicros":2011},"timeWaitingMicros":{"storageEngineMicros":5012}},"remote":"127.0.0.1:59065","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":116,"durationMillis":116}}
{"t":{"$date":"2026-08-24T21:49:54.712+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn20","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"80502fec-a4e8-4a7d-82e7-bb953dd95b13"}},"$db":"ecommerce_store"},"opid":52324,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":29285},"timeWaitingMicros":{"storageEngineMicros":4475}},"remote":"127.0.0.1:59065","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":100,"durationMillis":100}}
{"t":{"$date":"2026-08-24T21:49:55.133+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":132692,"thread":"24304:140721565411152","session_dhandle_name":"file:sizeStorer.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 1 pages (0 MB), walked 1 pages and checkpointed 0 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.133+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":133690,"thread":"24304:140721565411152","session_dhandle_name":"file:sizeStorer.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 2 pages (0 MB), walked 2 pages and checkpointed 0 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.135+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":134686,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 3 pages (0 MB), walked 8 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.136+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":135685,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 4 pages (0 MB), walked 9 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.137+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":136681,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 5 pages (0 MB), walked 10 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.138+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":137680,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 6 pages (0 MB), walked 11 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.139+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":138676,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 7 pages (0 MB), walked 12 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.140+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":139709,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 8 pages (0 MB), walked 13 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.142+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":141715,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 9 pages (1 MB), walked 14 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.143+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":142712,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 10 pages (1 MB), walked 15 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.151+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":150691,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 20 pages (2 MB), walked 25 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.156+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":156683,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 30 pages (3 MB), walked 35 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.162+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":162668,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 40 pages (5 MB), walked 45 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.169+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":169190,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 50 pages (6 MB), walked 55 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.176+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":175173,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 60 pages (8 MB), walked 65 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.182+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":181158,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 70 pages (9 MB), walked 75 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.188+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":187144,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 80 pages (10 MB), walked 85 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.193+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":193126,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 90 pages (12 MB), walked 95 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.199+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":199111,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 100 pages (13 MB), walked 105 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.281+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":280910,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 200 pages (27 MB), walked 205 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.342+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":342080,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 300 pages (41 MB), walked 305 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.408+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":407859,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 400 pages (55 MB), walked 405 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.469+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":468652,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 500 pages (69 MB), walked 505 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.530+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":529384,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 600 pages (83 MB), walked 605 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.589+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":588569,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 700 pages (97 MB), walked 705 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.656+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":655175,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 800 pages (110 MB), walked 805 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.719+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":718544,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 900 pages (124 MB), walked 905 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:55.757+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597395,"ts_usec":756765,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 0 seconds, wrote 1000 pages (138 MB), walked 1005 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:56.113+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597396,"ts_usec":113269,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 1 seconds, wrote 2000 pages (277 MB), walked 2005 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:56.206+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn17","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"4e73c4db-6bba-47e1-af59-1e47c9d92ad7"}},"$db":"ecommerce_store"},"opid":49253,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":12320,"timeReadingMicros":995},"timeWaitingMicros":{"storageEngineMicros":27822}},"remote":"127.0.0.1:59061","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":504,"durationMillis":504}}
{"t":{"$date":"2026-08-24T21:49:56.352+03:00"},"s":"E",  "c":"WT",       "id":22435,   "ctx":"thread49","msg":"WiredTiger error message","attr":{"error":28,"message":{"ts_sec":1787597396,"ts_usec":351957,"thread":"24304:140721565411152","session_name":"log-server","category":"WT_VERB_DEFAULT","log_id":1000000,"category_id":12,"verbose_level":"ERROR","verbose_level_id":-3,"msg":"int __cdecl __win_file_set_end(struct __wt_file_handle *,struct __wt_session *,__int64):385:E:\\mongodb-project-data\\journal\\WiredTigerTmplog.0000000004: handle-set-end: SetEndOfFile: There is not enough space on the disk.\r\n","error_str":"No space left on device","error_code":28}}}
{"t":{"$date":"2026-08-24T21:49:56.353+03:00"},"s":"E",  "c":"WT",       "id":22435,   "ctx":"thread49","msg":"WiredTiger error message","attr":{"error":28,"message":{"ts_sec":1787597396,"ts_usec":352954,"thread":"24304:140721565411152","session_name":"log-server","category":"WT_VERB_DEFAULT","log_id":1000000,"category_id":12,"verbose_level":"ERROR","verbose_level_id":-3,"msg":"int __cdecl __log_prealloc_once(struct __wt_session_impl *):577:log pre-alloc server error","error_str":"No space left on device","error_code":28}}}
{"t":{"$date":"2026-08-24T21:49:56.354+03:00"},"s":"E",  "c":"WT",       "id":22435,   "ctx":"thread49","msg":"WiredTiger error message","attr":{"error":28,"message":{"ts_sec":1787597396,"ts_usec":353953,"thread":"24304:140721565411152","session_name":"log-server","category":"WT_VERB_DEFAULT","log_id":1000000,"category_id":12,"verbose_level":"ERROR","verbose_level_id":-3,"msg":"unsigned int __cdecl __log_server(void *):1025:log server error","error_str":"No space left on device","error_code":28}}}
{"t":{"$date":"2026-08-24T21:49:56.355+03:00"},"s":"E",  "c":"WT",       "id":22435,   "ctx":"thread49","msg":"WiredTiger error message","attr":{"error":-31804,"message":{"ts_sec":1787597396,"ts_usec":353953,"thread":"24304:140721565411152","session_name":"log-server","category":"WT_VERB_DEFAULT","log_id":1000000,"category_id":12,"verbose_level":"ERROR","verbose_level_id":-3,"msg":"unsigned int __cdecl __log_server(void *):1025:the process must exit and restart","error_str":"WT_PANIC: WiredTiger library panic","error_code":-31804}}}
{"t":{"$date":"2026-08-24T21:49:56.355+03:00"},"s":"F",  "c":"ASSERT",   "id":23089,   "ctx":"thread49","msg":"Fatal assertion","attr":{"msgid":50853,"location":"src/mongo/db/storage/wiredtiger/wiredtiger_util.cpp:647:9:int __cdecl mongo::`anonymous-namespace'::mdb_handle_error_with_startup_suppression(struct __wt_event_handler *,struct __wt_session *,int,const char *)"}}
{"t":{"$date":"2026-08-24T21:49:56.355+03:00"},"s":"F",  "c":"ASSERT",   "id":23090,   "ctx":"thread49","msg":"\n\n***aborting after fassert() failure\n\n"}
{"t":{"$date":"2026-08-24T21:49:56.355+03:00"},"s":"F",  "c":"CONTROL",  "id":6384300, "ctx":"thread49","msg":"Writing fatal message","attr":{"message":"Got signal: 22 (SIGABRT).\n"}}
{"t":{"$date":"2026-08-24T21:49:56.369+03:00"},"s":"I",  "c":"CONTROL",  "id":31380,   "ctx":"thread49","msg":"BACKTRACE","attr":{"bt":{"backtrace":[{"a":"7FF6D546E141","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6CEB51"},{"a":"7FF6D5479BF3","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6DA603"},{"a":"7FFC49C5E6D5","module":"ucrtbase.dll","s":"raise","s+":"1E5"},{"a":"7FFC49C5F6E1","module":"ucrtbase.dll","s":"abort","s+":"31"},{"a":"7FF6D5485BA6","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6E65B6"},{"a":"7FF6D5486AA2","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6E74B2"},{"a":"7FF6D25FF629","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"54989"},{"a":"7FF6D26A1758","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"F6AB8"},{"a":"7FF6D26A28F8","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"F7C58"},{"a":"7FF6D2706928","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"15BC88"},{"a":"7FFC49C09333","module":"ucrtbase.dll","s":"recalloc","s+":"A3"},{"a":"7FFC4AEC259D","module":"KERNEL32.DLL","s":"BaseThreadInitThunk","s+":"1D"}]}},"tags":[]}
{"t":{"$date":"2026-08-24T21:49:56.369+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D546E141","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6CEB51"}}}
{"t":{"$date":"2026-08-24T21:49:56.369+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D5479BF3","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6DA603"}}}
{"t":{"$date":"2026-08-24T21:49:56.369+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC49C5E6D5","module":"ucrtbase.dll","s":"raise","s+":"1E5"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC49C5F6E1","module":"ucrtbase.dll","s":"abort","s+":"31"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D5485BA6","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6E65B6"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D5486AA2","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6E74B2"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D25FF629","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"54989"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D26A1758","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"F6AB8"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D26A28F8","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"F7C58"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D2706928","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"15BC88"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC49C09333","module":"ucrtbase.dll","s":"recalloc","s+":"A3"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC4AEC259D","module":"KERNEL32.DLL","s":"BaseThreadInitThunk","s+":"1D"}}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"F",  "c":"CONTROL",  "id":6384300, "ctx":"thread49","msg":"Writing fatal message","attr":{"message":"\n"}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"F",  "c":"CONTROL",  "id":6384300, "ctx":"thread49","msg":"Writing fatal message","attr":{"message":"\n"}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"F",  "c":"CONTROL",  "id":23134,   "ctx":"thread49","msg":"Unhandled exception","attr":{"exceptionString":"0xE0000001","addressString":"0x00007FFC4963055C"}}
{"t":{"$date":"2026-08-24T21:49:56.370+03:00"},"s":"F",  "c":"CONTROL",  "id":23136,   "ctx":"thread49","msg":"*** stack trace for unhandled exception:"}
{"t":{"$date":"2026-08-24T21:49:56.376+03:00"},"s":"I",  "c":"CONTROL",  "id":31380,   "ctx":"thread49","msg":"BACKTRACE","attr":{"bt":{"backtrace":[{"a":"7FFC4963055C","module":"KERNELBASE.dll","s":"RaiseException","s+":"6C"},{"a":"7FF6D547929A","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6D9CAA"},{"a":"7FF6D5479C15","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6DA625"},{"a":"7FFC49C5E6D5","module":"ucrtbase.dll","s":"raise","s+":"1E5"},{"a":"7FFC49C5F6E1","module":"ucrtbase.dll","s":"abort","s+":"31"},{"a":"7FF6D5485BA6","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6E65B6"},{"a":"7FF6D5486AA2","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6E74B2"},{"a":"7FF6D25FF629","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"54989"},{"a":"7FF6D26A1758","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"F6AB8"},{"a":"7FF6D26A28F8","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"F7C58"},{"a":"7FF6D2706928","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"15BC88"},{"a":"7FFC49C09333","module":"ucrtbase.dll","s":"recalloc","s+":"A3"},{"a":"7FFC4AEC259D","module":"KERNEL32.DLL","s":"BaseThreadInitThunk","s+":"1D"}]}},"tags":[]}
{"t":{"$date":"2026-08-24T21:49:56.376+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC4963055C","module":"KERNELBASE.dll","s":"RaiseException","s+":"6C"}}}
{"t":{"$date":"2026-08-24T21:49:56.376+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D547929A","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6D9CAA"}}}
{"t":{"$date":"2026-08-24T21:49:56.376+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D5479C15","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6DA625"}}}
{"t":{"$date":"2026-08-24T21:49:56.376+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC49C5E6D5","module":"ucrtbase.dll","s":"raise","s+":"1E5"}}}
{"t":{"$date":"2026-08-24T21:49:56.376+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC49C5F6E1","module":"ucrtbase.dll","s":"abort","s+":"31"}}}
{"t":{"$date":"2026-08-24T21:49:56.376+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D5485BA6","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6E65B6"}}}
{"t":{"$date":"2026-08-24T21:49:56.376+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D5486AA2","module":"mongod.exe","s":"tcmalloc::Sampler::operator=","s+":"6E74B2"}}}
{"t":{"$date":"2026-08-24T21:49:56.377+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D25FF629","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"54989"}}}
{"t":{"$date":"2026-08-24T21:49:56.377+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D26A1758","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"F6AB8"}}}
{"t":{"$date":"2026-08-24T21:49:56.377+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D26A28F8","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"F7C58"}}}
{"t":{"$date":"2026-08-24T21:49:56.377+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FF6D2706928","module":"mongod.exe","s":"MallocExtension::ReadStackTraces","s+":"15BC88"}}}
{"t":{"$date":"2026-08-24T21:49:56.377+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC49C09333","module":"ucrtbase.dll","s":"recalloc","s+":"A3"}}}
{"t":{"$date":"2026-08-24T21:49:56.377+03:00"},"s":"I",  "c":"CONTROL",  "id":31445,   "ctx":"thread49","msg":"Frame","attr":{"frame":{"a":"7FFC4AEC259D","module":"KERNEL32.DLL","s":"BaseThreadInitThunk","s+":"1D"}}}
{"t":{"$date":"2026-08-24T21:49:56.380+03:00"},"s":"I",  "c":"CONTROL",  "id":23132,   "ctx":"thread49","msg":"Writing minidump diagnostic file","attr":{"dumpName":"C:\\Program Files\\MongoDB\\Server\\8.3\\bin\\mongod.2026-08-24T18-49-56.mdmp"}}
{"t":{"$date":"2026-08-24T21:49:56.446+03:00"},"s":"I",  "c":"COMMAND",  "id":51803,   "ctx":"conn20","msg":"Slow query","attr":{"type":"command","isFromUserConnection":true,"isFromPriorityPortConnection":false,"ns":"ecommerce_store.$cmd","collectionType":"normal","command":{"update":"orders_quarantine","ordered":false,"lsid":{"id":{"$uuid":"80502fec-a4e8-4a7d-82e7-bb953dd95b13"}},"$db":"ecommerce_store"},"opid":52325,"numYields":0,"reslen":60,"locks":{"ReplicationStateTransition":{"acquireCount":{"w":500}},"Global":{"acquireCount":{"w":500}},"Database":{"acquireCount":{"w":500}},"Collection":{"acquireCount":{"w":500}}},"flowControl":{"acquireCount":500},"storage":{"data":{"bytesRead":11997,"timeReadingMicros":998},"timeWaitingMicros":{"storageEngineMicros":35511}},"remote":"127.0.0.1:59065","protocol":"op_msg","numInterruptChecks":3002,"priorityLowered":false,"wasMarkedNonDeprioritizable":false,"queues":{"ingress":{"admissions":1,"totalTimeQueuedMicros":0},"execution":{"admissions":501,"totalTimeQueuedMicros":0}},"workingMillis":646,"durationMillis":646}}
{"t":{"$date":"2026-08-24T21:49:56.539+03:00"},"s":"I",  "c":"WTCHKPT",  "id":22430,   "ctx":"Checkpointer","msg":"WiredTiger message","attr":{"message":{"ts_sec":1787597396,"ts_usec":538405,"thread":"24304:140721565411152","session_dhandle_name":"file:collection-dca7210f-066e-4bb0-83cb-33d835631296.wt","session_name":"WT_SESSION.checkpoint","category":"WT_VERB_CHECKPOINT_PROGRESS","log_id":1000000,"category_id":7,"verbose_level":"INFO","verbose_level_id":0,"msg":"Checkpoint has been running for 1 seconds, wrote 3000 pages (415 MB), walked 3005 pages and checkpointed 1 files"}}}
{"t":{"$date":"2026-08-24T21:49:56.825+03:00"},"s":"F",  "c":"CONTROL",  "id":23137,   "ctx":"thread49","msg":"*** immediate exit due to unhandled exception"}
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> $JavaProcesses = Get-Process java -ErrorAction SilentlyContinue
>> if ($JavaProcesses) {
>>     Write-Host "يوجد Java يعمل؛ لا تحذف Spark temp الآن:" -ForegroundColor Yellow
>>     $JavaProcesses | Select-Object Id,ProcessName,Path
>>     throw "أغلق تشغيل Spark أولًا ثم أعد المحاولة"
>> }
>>
>> $SparkTemp = "E:\spark-tmp"
>> if (Test-Path $SparkTemp) {
>>     Remove-Item -LiteralPath (Join-Path $SparkTemp "*") `
>>         -Recurse -Force -ErrorAction SilentlyContinue
>>     Write-Host "Spark temporary files cleaned"
>> }
>>
>> Get-PSDrive E | Select-Object Name,
>>     @{Name="FreeGB";Expression={[math]::Round($_.Free / 1GB, 2)}},
>>     @{Name="UsedGB";Expression={[math]::Round($_.Used / 1GB, 2)}}
>>
يوجد Java يعمل؛ لا تحذف Spark temp الآن:

أغلق تشغيل Spark أولًا ثم أعد المحاولة
At line:7 char:5
+     throw "أغلق تشغيل Spark أولًا ثم أعد المحاولة"
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : OperationStopped: (أغلق تشغيل Spark أولًا ثم أعد المحاولة:String) [], RuntimeException
    + FullyQualifiedErrorId : أغلق تشغيل Spark أولًا ثم أعد المحاولة

PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> Get-CimInstance Win32_Process -Filter "Name = 'java.exe'" |
>>     Select-Object ProcessId,CommandLine
>>

ProcessId CommandLine
--------- -----------
     7332 "C:\Program Files\Java\jdk-17/bin/java.exe"  "-Dfile.encoding=UTF-8"  --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=...


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> Stop-Process -Id 7332 -Force -ErrorAction SilentlyContinue
>> Start-Sleep -Seconds 3
>> Write-Host "Spark Java process 7332 stopped"
>>
>> $SparkTemp = "E:\spark-tmp"
>> if (Test-Path $SparkTemp) {
>>     Remove-Item -LiteralPath (Join-Path $SparkTemp "*") `
>>         -Recurse -Force -ErrorAction SilentlyContinue
>>     Write-Host "Spark temp cleaned"
>> }
>>
>> Get-PSDrive E | Select-Object Name,
>>     @{Name="FreeGB";Expression={[math]::Round($_.Free / 1GB, 2)}},
>>     @{Name="UsedGB";Expression={[math]::Round($_.Used / 1GB, 2)}}
>>
Spark Java process 7332 stopped
Spark temp cleaned

Name FreeGB UsedGB
---- ------ ------
E      3.89 181.65


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> Get-ChildItem E:\ -Force |
>>     Select-Object Mode,Name,
>>         @{Name="SizeGB";Expression={
>>             if ($_.PSIsContainer) {
>>                 $bytes = (Get-ChildItem $_.FullName -Recurse -Force -File -ErrorAction SilentlyContinue |
>>                     Measure-Object -Property Length -Sum).Sum
>>                 [math]::Round(($bytes / 1GB), 2)
>>             } else {
>>                 [math]::Round(($_.Length / 1GB), 2)
>>             }
>>         }} |
>>     Sort-Object SizeGB -Descending
>>

Mode   Name                                     SizeGB
----   ----                                     ------
d----- الهام                                     41.46
d----- mongodb-project-data                      31.65
d----- Fultter                                      19
d----- مستوى ثالث                                18.99
d----- سطح المكتب                                13.68
d----- PycharmProjects                           10.04
d----- التنزيلات                                  3.85
d----- lec_1                                      3.69
d----- شهاب الخالد                                 2.9
d----- Lec_6                                      2.64
d----- تعلم الهياكل                               2.44
d----- lec_5                                      2.37
-a---- lec_6.zip                                  2.02
d----- big data                                   1.75
d----- tablupabluc                                1.66
d----- agent ai                                   1.51
d----- flutter_records                            1.44
d----- مكتبة مكتبة                                1.35
d----- Book python                                0.93
d-r--- دوره احتارف الكالي لنكس                    0.58
d----- Java                                       0.28
-a---- archive-٣.zip                              0.16
d----- New folder                                 0.06
d----- spark-tmp                                  0.05
d----- hospital.py                                0.05
d----- mongodb-project-log                        0.05
d----- الجنيد٢                                    0.04
d----- Qtpython                                   0.04
d----- Agent 2                                    0.02
d----- images                                     0.02
d----- Lec_2                                      0.02
d----- محاضرات مهارات الحاسوب                     0.01
d----- كتب ممتازة يشرح اساسيات الذكاء الاصطناعي   0.01
da---- هياكل البيانات                             0.01
-a---- المحاضرة الاولى معالجة صور (1).zip            0
-a---- QRoundProgressBar-master.zip                  0
-a---- Screenshot 2024-12-02 113528.png              0
-a---- This PC - Shortcut.lnk                        0
-a---- prolog-expert-system-master.zip               0
-a---- New Volume (D) - Shortcut.lnk                 0
-a---- npoint                                        0
-a---- page.jpg.png                                  0
d----- machen linear                                 0        >
>> Get-PSDrive E | Select-Object Name,               0
>>     @{Name="FreeGB";Expression={[math]::Round($_.Free / 1GB, 2)}},
>>     @{Name="UsedGB";Expression={[math]::Round($_.Used / 1GB, 2)}}
>>

Name FreeGB UsedGB
---- ------ ------
E     36.92 148.63


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> $MongoBin = "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
>> $DataPath = "E:\mongodb-project-data"
>> $LogPath = "E:\mongodb-project-log"
>> $LogFile = Join-Path $LogPath "mongod.log"
>>
>> New-Item -ItemType Directory -Force -Path $LogPath | Out-Null
>>                                                                                                                                                                                           >> $Existing = Get-Process mongod -ErrorAction SilentlyContinue                                                                                                                              >> if (-not $Existing) {                                                                                                                                                                     >>     Start-Process `                                                                                                                                                                       >>       -FilePath $MongoBin `                                                                                                                                                               >>       -ArgumentList @(                                                                                                                                                                    >>         "--dbpath", $DataPath,                                                                                                                                                            >>         "--logpath", $LogFile,                                                                                                                                                            >>         "--logappend",                                                                                                                                                                    >>         "--bind_ip", "127.0.0.1",                                                                                                                                                         >>         "--port", "27017"                                                                                                                                                                 >>       ) `                                                                                                                                                                                 >>       -WindowStyle Hidden                                                                                                                                                                 >>     Write-Host "MongoDB start requested"                                                                                                                                                  >> } else {                                                                                                                                                                                  >>     Write-Host "MongoDB already running. PID:" $Existing.Id                                                                                                                               >> }                                                                                                                                                                                         >>
>> Start-Sleep -Seconds 10
>>
>> Get-Process mongod -ErrorAction SilentlyContinue |
>>     Select-Object Id,ProcessName,Path
>>
>> Test-NetConnection 127.0.0.1 -Port 27017 |
>>     Select-Object ComputerName,RemotePort,TcpTestSucceeded
>>
>> @'
>> from pymongo import MongoClient
>>
>> run_id = "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5"
>> client = MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=10000)
>> client.admin.command("ping")
>> db = client["ecommerce_store"]
>> print("MongoDB: PASS")
>> for name in ["orders_raw", "orders_validated", "orders_quarantine"]:
>>     print(name + ":", db[name].count_documents({"run_id": run_id}))
>> print("quality metrics:", db["quality_partition_metrics"].count_documents({"run_id": run_id}))
>> client.close()
>> '@ | & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -
>>
MongoDB start requested

  Id ProcessName Path
  -- ----------- ----
4160 mongod      C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe

MongoDB: PASS
orders_raw: 30000000
orders_validated: 23664580
orders_quarantine: 6335420
quality metrics: 1


PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> $FreeGB = [math]::Round((Get-PSDrive E).Free / 1GB, 2)
>> Write-Host "Free E before Cleaning: $FreeGB GB"
>> if ($FreeGB -lt 20) {
>>     throw "المساحة الحرة أقل من 20GB؛ أوقفنا Cleaning لحماية MongoDB"
>> }
>>
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step cleaning `
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 `
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 0
>>
Free E before Cleaning: 37.01 GB
26/08/24 22:45:57 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 22:45:58 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
26/08/24 23:41:55 WARN SparkEnv: Exception while deleting Spark temp dir: E:\spark-tmp\spark-58ff2d5b-5387-45eb-a76b-7b18ae100388\userFiles-b9daf3d0-fe41-47ee-a42e-c8048f90cc11
java.io.IOException: Failed to delete: E:\spark-tmp\spark-58ff2d5b-5387-45eb-a76b-7b18ae100388\userFiles-b9daf3d0-fe41-47ee-a42e-c8048f90cc11\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.SparkEnv.stop(SparkEnv.scala:108)
        at org.apache.spark.SparkContext.$anonfun$stop$25(SparkContext.scala:2305)
        at org.apache.spark.util.Utils$.tryLogNonFatalError(Utils.scala:1375)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2305)
        at org.apache.spark.SparkContext.stop(SparkContext.scala:2211)
        at org.apache.spark.api.java.JavaSparkContext.stop(JavaSparkContext.scala:550)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:568)
        at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
        at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:374)
        at py4j.Gateway.invoke(Gateway.java:282)
        at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
        at py4j.commands.CallCommand.execute(CallCommand.java:79)
        at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
        at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
        at java.base/java.lang.Thread.run(Thread.java:842)
{
  "cleaning": {
    "step": "cleaning_after_raw_classification",
    "mode": "full_pyspark_cleaning",
    "run_id": "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5",
    "classification_order": "raw_validated_and_raw_quarantined_then_clean_quarantine",
    "cleaning_input": "orders_quarantine_only",
    "cleaning_applied": true,
    "partitions": 2,
    "requested_partitions": 2,
    "batch_size": 500,
    "raw_valid_count": 23664580,
    "raw_invalid_count": 6335420,
    "raw_loaded": 30000000,
    "initial_valid_count": 23664580,
    "initial_invalid_count": 6335420,
    "cleaned_quarantine_count": 6335420,
    "valid_count": 23664580,
    "corrected_count": 0,
    "quarantine_count": 6335420,
    "inserted_count": 0,
    "updated_count": 6335420,
    "unchanged_count": 0,
    "error_case_counts": {
      "MULTIPLE_CONFLICTING_ERRORS": 2428465,
      "INVALID_IMPOSSIBLE_DATE": 5291850,
      "INVALID_EMAIL": 207761,
      "DUPLICATE_ORDER_ID": 417584,
      "SCHEMA_REQUIRED_FIELD": 628866,
      "EMPTY_ITEMS": 208471,
      "AMBIGUOUS_NEGATIVE_VALUE": 207653,
      "INVALID_PAYMENT_STATUS": 221163,
      "INVALID_PHONE": 208594,
      "UNKNOWN_PRICE": 748443,
      "CORRUPTED_ITEMS_JSON": 208978,
      "INVALID_CURRENCY": 208736,
      "INVALID_STATUS": 208666
    },
    "elapsed_seconds": 3353.454853,
    "throughput_rows_per_second": 1889.22,
    "reconciliation_ok": true
  }
}
26/08/24 23:41:55 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-58ff2d5b-5387-45eb-a76b-7b18ae100388\userFiles-b9daf3d0-fe41-47ee-a42e-c8048f90cc11
java.io.IOException: Failed to delete: E:\spark-tmp\spark-58ff2d5b-5387-45eb-a76b-7b18ae100388\userFiles-b9daf3d0-fe41-47ee-a42e-c8048f90cc11\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
26/08/24 23:41:55 ERROR ShutdownHookManager: Exception while deleting Spark temp dir: E:\spark-tmp\spark-58ff2d5b-5387-45eb-a76b-7b18ae100388
java.io.IOException: Failed to delete: E:\spark-tmp\spark-58ff2d5b-5387-45eb-a76b-7b18ae100388\userFiles-b9daf3d0-fe41-47ee-a42e-c8048f90cc11\mongo-spark-connector_2.12-10.7.0-all.jar
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:147)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursivelyUsingJavaIO(JavaUtils.java:130)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:117)
        at org.apache.spark.network.util.JavaUtils.deleteRecursively(JavaUtils.java:90)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively(SparkFileUtils.scala:121)
        at org.apache.spark.util.SparkFileUtils.deleteRecursively$(SparkFileUtils.scala:120)
        at org.apache.spark.util.Utils$.deleteRecursively(Utils.scala:1126)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4(ShutdownHookManager.scala:65)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$4$adapted(ShutdownHookManager.scala:62)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at org.apache.spark.util.ShutdownHookManager$.$anonfun$new$2(ShutdownHookManager.scala:62)
        at org.apache.spark.util.SparkShutdownHook.run(ShutdownHookManager.scala:214)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$2(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at org.apache.spark.util.Utils$.logUncaughtExceptions(Utils.scala:1928)
        at org.apache.spark.util.SparkShutdownHookManager.$anonfun$runAll$1(ShutdownHookManager.scala:188)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at scala.util.Try$.apply(Try.scala:213)
        at org.apache.spark.util.SparkShutdownHookManager.runAll(ShutdownHookManager.scala:188)
        at org.apache.spark.util.SparkShutdownHookManager$$anon$2.run(ShutdownHookManager.scala:178)
        at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
        at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.base/java.lang.Thread.run(Thread.java:842)
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   -m py_compile src\main.py src\quality_rules.py
>>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline> $ErrorActionPreference = "Stop"
>>
>> cd "C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline"
>>
>> $FreeGB = [math]::Round((Get-PSDrive E).Free / 1GB, 2)
>> Write-Host "Free E before Cleaning: $FreeGB GB"
>> if ($FreeGB -lt 20) {
>>     throw "المساحة الحرة أقل من 20GB؛ لم يبدأ Cleaning"
>> }
>>                                                SUCCESS: The process with PID 4208 (child process of PID 12620) has been terminated.
>> $env:HADOOP_HOME = "C:\Users\PC\Desktop\big_data_progect\hadoop"
>> $env:HADOOP_HOME_DIR = $env:HADOOP_HOME
>> $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
>> $env:SPARK_LOCAL_IP = "127.0.0.1"
>> $env:PYSPARK_PYTHON = "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe"
>> $env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
>> $env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH
>>
>> $Jar = (Resolve-Path ".\tools\mongo-spark-connector_2.12-10.7.0-all.jar").Path
>>
>> & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" `
>>   src\main.py `
>>   --step cleaning `        12620 (child process of PID 3108) has been terminated.
>>   --run-id "c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5" `
>>   --mongo-uri "mongodb://127.0.0.1:27017" `
>>   --database "ecommerce_store" `
>>   --partitions 2 `
>>   --batch-size 500 ` with PID 3108 (child process of PID 16796) has been terminated.
>>   --master "local[2]" `
>>   --connector-jar "$Jar" `
>>   --reports-dir "reports" `
>>   --limit 0
>>
Free E before Cleaning: 35.68 GB
26/08/24 23:58:21 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/24 23:58:21 WARN SparkConf: Note that spark.local.dir will be overridden by the value set by the cluster manager (via SPARK_LOCAL_DIRS in mesos/standalone/kubernetes and LOCAL_DIRS in YARN).
[










>> print("quarantine audit documents:", audit_quarantine)
>>
>> if counts["orders_raw"] != 30_000_000:
>>     raise RuntimeError("orders_raw تغير؛ أوقف التنفيذ")
>> if counts["orders_validated"] + counts["orders_quarantine"] != 30_000_000:
>>     raise RuntimeError("فشل التوفيق النهائي")
>> if not cleaning_metrics:
>>     raise RuntimeError("لا توجد Cleaning metrics")
>>
>> print("FINAL COUNTS AND AUDIT CHECK: PASS")
>> client.close()
>> '@ | & "C:\Users\PC\Desktop\big_data_progect\.venv\Scripts\python.exe" -
>>
MongoDB: PASS
{'orders_quarantine': 4344604,
 'orders_raw': 30000000,
 'orders_validated': 25655396}
sum(validated + quarantine): 30000000
quality metrics documents: 3
cleaning metrics documents: 2
cleaned documents in validated: 1990816
corrected documents in validated: 1990816
validated audit documents: 1990816
quarantine audit documents: 4344604
FINAL COUNTS AND AUDIT CHECK: PASS
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>
PS C:\Users\PC\Desktop\big_data_progect\midterm1-data-pipeline>