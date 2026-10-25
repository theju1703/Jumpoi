Set-Location "C:\Users\Thejeshwharan\OneDrive\Desktop\3Qspace\Jumpoi"
$pyPath = "C:\Users\Thejeshwharan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (Test-Path $pyPath) {
    & $pyPath start_erp.py $args
} else {
    python start_erp.py $args
}
