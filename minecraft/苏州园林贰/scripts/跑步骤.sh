#!/usr/bin/env bash
# 跑步骤 <步骤号> ：生成作业 → 备份存档(备份/步骤N前) → 执行 → 报告结果 → 渲染顶视
# 用法：bash scripts/跑步骤.sh 5
set -u
N="$1"
ROOT="D:/Games/Minecraft/AI工程/苏州园林贰"
WORLD="D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\saves\苏州园林贰"
cd "$ROOT" || exit 1

SCRIPT=$(ls scripts/步骤${N}_*.mjs 2>/dev/null | head -1)
if [ -z "$SCRIPT" ]; then echo "NO_SCRIPT 步骤$N"; exit 1; fi

node "$SCRIPT" || { echo "GEN_FAIL"; exit 1; }

if [ "$N" != "1" ]; then
  robocopy "$WORLD" "D:\Games\Minecraft\AI工程\苏州园林贰\备份\步骤${N}前" //MIR //XF session.lock //NFL //NDL //NJH //NJS > /dev/null
  c=$?
  if [ $c -ge 8 ]; then echo "BACKUP_FAIL $c"; exit 1; fi
  echo "BACKUP_OK"
fi

cd "D:/Games/Minecraft/AI工程" || exit 1
node AI-Offline/Bootstrap/世界命令.mjs run-job "$ROOT/施工/步骤${N}.json" > "$ROOT/证据/步骤${N}_运行.log" 2>&1
echo "CLI_EXIT=$?"

LATEST=$(ls -t "D:/Games/Minecraft/AI工程/AI-Offline/jobs" | head -1)
python -c "
import json
r=json.load(open('D:/Games/Minecraft/AI工程/AI-Offline/jobs/$LATEST/result.json',encoding='utf-8'))
print('status',r['status'],'changed',r['changed_blocks'],'mismatches',r['mismatches'],'save',r['save_completed'])
for e in r.get('readback',[]):
    pos=e['position'][:3]; exp=e['position'][3] if len(e['position'])>3 else None
    if exp and exp!=e.get('actual'): print('MISMATCH',pos,'exp',exp,'got',e.get('actual'))
"
node "$ROOT/scripts/渲染扫描.mjs" "D:/Games/Minecraft/AI工程/AI-Offline/jobs/$LATEST/result.json" "$ROOT/证据/步骤${N}_顶视.png"
ls "D:/Games/Minecraft/AI工程/AI-Offline/runtime/executor.lock" > /dev/null 2>&1 && echo "WARN_LOCK_LEFT" || true
