
$WshShell = New-Object -comObject WScript.Shell

# Web App Shortcut
$Shortcut1 = $WshShell.CreateShortcut("C:\Users\amfuh\Desktop\Pest and Disease Prediction Model.lnk")
$Shortcut1.TargetPath = "e:\1. AntiGravity\Pest and disesease\Pest_and_Disease_Prediction_Model.html"
$Shortcut1.WorkingDirectory = "e:\1. AntiGravity\Pest and disesease"
$Shortcut1.Description = "Launch KSNUAHS Pest and Disease Forewarning Web App"
$Shortcut1.Save()

# Updater Shortcut
$Shortcut2 = $WshShell.CreateShortcut("C:\Users\amfuh\Desktop\Update Weather Dataset (KSNUAHS).lnk")
$Shortcut2.TargetPath = "e:\1. AntiGravity\Pest and disesease\Update_Weather_Dataset.bat"
$Shortcut2.WorkingDirectory = "e:\1. AntiGravity\Pest and disesease"
$Shortcut2.Description = "Run Agromet Weather Excel Ingestion and GitHub Updater"
$Shortcut2.Save()
