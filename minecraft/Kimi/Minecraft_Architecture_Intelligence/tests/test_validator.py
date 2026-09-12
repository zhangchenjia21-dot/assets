# -*- coding: utf-8 -*-
"""test_validator — Spatial Validator 回归测试（项目代号 H · P2）。

运行（在 $OUT 根目录下）：
    py -3 -m unittest tests.test_validator -v

夹具：tests/fixtures/*.json（合成 Canonical IR，由 generate_fixtures.py 程序化生成；
测试启动时若缺失会自动重新生成）。

覆盖（任务书第 12 节：每条 HARD 规则至少一个正例 + 一个负例）：
    V001 正例 correct_entrance        负例 no_exterior_entrance
    V002 正例 correct_entrance        负例 blocked_entrance
    V003 正例 correct_entrance        负例 blocked_entrance（内部整体不可达）
    V004 正例 correct_entrance        负例 isolated_room
    V005 正例 correct_stair           负例 stair_bottom_blocked
    V006 正例 correct_stair           负例 stair_top_blocked（楼梯尽头是墙）
    V007 正例 correct_multifloor      负例 broken_vertical_access
另含：正例蓝图不得有任何 HARD_FAIL；V001–V012 全部规则必须出现在结果里。
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(ROOT / "05_SPATIAL_VALIDATOR" / "validator_source"))

from core import load_rules_config, validate_one  # noqa: E402


def _ensure_fixtures() -> None:
    need = ["correct_entrance", "blocked_entrance", "correct_stair",
            "stair_top_blocked", "stair_bottom_blocked", "isolated_room",
            "broken_vertical_access", "correct_multifloor", "no_exterior_entrance"]
    if all((FIXTURES / f"{n}.json").is_file() for n in need):
        return
    import subprocess
    subprocess.run([sys.executable, str(FIXTURES / "generate_fixtures.py")],
                   check=True)


class TestValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _ensure_fixtures()
        cls.cfg = load_rules_config()
        cls.results = {}

    @classmethod
    def result(cls, name: str) -> dict:
        if name not in cls.results:
            cls.results[name] = validate_one(FIXTURES / f"{name}.json",
                                             rules_config=cls.cfg)
        return cls.results[name]

    def rule(self, fixture: str, rid: str) -> dict:
        for r in self.result(fixture)["rules"]:
            if r["rule_id"] == rid:
                return r
        self.fail(f"{fixture} 缺少规则 {rid} 的结果")

    # ---- 结构性断言 -------------------------------------------------------
    def test_all_rules_present(self):
        """每张蓝图都输出 V001–V012 全部 12 条规则结果。"""
        r = self.result("correct_entrance")
        ids = {x["rule_id"] for x in r["rules"]}
        self.assertEqual(ids, {f"V{i:03d}" for i in range(1, 13)})
        for k in ("validation_status", "hard_fail_count", "warning_count",
                  "info_count", "rules_triggered", "walkability_score",
                  "connectivity_score", "vertical_circulation_score",
                  "validator_confidence"):
            self.assertIn(k, r)

    # ---- 正例：不得有 HARD_FAIL -------------------------------------------
    def test_correct_entrance_no_hard_fail(self):
        r = self.result("correct_entrance")
        self.assertEqual(r["hard_fail_count"], 0,
                         msg=str([x for x in r["rules"] if x["triggered"]]))

    def test_correct_stair_no_hard_fail(self):
        r = self.result("correct_stair")
        self.assertEqual(r["hard_fail_count"], 0,
                         msg=str([x for x in r["rules"] if x["triggered"]]))

    def test_correct_multifloor_no_hard_fail(self):
        r = self.result("correct_multifloor")
        self.assertEqual(r["hard_fail_count"], 0,
                         msg=str([x for x in r["rules"] if x["triggered"]]))

    # ---- V001 No Exterior Entrance ----------------------------------------
    def test_v001_positive(self):
        self.assertFalse(self.rule("correct_entrance", "V001")["triggered"])

    def test_v001_negative(self):
        r = self.rule("no_exterior_entrance", "V001")
        self.assertTrue(r["triggered"])
        self.assertEqual(r["severity"], "HARD_FAIL")

    # ---- V002 Main Entrance Blocked ---------------------------------------
    def test_v002_positive(self):
        self.assertFalse(self.rule("correct_entrance", "V002")["triggered"])

    def test_v002_negative(self):
        r = self.rule("blocked_entrance", "V002")
        self.assertTrue(r["triggered"])
        self.assertEqual(r["severity"], "HARD_FAIL")

    # ---- V003 Major Interior Unreachable ----------------------------------
    def test_v003_positive(self):
        self.assertFalse(self.rule("correct_entrance", "V003")["triggered"])

    def test_v003_negative(self):
        # 门内侧被实体柱封死 → 全部内部空间不可达
        self.assertTrue(self.rule("blocked_entrance", "V003")["triggered"])

    # ---- V004 Isolated Room / Space ---------------------------------------
    def test_v004_positive(self):
        self.assertFalse(self.rule("correct_entrance", "V004")["triggered"])

    def test_v004_negative(self):
        r = self.rule("isolated_room", "V004")
        self.assertTrue(r["triggered"])
        self.assertEqual(r["severity"], "HARD_FAIL")

    # ---- V005 Stair Bottom Blocked ----------------------------------------
    def test_v005_positive(self):
        self.assertFalse(self.rule("correct_stair", "V005")["triggered"])

    def test_v005_negative(self):
        r = self.rule("stair_bottom_blocked", "V005")
        self.assertTrue(r["triggered"])
        self.assertEqual(r["severity"], "HARD_FAIL")

    # ---- V006 Stair Top Blocked（重点：楼梯尽头是墙） ----------------------
    def test_v006_positive(self):
        self.assertFalse(self.rule("correct_stair", "V006")["triggered"])

    def test_v006_negative(self):
        r = self.rule("stair_top_blocked", "V006")
        self.assertTrue(r["triggered"])
        self.assertEqual(r["severity"], "HARD_FAIL")

    # ---- V007 Vertical Circulation Broken ---------------------------------
    def test_v007_positive(self):
        self.assertFalse(self.rule("correct_multifloor", "V007")["triggered"])

    def test_v007_negative(self):
        r = self.rule("broken_vertical_access", "V007")
        self.assertTrue(r["triggered"])
        self.assertEqual(r["severity"], "HARD_FAIL")

    # ---- 正例不被露天表面误杀（P1 教训：屋顶分量不得计入孤立房间） ---------
    def test_rooftop_component_not_counted_as_isolated_room(self):
        # correct_entrance 屋顶露天站位形成独立分量，但 V004 不得触发
        r = self.result("correct_entrance")
        self.assertGreaterEqual(r["diagnostics"]["walkable_components"], 2)
        self.assertFalse(self.rule("correct_entrance", "V004")["triggered"])


if __name__ == "__main__":
    unittest.main()
