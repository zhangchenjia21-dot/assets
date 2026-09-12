$ErrorActionPreference='Stop'
$root='D:\Games\Minecraft\AI工程'
$work="$root\AI-Blueprints\interop-test"
$probe="$root\T12正式入库\原生探针"
$evidence="$root\T12正式入库"
$instance="$root\..\.minecraft\versions\26.2-Fabric 0.19.5"
$jdk='D:\Games\Minecraft\AI工程\AI-Test\Minecraft-AI-Fabric-26.2-Test\runtime\jdk-25.0.4.1+1\bin'
$profile=Get-Content -LiteralPath "$instance\26.2-Fabric 0.19.5.json" -Raw|ConvertFrom-Json
$jars=@("$instance\26.2-Fabric 0.19.5.jar")
foreach($lib in $profile.libraries){
 $relative=$lib.downloads.artifact.path
 if(!$relative){$p=$lib.name.Split(':');$relative=$p[0].Replace('.','/')+'/'+$p[1]+'/'+$p[2]+'/'+$p[1]+'-'+$p[2]+'.jar'}
 $file=Join-Path "$root\..\.minecraft\libraries" $relative
 if(Test-Path -LiteralPath $file){$jars+=$file}
}
$classpath=($jars|Select-Object -Unique)-join ';'
New-Item -ItemType Directory -Force "$probe\mods","$probe\classes"|Out-Null
# 仅复制已安装的读取器及必要依赖到独立探针目录，不安装到 Owner，不加载任何 Bridge。
$mods=Get-ChildItem -LiteralPath "$instance\mods" -File |Where-Object {$_.Name -like '*litematica*.jar' -or $_.Name -like 'malilib*.jar' -or $_.Name -like 'fabric-api-*.jar'}
foreach($mod in $mods){Copy-Item -LiteralPath $mod.FullName -Destination "$probe\mods" -Force}
$cp=$classpath+';'+(($mods|ForEach-Object FullName)-join ';')
& "$jdk\javac.exe" -proc:none -encoding UTF-8 -cp $cp -d "$probe\classes" "$PSScriptRoot\投影加载探针.java"
if($LASTEXITCODE -ne 0){throw 'Probe compilation failed'}
$metadata='{"schemaVersion":1,"id":"litematica_interop_probe","version":"0.6.0","environment":"client","entrypoints":{"preLaunch":["probe.投影加载探针"]}}'
$escaped=[regex]::Replace($metadata,'[^\x00-\x7F]',{param($m)'\u'+([int][char]$m.Value).ToString('x4')})
[IO.File]::WriteAllText("$probe\classes\fabric.mod.json",$escaped,[Text.Encoding]::ASCII)
& "$jdk\jar.exe" --create --file "$probe\mods\interop-probe.jar" -C "$probe\classes" .
if($LASTEXITCODE -ne 0){throw 'Probe packaging failed'}
Push-Location $probe
try{
 & "$jdk\java.exe" '-Dfile.encoding=UTF-8' "-Dv6.evidence=$evidence" '-Xmx2G' '-cp' $classpath 'net.fabricmc.loader.impl.launch.knot.KnotClient' '--gameDir' $probe '--version' '26.2' '--username' 'FileReadProbe' '--accessToken' '0' '--assetsDir' "$root\..\.minecraft\assets" 1> "$evidence\native-loader-stdout.log" 2> "$evidence\native-loader-stderr.log"
 if($LASTEXITCODE -ne 0){throw "Probe exited: $LASTEXITCODE"}
 if(!(Select-String -LiteralPath "$evidence\native-loader-stdout.log" -Pattern 'V6A_NATIVE_LITEMATICA_LOAD_PASS_NO_WORLD_OPENED' -Quiet)){throw 'Missing pass marker'}
 'V6A_NATIVE_LITEMATICA_LOAD_PASS_NO_WORLD_OPENED'
}finally{Pop-Location}
