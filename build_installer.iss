#define MyAppName "Agent Cripto TDR"
#define MyAppVersion "0.4"
#define MyAppPublisher "Projecte educatiu TDR"

[Setup]
AppId={{A7A84326-8B14-4D87-98F7-4FC2F7F0D0D2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\Agent Cripto TDR
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=Agent_Cripto_TDR_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "app\*"; DestDir: "{app}\app"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "setup.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "INICIAR_AGENT.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "INSTAL_LAR_AGENT.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "DESINSTAL_LAR_AGENT.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "VERSIO.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\Agent Cripto TDR"; Filename: "{app}\INICIAR_AGENT.bat"; WorkingDir: "{app}"
Name: "{group}\Agent Cripto TDR"; Filename: "{app}\INICIAR_AGENT.bat"; WorkingDir: "{app}"

[Run]
Filename: "{app}\INSTAL_LAR_AGENT.bat"; Description: "Instal·lar Python, Streamlit i dependències"; Flags: postinstall waituntilterminated
