<# 
.SYNOPSIS
    OCTGN Marvel Champions LCTG FanMade pack installer

.NOTES
  Version:          0.5
  Author:           Drakhan from MARVELLOUS Discord server
  Creation Date:    02/05/2023
  Purpose/Change:   Initial script development
  
  Version History:  0.5 03/18/2023
					  [UPDATE] : Pack type check (Hero, Villain)

  Version History:  0.4 02/11/2023
                      [ADD]    : Disable ProgressBar Preference
					  [UPDATE] : Pack management
					             Errors handling
					  

.LINK 
	Marvellous Ascii Art generate with : https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
#>

# -----------------------------------------------------------------------
# -- SCRIPT
# -----------------------------------------------------------------------
#Requires -Version 5.0
[CmdletBinding()] param ()
Clear-Host
$ScriptVer = "0.5"
$Logo = @"

    _____                            .__  .__                       
   /     \ _____ __________  __ ____ |  | |  |   ____  __ __  ______
  /  \ /  \\__  \\_  __ \  \/ // __ \|  | |  |  /  _ \|  |  \/  ___/
 /    Y    \/ __ \|  | \/\   /\  ___/|  |_|  |_(  <_> )  |  /\___ \ 
 \____|__  (____  /__|    \_/  \___  >____/____/\____/|____//____  >
         \/     \/                 \/                            \/  
"@
$ScriptTitle1 = "                       MARVEL Champions LCG"
$ScriptTitle2 = "                 OCTGN FanMade Deck Installer V$($ScriptVer)"
# Disable progress bar
$OriginalProgressPreference = $Global:ProgressPreference
$Global:ProgressPreference = 'SilentlyContinue'

# -----------------------------------------------------------------------
# -- VARIABLES
# -----------------------------------------------------------------------
$ScriptPath = Split-Path -Parent $($global:MyInvocation.MyCommand.Definition)
$PacksToInstall = $null
$PackDestFolder = Join-Path -Path $ENV:Temp -ChildPath "OCTGNMarvellous"
[string]$global:OCTGNDataFolder = ""
[string]$global:OCTGNRootFolder = ""
[string]$MCModuleFolder = "055c536f-adba-4bc2-acbf-9aefb9756046"
[array]$DataFolders = "GameDatabase","ImageDatabase"
[xml]$xmlSet = $null
[bool]$VillanToCheck = $false
[int]$Counter = 1
[int]$nbErrors = 0
[array]$PackType = @("HERO","VILLAIN")

# regionFunctions
# -----------------------------------------------------------------------
# -- FUNCTIONS
# -----------------------------------------------------------------------
function KeyToExit {
	Write-Host -NoNewLine 'Press any key to continue...';
	$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
}

function Quit-Message {
	param(
		[Parameter()]
		[String]$Message,
		[switch]$ExitToPrompt
	)
	
	If($Message -match "Error") {$Prefix = " XX>";$TextColor = "Red"}
	Else {$Prefix = " .:";$TextColor = "White"}
	
	Write-Host ""
	Write-Host " $($Prefix) $($Message)" -ForegroundColor $TextColor
	Write-Host ""
	If($ExitToPrompt) {
		KeyToExit
		Exit
	}
}

function Check-OCTGNFolders {
	If ((Get-ItemProperty HKCU:\Software\OCTGN -Name Installed -ErrorAction SilentlyContinue).Installed) {
		Write-Host " .: OCTGN Found !" -ForegroundColor Yellow
		$global:OCTGNRootFolder = (Get-ItemProperty hkcu:\Software\OCTGN -Name InstallPath -ErrorAction SilentlyContinue).InstallPath
		$global:OCTGNDataFolder = Join-Path -Path $global:OCTGNRootFolder -ChildPath "Data\GameDataBase"
		Write-Verbose $global:OCTGNRootFolder
		Write-Verbose $global:OCTGNDataFolder
	}
    Else {
		Quit-Message -Message "ERROR : OCTGN not found" -ExitToPrompt
    }
    If(Test-Path -Path $(Join-Path -path $global:OCTGNDataFolder -childpath $MCModuleFolder)) {
		Write-Host " .: Marvel Champions LCG module Found !" -ForegroundColor Cyan
	}
	Else {
		Quit-Message -Message "ERROR : Marvel Champions LCG module not found !" -ExitToPrompt
	}
}

function Dialog-Box {
	Add-Type -AssemblyName System.Windows.Forms
	$FileBrowser = New-Object System.Windows.Forms.OpenFileDialog -Property @{ 
		InitialDirectory = [Environment]::GetFolderPath('UserProfile') 
		MultiSelect = $true
		Title = 'Select OCTGN pack(s) to install :'
		Filter = 'Archive (*.zip)|*.zip'
	}
	$null = $FileBrowser.ShowDialog()

	return $FileBrowser.FileNames
}

function Extract-Packs {
	param(
		[Parameter()]
		[Array]$ArchivesToExtract
	)
	
	[bool]$DatabaseFolder = $true
	[bool]$ExtractOK = $true
	
	ForEach($ArchiveFile in $ArchivesToExtract) {
		Try {
			Expand-Archive -LiteralPath $ArchiveFile -DestinationPath $PackDestFolder -Force -ErrorAction Stop
			$DataFolders | ForEach {
				If(-NOT(Test-Path $(Join-Path -Path $PackDestFolder -ChildPath $_))) {$DatabaseFolder = $false}
			}
			If(-NOT($DatabaseFolder)) {
				Remove-Item -Path $PackDestFolder -Force -Recurse -Confirm:$False
				Quit-Message -Message "Error archive $($ArchiveFile) is not an OCTGN Marvel Champions LCG FanMade pack."
				$ExtractOK = $false
			}
		}
		Catch {
			Remove-Item -Path $PackDestFolder -Force -Recurse -Confirm:$False
			Quit-Message -Message "Error during extract archive content $($ArchiveFile)"
			$ExtractOK = $false
		}
	}
	
	return $ExtractOK
}

function Check-PackID {
	param(
		[Parameter()]
		[String]$IDToCheck,
		[String]$PackName
	)
	
	[xml]$InstalledSet = Get-Content $("$global:OCTGNDataFolder\$MCModuleFolder\Sets\$IDToCheck\Set.xml")
	If($InstalledSet.Set.Name -eq $PackName) {
		$ToInstall = $true
	}
	Else {
		$ToInstall = $false
	}
	
	return $ToInstall
}
# endregion Functions

# region Main
# -----------------------------------------------------------------------
# -- MAIN
# -----------------------------------------------------------------------
Write-Host $Logo
Write-Host
Write-Host $ScriptTitle1
Write-Host $ScriptTitle2
Write-Host
Write-Host
Write-Host ". Prerequisites check ..."
Check-OCTGNFolders
$nbPack = Dialog-Box

If($nbPack.Count -eq 0) {
	Quit-Message -Message "No file have been selected." -ExitToPrompt
}

# $SetList = [collections.arraylist](Get-ChildItem -Path $global:OCTGNDataFolder\$MCModuleFolder\Sets)

Write-Host "  . $($nbPack.Count) pack(s) to install"
ForEach($Pack in $nbPack) {
	$CardSetType = $null
	$CardSetTypeToCheck = $null
	$PackColor = $null
	Write-Verbose " Source file : $($Pack)"
	Write-Host "  .. $($Counter)/$($($nbPack.Count)) -> " -NoNewLine
	If(Extract-Packs -ArchivesToExtract $Pack) {
		$PackID = Get-ChildItem -Path $(Join-Path -Path $PackDestFolder -ChildPath "GameDatabase\$($MCModuleFolder)\Sets")
		[xml]$xmlSet = Get-Content $("$($PackID.FullName)\Set.xml")
		$CardSetTypeToCheck =  ($xmlSet.set.cards.ChildNodes | where {$_.Property.Name -match "Type"})
		ForEach($CardType in $CardSetTypeToCheck) {
			If(($CardType.property | Where {$_.Name -eq "Type"}).Value -IN $PackType) {
				$CardSetType = ($CardType.property | Where {$_.Name -eq "type"}).Value.ToUpper()
				Break
			}
		}
		Switch ($CardSetType) {
			"HERO" {$PackColor = "DarkCyan"}
			"VILLAIN" {$PackColor = "Magenta"}
			dafault {$PackColor = "White"}
		}
		Write-Host "$($xmlSet.Set.Name)" -ForegroundColor $PackColor
		Write-Host "        Pack : $($CardSetType)"
		Write-Host "        ID   : $($xmlSet.set.id)"
		Write-Verbose "GameID   : $($xmlSet.set.gameid)"
		Try {
			# Copy-Item -Path "$($PackDestFolder)\*" -Destination $(Join-Path -path $env:LOCALAPPDATA -childpath "Programs\OCTGN\Data") -Recurse -Force -ErrorAction STOP
			Copy-Item -Path "$($PackDestFolder)\*" -Destination $($global:OCTGNRootFolder+"\Data") -Recurse -Force -ErrorAction STOP
		}
		Catch {
			# Catching copy error
			Quit-Message -Message "Copy error to destination folder : $($global:OCTGNRootFolder)"
			$Counter++
			$nbErrors++
			Continue
		}
	}
	Else {
		$Counter++
		$nbErrors++
		Continue
	}
	
	# Remove items in %TEMP% folder
	Remove-Item -Path $PackDestFolder -Force -Recurse -Confirm:$False
	$Counter++
}

If($nbErrors -eq 0) {
	Write-Host ""
	Write-Host " .: All packages are successfully installed." -ForegroundColor Green
}
Else {
	$PackInstalled = [int]$($nbPack.Count)
	Write-Host ""
	Write-Host " .: Some errors are found." -ForegroundColor Red 
	Write-Host " .: $($PackInstalled - $nbErrors) pack(s) successfully installed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "                        Enjoy !"
Write-Host ""

# restore progress bar preference
$Global:ProgressPreference = $OriginalProgressPreference

KeyToExit
# endregion Main