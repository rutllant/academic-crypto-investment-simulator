#define MyAppName "Academic FX Investment Simulator"
#define MyAppPublisher "Projecte educatiu TDR"
#define MyAppURL "https://github.com/rutllant/academic-crypto-investment-simulator"
#define MyAppVersion GetEnv("APP_VERSION")
#define SourceDir GetEnv("SOURCE_DIR")

[Setup]
AppId={{A7A84326-8B14-4D87-98F7-4FC2F7F0D0D2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\Programs\Academic FX Investment Simulator
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=Agent_FX_TDR_Setup_v{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName={#MyAppName}

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Crear un accés directe a l'escriptori"; GroupDescription: "Accessos directes:"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\INICIAR_AGENT.bat"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\INICIAR_AGENT.bat"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\INICIAR_AGENT.bat"; Description: "Iniciar {#MyAppName}"; Flags: postinstall nowait skipifsilent
