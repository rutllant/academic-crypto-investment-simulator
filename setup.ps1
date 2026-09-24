$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$AppDir = $PSScriptRoot
$RuntimeRoot = Join-Path $env:LOCALAPPDATA 'AgentCriptoTDR\Runtime'
$PythonDir = Join-Path $RuntimeRoot 'Python313'
$PythonExe = Join-Path $PythonDir 'python.exe'
$VenvDir = Join-Path $AppDir '.venv'
$VenvPython = Join-Path $VenvDir 'Scripts\python.exe'
$Requirements = Join-Path $AppDir 'requirements.txt'
$LogFile = Join-Path $AppDir 'install.log'
$PythonVersion = '3.13.11'
$PythonInstallerUrl = "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-amd64.exe"
$TempInstaller = Join-Path $env:TEMP "python-$PythonVersion-amd64.exe"

function Log([string]$Message) {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $line = "[$stamp] $Message"
    Write-Host $Message
    Add-Content -LiteralPath $LogFile -Value $line -Encoding UTF8
}

function Test-Modules {
    if (-not (Test-Path $VenvPython)) { return $false }
    & $VenvPython -c "import streamlit, pandas, numpy, plotly, ccxt; print('OK')" *> $null
    return ($LASTEXITCODE -eq 0)
}

try {
    New-Item -ItemType Directory -Force -Path $RuntimeRoot | Out-Null
    "" | Set-Content -LiteralPath $LogFile -Encoding UTF8

    Log '======================================================'
    Log 'AGENT CRIPTO TDR - PREPARACIO AUTOMATICA'
    Log '======================================================'
    Log "Carpeta de l'aplicacio: $AppDir"

    if (-not (Test-Path $PythonExe)) {
        Log "Descarregant Python $PythonVersion (64 bits) des de python.org..."
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $PythonInstallerUrl -OutFile $TempInstaller -UseBasicParsing

        Log 'Instal·lant Python de forma silenciosa i nomes per a aquest usuari...'
        $arguments = @(
            '/quiet',
            'InstallAllUsers=0',
            'PrependPath=0',
            'Include_launcher=0',
            'Include_test=0',
            'Include_doc=0',
            'Include_tcltk=0',
            'Shortcuts=0',
            'AssociateFiles=0',
            "TargetDir=$PythonDir"
        )
        $p = Start-Process -FilePath $TempInstaller -ArgumentList $arguments -Wait -PassThru
        if ($p.ExitCode -ne 0) {
            throw "L'instal·lador de Python ha retornat el codi $($p.ExitCode)."
        }
        Remove-Item -LiteralPath $TempInstaller -Force -ErrorAction SilentlyContinue
    } else {
        Log 'Python dedicat ja esta instal·lat.'
    }

    if (-not (Test-Path $PythonExe)) {
        throw "No s'ha trobat python.exe despres de la instal·lacio."
    }

    Log 'Comprovant Python...'
    & $PythonExe --version | Tee-Object -FilePath $LogFile -Append | Out-Host

    if (-not (Test-Path $VenvPython)) {
        Log 'Creant l entorn privat de l aplicacio...'
        & $PythonExe -m venv $VenvDir
        if ($LASTEXITCODE -ne 0) { throw 'No s ha pogut crear l entorn virtual.' }
    } else {
        Log 'L entorn privat ja existeix.'
    }

    Log 'Actualitzant pip...'
    & $VenvPython -m pip install --disable-pip-version-check --upgrade pip setuptools wheel 2>&1 | Tee-Object -FilePath $LogFile -Append | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'Error actualitzant pip.' }

    Log 'Instal·lant Streamlit i totes les dependències de l Agent...'
    & $VenvPython -m pip install --disable-pip-version-check -r $Requirements 2>&1 | Tee-Object -FilePath $LogFile -Append | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'Error instal·lant les dependències.' }

    Log 'Verificant Streamlit, pandas, numpy, Plotly i CCXT...'
    if (-not (Test-Modules)) {
        Log 'La verificacio ha fallat. Reintentant la instal·lacio de dependències...'
        & $VenvPython -m pip install --disable-pip-version-check --upgrade --force-reinstall -r $Requirements 2>&1 | Tee-Object -FilePath $LogFile -Append | Out-Host
        if ($LASTEXITCODE -ne 0 -or -not (Test-Modules)) {
            throw 'Les dependències no han superat la verificacio final.'
        }
    }

    Log 'Creant acces directe a l escriptori...'
    $WshShell = New-Object -ComObject WScript.Shell
    $Desktop = [Environment]::GetFolderPath('Desktop')
    $ShortcutPath = Join-Path $Desktop 'Agent Cripto TDR.lnk'
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = Join-Path $AppDir 'INICIAR_AGENT.bat'
    $Shortcut.WorkingDirectory = $AppDir
    $Shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,14"
    $Shortcut.Description = 'Agent inversor simulat - TDR'
    $Shortcut.Save()

    @(
        "Agent Cripto TDR preparat correctament",
        "Data: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
        "Python: $PythonVersion",
        "Streamlit: instal·lat i verificat"
    ) | Set-Content -LiteralPath (Join-Path $AppDir '.install_ok') -Encoding UTF8

    Log '======================================================'
    Log 'INSTAL·LACIO COMPLETADA CORRECTAMENT'
    Log 'Python + Streamlit + dependències: OK'
    Log '======================================================'
    Write-Host ''
    Write-Host 'Ja pots iniciar l Agent Cripto des de l acces directe de l escriptori.' -ForegroundColor Green
    exit 0
}
catch {
    Log "ERROR: $($_.Exception.Message)"
    Log "Consulta el fitxer install.log: $LogFile"
    Write-Host ''
    Write-Host 'La instal·lacio no s ha pogut completar.' -ForegroundColor Red
    Write-Host 'Cal connexio a Internet durant la primera instal·lacio.'
    exit 1
}
