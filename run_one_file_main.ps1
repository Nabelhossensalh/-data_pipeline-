$ErrorActionPreference = "Stop"

# Project paths
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseRoot = Split-Path -Parent $ProjectRoot
$PythonExe = Join-Path $BaseRoot ".venv\Scripts\python.exe"
$MainScript = Join-Path $ProjectRoot "src\main.py"
$HadoopHome = Join-Path $BaseRoot "hadoop"
$ConnectorJar = Join-Path $ProjectRoot "tools\mongo-spark-connector_2.12-10.7.0-all.jar"
$MongoBin = "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
$MongoData = "E:\mongodb-project-data"
$MongoLogDir = "E:\mongodb-project-log"
$MongoLog = Join-Path $MongoLogDir "mongod.log"

Write-Host "=== ONE FILE HYBRID PIPELINE ==="
Write-Host "Project: $ProjectRoot"

# Set the CSV path here. Change only this line for another file.
$InputFile = "C:\Users\PC\Desktop\big_data_progect\UsedCarsSA_Unclean_EN.csv"
$InputPath = [System.IO.Path]::GetFullPath($InputFile)

if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) {
    throw "Input file does not exist: $InputPath"
}
if ([System.IO.Path]::GetExtension($InputPath).ToLowerInvariant() -ne ".csv") {
    throw "Input file must have a .csv extension: $InputPath"
}
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python executable not found: $PythonExe"
}
if (-not (Test-Path -LiteralPath $MainScript -PathType Leaf)) {
    throw "main.py not found: $MainScript"
}
if (-not (Test-Path -LiteralPath $ConnectorJar -PathType Leaf)) {
    throw "MongoDB Spark Connector not found: $ConnectorJar"
}
if (-not (Test-Path -LiteralPath $HadoopHome)) {
    throw "HADOOP_HOME not found: $HadoopHome"
}
if (-not (Test-Path -LiteralPath $MongoData)) {
    throw "MongoDB data path not found: $MongoData"
}

New-Item -ItemType Directory -Force -Path $MongoLogDir | Out-Null

# Start MongoDB if it is not already running.
$MongoProcess = Get-Process mongod -ErrorAction SilentlyContinue
if (-not $MongoProcess) {
    Write-Host "Starting MongoDB..."
    Start-Process `
        -FilePath $MongoBin `
        -ArgumentList @(
            "--dbpath", $MongoData,
            "--logpath", $MongoLog,
            "--logappend",
            "--bind_ip", "127.0.0.1",
            "--port", "27017"
        ) `
        -WindowStyle Hidden
} else {
    Write-Host "MongoDB is already running. PID: $($MongoProcess.Id)"
}

$MongoReady = $false
for ($i = 1; $i -le 30; $i++) {
    Start-Sleep -Seconds 1
    $Test = Test-NetConnection 127.0.0.1 -Port 27017 -WarningAction SilentlyContinue
    if ($Test.TcpTestSucceeded) {
        $MongoReady = $true
        break
    }
}
if (-not $MongoReady) {
    throw "MongoDB is not ready on 127.0.0.1:27017. Check $MongoLog"
}
Write-Host "MongoDB: PASS"

$env:HADOOP_HOME = $HadoopHome
$env:HADOOP_HOME_DIR = $HadoopHome
$env:SPARK_LOCAL_DIRS = "E:\spark-tmp"
$env:SPARK_LOCAL_IP = "127.0.0.1"
$env:PYSPARK_PYTHON = $PythonExe
$env:PYSPARK_DRIVER_PYTHON = $PythonExe
$env:PATH = "$HadoopHome\bin;" + $env:PATH

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ReportsDir = Join-Path $ProjectRoot "reports\doctor_$Stamp"
New-Item -ItemType Directory -Force -Path $ReportsDir | Out-Null

Write-Host "Input: $InputPath"
Write-Host "Threshold: 200 MB"
Write-Host "Engine: auto"
Write-Host "Pipeline: discover, raw-load, quality, cleaning, metrics"
Write-Host "Reports: $ReportsDir"
Write-Host "Starting main.py end-to-end..."

Set-Location $ProjectRoot

$Arguments = @(
    "src\main.py",
    "--step", "all",
    "--input", $InputPath,
    "--engine", "auto",
    "--threshold-mb", "200",
    "--storage-backend", "auto",
    "--partitions", "0",
    "--batch-size", "500",
    "--master", "auto",
    "--connector-jar", $ConnectorJar,
    "--reports-dir", $ReportsDir,
    "--limit", "0"
)

& $PythonExe @Arguments
$ExitCode = $LASTEXITCODE

if ($ExitCode -ne 0) {
    throw "main.py failed with exit code $ExitCode. Check $ReportsDir\error.json"
}

Write-Host "PIPELINE COMPLETED: PASS"
Write-Host "Reports saved in: $ReportsDir"
