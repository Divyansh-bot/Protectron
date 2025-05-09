; Inno Setup Script - Protectron Installer
[Setup]
AppName=Protectron
AppVersion=1.0
DefaultDirName={userpf}\Protectron
DefaultGroupName=Protectron
UninstallDisplayIcon={app}\Protectron.exe
Compression=lzma
SolidCompression=yes
OutputDir=.
OutputBaseFilename=Protectron_Installer
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=icon.ico

[Files]
Source: "dist\Protectron.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "models\*"; DestDir: "{app}\models"; Flags: recursesubdirs createallsubdirs
Source: "modules\*"; DestDir: "{app}\modules"; Flags: recursesubdirs createallsubdirs
Source: "data\*"; DestDir: "{app}\data"; Flags: recursesubdirs createallsubdirs
Source: "settings.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Protectron"; Filename: "{app}\Protectron.exe"
Name: "{userdesktop}\Protectron"; Filename: "{app}\Protectron.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\Protectron.exe"; Description: "Launch Protectron"; Flags: nowait postinstall skipifsilent
