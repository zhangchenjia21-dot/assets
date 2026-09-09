Get-CimInstance Win32_Process -Filter "ProcessId=51736 or ProcessId=54720" | ForEach-Object {
  $cmd = $_.CommandLine
  if ($cmd -and $cmd.Length -gt 300) { $cmd = $cmd.Substring(0, 300) }
  Write-Output ("PID=" + $_.ProcessId + " NAME=" + $_.Name)
  Write-Output ("CMD=" + $cmd)
  Write-Output "---"
}
