Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c aws_profile_selector.bat"
oShell.Run strArgs, 0, false