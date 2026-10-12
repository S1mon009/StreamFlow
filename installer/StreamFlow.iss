#ifndef AppVersion
  #define AppVersion "0.1.0"
#endif

[Setup]
AppId={{B9B1E7A0-6D17-4D76-9E18-4178B5A32F0C}
AppName=StreamFlow
AppVersion={#AppVersion}
DefaultDirName={autopf}\StreamFlow
DefaultGroupName=StreamFlow
DisableProgramGroupPage=yes
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
OutputDir=..\release
OutputBaseFilename=StreamFlow-Setup-{#AppVersion}
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\StreamFlow.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "..\dist\StreamFlow\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\StreamFlow"; Filename: "{app}\StreamFlow.exe"

[Run]
Filename: "{app}\StreamFlow.exe"; Description: "Launch StreamFlow"; Flags: postinstall skipifsilent
