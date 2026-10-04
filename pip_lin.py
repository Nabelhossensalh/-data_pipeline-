
import os
import sys
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime


# ============================================================
# SAME AS:
# $ErrorActionPreference = "Stop"
# ============================================================

# Python stops immediately whenever we explicitly raise an error.


# ============================================================
# PROJECT PATHS
# ============================================================

# Same as:
# $ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
ProjectRoot = Path(__file__).resolve().parent

# Same as:
# $BaseRoot = Split-Path -Parent $ProjectRoot
BaseRoot = ProjectRoot.parent

# Same as:
# $PythonExe = Join-Path $BaseRoot ".venv\Scripts\python.exe"
PythonExe = BaseRoot / ".venv" / "Scripts" / "python.exe"

# Same as:
# $MainScript = Join-Path $ProjectRoot "src\main.py"
MainScript = ProjectRoot / "src" / "main.py"

# Same as:
# $HadoopHome = Join-Path $BaseRoot "hadoop"
HadoopHome = BaseRoot / "hadoop"

# Same as:
# $ConnectorJar = Join-Path `
#     $ProjectRoot `
#     "tools\mongo-spark-connector_2.12-10.7.0-all.jar"
ConnectorJar = (
    ProjectRoot
    / "tools"
    / "mongo-spark-connector_2.12-10.7.0-all.jar"
)

# Same as:
# $MongoBin = "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
MongoBin = Path(
    r"C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe"
)

# Same as:
# $MongoData = "E:\mongodb-project-data"
MongoData = Path(r"E:\mongodb-project-data")

# Same as:
# $MongoLogDir = "E:\mongodb-project-log"
MongoLogDir = Path(r"E:\mongodb-project-log")

# Same as:
# $MongoLog = Join-Path $MongoLogDir "mongod.log"
MongoLog = MongoLogDir / "mongod.log"


# ============================================================
# INPUT FILE
# ============================================================

# Same as:
# $InputFile="C:\Users\PC\Desktop\big_data_progect\01_student_test_small.csv"

InputFile = Path(
    r"C:\Users\PC\Desktop\big_data_progect\01_student_test_small.csv"
)

# Same as:
# $InputPath = [System.IO.Path]::GetFullPath($InputFile)

InputPath = InputFile.resolve()


# ============================================================
# WRITE-HOST
# ============================================================

print("=== ONE FILE HYBRID PIPELINE ===")
print(f"Project: {ProjectRoot}")


# ============================================================
# INPUT VALIDATION
# ============================================================

# Same as:
#
# if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) {
#     throw "Input file does not exist: $InputPath"
# }

if not InputPath.is_file():
    raise RuntimeError(
        f"Input file does not exist: {InputPath}"
    )


# Same as:
#
# if ([System.IO.Path]::GetExtension($InputPath).ToLowerInvariant() -ne ".csv") {
#     throw "Input file must have a .csv extension: $InputPath"
# }

if InputPath.suffix.lower() != ".csv":
    raise RuntimeError(
        f"Input file must have a .csv extension: {InputPath}"
    )


# Same as:
#
# if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
#     throw "Python executable not found: $PythonExe"
# }

if not PythonExe.is_file():
    raise RuntimeError(
        f"Python executable not found: {PythonExe}"
    )


# Same as:
#
# if (-not (Test-Path -LiteralPath $MainScript -PathType Leaf)) {
#     throw "main.py not found: $MainScript"
# }

if not MainScript.is_file():
    raise RuntimeError(
        f"main.py not found: {MainScript}"
    )


# Same as:
#
# if (-not (Test-Path -LiteralPath $ConnectorJar -PathType Leaf)) {
#     throw "MongoDB Spark Connector not found: $ConnectorJar"
# }

if not ConnectorJar.is_file():
    raise RuntimeError(
        f"MongoDB Spark Connector not found: {ConnectorJar}"
    )


# Same as:
#
# if (-not (Test-Path -LiteralPath $HadoopHome)) {
#     throw "HADOOP_HOME not found: $HadoopHome"
# }

if not HadoopHome.exists():
    raise RuntimeError(
        f"HADOOP_HOME not found: {HadoopHome}"
    )


# Same as:
#
# if (-not (Test-Path -LiteralPath $MongoData)) {
#     throw "MongoDB data path not found: $MongoData"
# }

if not MongoData.exists():
    raise RuntimeError(
        f"MongoDB data path not found: {MongoData}"
    )


# ============================================================
# CREATE MONGO LOG DIRECTORY
# ============================================================

# Same as:
#
# New-Item -ItemType Directory -Force -Path $MongoLogDir | Out-Null

MongoLogDir.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# CHECK WHETHER MONGODB IS ALREADY RUNNING
# ============================================================

# PowerShell:
#
# $MongoProcess = Get-Process mongod -ErrorAction SilentlyContinue

def get_mongo_processes():
    """
    Equivalent to:
        Get-Process mongod -ErrorAction SilentlyContinue

    Returns the Windows process IDs of mongod.exe.
    """

    result = subprocess.run(
        [
            "tasklist",
            "/FI",
            "IMAGENAME eq mongod.exe",
            "/FO",
            "CSV",
            "/NH"
        ],
        capture_output=True,
        text=True,
        check=False
    )

    processes = []

    if result.returncode != 0:
        return processes

    for line in result.stdout.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith('"mongod.exe"'):

            parts = [
                x.strip('"')
                for x in line.split('","')
            ]

            if len(parts) >= 2:

                try:
                    processes.append(
                        int(parts[1])
                    )
                except ValueError:
                    pass

    return processes


MongoProcesses = get_mongo_processes()


# ============================================================
# START MONGODB IF NOT RUNNING
# ============================================================

# PowerShell:
#
# if (-not $MongoProcess) {
#     Write-Host "Starting MongoDB..."
#
#     Start-Process `
#         -FilePath $MongoBin `
#         -ArgumentList @(
#             "--dbpath", $MongoData,
#             "--logpath", $MongoLog,
#             "--logappend",
#             "--bind_ip", "127.0.0.1",
#             "--port", "27017"
#         ) `
#         -WindowStyle Hidden
#
# } else {
#     Write-Host "MongoDB is already running. PID: $($MongoProcess.Id)"
# }

if not MongoProcesses:

    print("Starting MongoDB...")

    MongoArguments = [
        "--dbpath",
        str(MongoData),

        "--logpath",
        str(MongoLog),

        "--logappend",

        "--bind_ip",
        "127.0.0.1",

        "--port",
        "27017"
    ]

    # Equivalent to Start-Process with WindowStyle Hidden.
    #
    # CREATE_NO_WINDOW prevents a console window from appearing.

    subprocess.Popen(
        [str(MongoBin)] + MongoArguments,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

else:

    # PowerShell prints the first/all IDs depending on interpolation.
    # We use the first PID for equivalent information.

    print(
        f"MongoDB is already running. "
        f"PID: {MongoProcesses[0]}"
    )


# ============================================================
# WAIT FOR MONGODB
# ============================================================

# PowerShell:
#
# $MongoReady = $false
#
# for ($i = 1; $i -le 30; $i++) {
#
#     Start-Sleep -Seconds 1
#
#     $Test = Test-NetConnection `
#         127.0.0.1 `
#         -Port 27017 `
#         -WarningAction SilentlyContinue
#
#     if ($Test.TcpTestSucceeded) {
#         $MongoReady = $true
#         break
#     }
# }

MongoReady = False

for _ in range(30):

    time.sleep(1)

    try:

        with socket.create_connection(
            ("127.0.0.1", 27017),
            timeout=1
        ):
            MongoReady = True
            break

    except OSError:
        pass


# Same as:
#
# if (-not $MongoReady) {
#     throw "MongoDB is not ready on 127.0.0.1:27017. Check $MongoLog"
# }

if not MongoReady:

    raise RuntimeError(
        "MongoDB is not ready on "
        "127.0.0.1:27017. "
        f"Check {MongoLog}"
    )


print("MongoDB: PASS")


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

# Same as:
#
# $env:HADOOP_HOME = $HadoopHome

os.environ["HADOOP_HOME"] = str(HadoopHome)


# Same as:
#
# $env:HADOOP_HOME_DIR = $HadoopHome

os.environ["HADOOP_HOME_DIR"] = str(HadoopHome)


# Same as:
#
# $env:SPARK_LOCAL_DIRS = "E:\spark-tmp"

os.environ["SPARK_LOCAL_DIRS"] = r"E:\spark-tmp"


# Same as:
#
# $env:SPARK_LOCAL_IP = "127.0.0.1"

os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"


# Same as:
#
# $env:PYSPARK_PYTHON = $PythonExe

os.environ["PYSPARK_PYTHON"] = str(PythonExe)


# Same as:
#
# $env:PYSPARK_DRIVER_PYTHON = $PythonExe

os.environ["PYSPARK_DRIVER_PYTHON"] = str(PythonExe)


# Same as:
#
# $env:PATH = "$HadoopHome\bin;" + $env:PATH

os.environ["PATH"] = (
    str(HadoopHome / "bin")
    + ";"
    + os.environ.get("PATH", "")
)


# ============================================================
# REPORT DIRECTORY
# ============================================================

# Same as:
#
# $Stamp = Get-Date -Format "yyyyMMdd_HHmmss"

Stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)


# Same as:
#
# $ReportsDir = Join-Path `
#     $ProjectRoot `
#     "reports\doctor_$Stamp"

ReportsDir = (
    ProjectRoot
    / "reports"
    / f"doctor_{Stamp}"
)
TestDatabase = f"big_data_student_test_{Stamp}"


# Same as:
#
# New-Item `
#     -ItemType Directory `
#     -Force `
#     -Path $ReportsDir |
#     Out-Null

ReportsDir.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DISPLAY SAME INFORMATION
# ============================================================

print(f"Input: {InputPath}")
print("Threshold: 200 MB")
print("Engine: auto")
print(
    "Pipeline: discover, raw-load, "
    "quality, cleaning, metrics"
)
print(f"Reports: {ReportsDir}")
print(f"MongoDB test database: {TestDatabase}")
print("Starting main.py end-to-end...")


# ============================================================
# SET LOCATION
# ============================================================

# PowerShell:
#
# Set-Location $ProjectRoot

os.chdir(ProjectRoot)


# ============================================================
# EXACT SAME ARGUMENTS
# ============================================================

# PowerShell:
#
# $Arguments = @(
#     "src\main.py",
#     "--step", "all",
#     "--input", $InputPath,
#     "--engine", "auto",
#     "--threshold-mb", "200",
#     "--storage-backend", "auto",
#     "--partitions", "0",
#     "--batch-size", "500",
#     "--master", "auto",
#     "--connector-jar", $ConnectorJar,
#     "--reports-dir", $ReportsDir,
#     "--limit", "0"
# )

Arguments = [
    "src\\main.py",

    "--step",
    "all",

    "--input",
    str(InputPath),

    "--engine",
    "auto",

    "--threshold-mb",
    "200",

    "--storage-backend",
    "auto",

    "--database",
    TestDatabase,

    "--partitions",
    "0",

    "--batch-size",
    "500",

    "--master",
    "auto",

    "--connector-jar",
    str(ConnectorJar),

    "--reports-dir",
    str(ReportsDir),

    "--limit",
    "0"

    
]


# ============================================================
# EXACT PYTHON EXECUTION
# ============================================================

# PowerShell:
#
# & $PythonExe @Arguments

Result = subprocess.run(
    [
        str(PythonExe)
    ] + Arguments,
    cwd=str(ProjectRoot),
    env=os.environ.copy(),
    check=False
)


# ============================================================
# EXIT CODE
# ============================================================

# PowerShell:
#
# $ExitCode = $LASTEXITCODE

ExitCode = Result.returncode


# ============================================================
# FAILURE
# ============================================================

# PowerShell:
#
# if ($ExitCode -ne 0) {
#     throw "main.py failed with exit code $ExitCode. Check $ReportsDir\error.json"
# }

if ExitCode != 0:

    raise RuntimeError(
        f"main.py failed with exit code {ExitCode}. "
        f"Check {ReportsDir / 'error.json'}"
    )


# ============================================================
# SUCCESS
# ============================================================

# PowerShell:
#
# Write-Host "PIPELINE COMPLETED: PASS"
# Write-Host "Reports saved in: $ReportsDir"

print("PIPELINE COMPLETED: PASS")
print(f"Reports saved in: {ReportsDir}")
