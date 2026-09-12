"""将当前 R1 等比例聚落图发布到既有 Owner 入口，避免旧四节点示意误导。"""
from pathlib import Path
import shutil
p=Path(__file__).resolve().parent
shutil.copyfile(p.parent/'visual/settlement-hierarchy.png',p/'中域规划示意图.png')
