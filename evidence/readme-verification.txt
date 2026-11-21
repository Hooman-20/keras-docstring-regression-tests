**********************
Windows PowerShell transcript start
Start time: 20261120163109
Username: DESKTOP-QHG906B\Hooman
RunAs User: DESKTOP-QHG906B\Hooman
Configuration Name: 
Machine: DESKTOP-QHG906B (Microsoft Windows NT 10.0.26300.0)
Host Application: C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe -Command try { [Console]::OutputEncoding=[System.Text.Encoding]::UTF8 } catch {}
Set-Location -LiteralPath 'C:\Users\Hooman\OneDrive\Documentos\Deepextra\keras-docstring-regression-tests'
$env:PATH = 'C:\Users\Hooman\OneDrive\Documentos\Deepextra\keras-2422-study\python\cpython-3.11-windows-x86_64-none;' + $env:PATH
$env:PYTHONDONTWRITEBYTECODE = '1'
$readme = Get-Content README.md -Raw
$commands = [regex]::Match($readme, '(?s)```powershell\r?\n(.*?)```').Groups[1].Value
$commands | Set-Content -Encoding UTF8 evidence/readme-commands.ps1
Start-Transcript -Path evidence/readme-verification.txt
Invoke-Expression $commands
$verificationExit = $LASTEXITCODE
Stop-Transcript
if ($verificationExit -ne 0) { throw "README verification failed: $verificationExit" }
Process ID: 8088
PSVersion: 5.1.26100.9818
PSEdition: Desktop
PSCompatibleVersions: 1.0, 2.0, 3.0, 4.0, 5.0, 5.1.26100.9818
BuildVersion: 10.0.26100.9818
CLRVersion: 4.0.30319.42000
WSManStackVersion: 3.0
PSRemotingProtocolVersion: 2.3
SerializationVersion: 1.1.0.1
**********************
Transcript started, output file is evidence/readme-verification.txt




**********************
Windows PowerShell transcript end
End time: 20261120163128
**********************
