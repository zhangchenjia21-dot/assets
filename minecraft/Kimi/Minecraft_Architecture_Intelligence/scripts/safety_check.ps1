$cut = Get-Date '2026-09-12 23:31'
Write-Output "cutoff = $cut"

# 1. schematics (original .litematic master library)
$sch = Get-ChildItem -Recurse -File 'D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\schematics' | Where-Object { $_.LastWriteTime -gt $cut }
Write-Output ("schematics modified/new since cutoff: " + $sch.Count)

# 2. references library
$refs = Get-ChildItem -Recurse -File 'D:\Games\Minecraft\AI工程\AI-Blueprints\references' | Where-Object { $_.LastWriteTime -gt $cut }
Write-Output ("references modified/new since cutoff: " + $refs.Count)
$refs | Select-Object -First 10 -ExpandProperty FullName

# 3. AI工程 top-level dirs last write time
Write-Output '--- AI工程 top-level LastWriteTime ---'
Get-ChildItem 'D:\Games\Minecraft\AI工程' | Select-Object Name, LastWriteTime | Format-Table -AutoSize | Out-String

# 4. saves (formal worlds) check
$savesRoot = 'D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\saves'
if (Test-Path $savesRoot) {
  $sv = Get-ChildItem -Recurse -File $savesRoot | Where-Object { $_.LastWriteTime -gt $cut }
  Write-Output ("saves modified/new since cutoff: " + $sv.Count)
} else {
  Write-Output "saves root not found: $savesRoot"
}
