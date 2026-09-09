import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "boomi-canvas-arrange.py"
SPEC = importlib.util.spec_from_file_location("boomi_canvas_arrange", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def shape(name, shapetype, *targets):
    return MODULE.Shape(
        name=name,
        shapetype=shapetype,
        dragpoints=[MODULE.Dragpoint(name=f"{name}.dp{i}", to_shape=target)
                    for i, target in enumerate(targets, start=1)],
    )


VALID_PROCESS = b'''<?xml version="1.0" encoding="UTF-8"?>
<Component xmlns:bns="http://api.platform.boomi.com/">
  <bns:object><process><shapes>
    <shape name="shape1" shapetype="start" x="0" y="0">
      <dragpoints><dragpoint name="shape1.dp1" toShape="shape2" x="0" y="0" /></dragpoints>
    </shape>
    <shape name="shape2" shapetype="stop" x="0" y="0" />
  </shapes></process></bns:object>
</Component>
'''


class CanvasArrangerTests(unittest.TestCase):
    def test_apply_positions_updates_childless_shape_element(self):
        element = MODULE.ET.Element(
            "shape", {"name": "stop", "shapetype": "stop", "x": "900", "y": "600"}
        )
        shapes = {
            "stop": MODULE.Shape(
                name="stop", shapetype="stop", x=900, y=600, element=element
            )
        }

        MODULE.apply_positions(shapes, {"stop": (240.0, 46.0)})

        self.assertEqual(element.get("x"), "240.0")
        self.assertEqual(element.get("y"), "46.0")

    def test_cycle_layout_terminates_and_positions_all_shapes(self):
        shapes = {
            "start": shape("start", "start", "loop"),
            "loop": shape("loop", "decision", "start"),
        }

        positions = MODULE.compute_layout(shapes)

        self.assertEqual(set(positions), set(shapes))
        self.assertNotEqual(positions["start"], positions["loop"])

    def test_acyclic_merge_is_after_longest_inbound_branch(self):
        shapes = {
            "start": shape("start", "start", "short", "long1"),
            "short": shape("short", "message", "merge"),
            "long1": shape("long1", "message", "long2"),
            "long2": shape("long2", "message", "merge"),
            "merge": shape("merge", "stop"),
        }

        positions = MODULE.compute_layout(shapes)

        self.assertGreater(positions["merge"][0], positions["long2"][0])

    def test_no_layout_does_not_rewrite_xml(self):
        with tempfile.TemporaryDirectory() as directory:
            process_file = Path(directory) / "process.xml"
            process_file.write_bytes(VALID_PROCESS)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(process_file), "--no-layout"],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(process_file.read_bytes(), VALID_PROCESS)
            self.assertIn("file unchanged", result.stdout)

    def test_dry_run_does_not_rewrite_xml(self):
        with tempfile.TemporaryDirectory() as directory:
            process_file = Path(directory) / "process.xml"
            process_file.write_bytes(VALID_PROCESS)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(process_file), "--dry-run"],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(process_file.read_bytes(), VALID_PROCESS)


if __name__ == "__main__":
    unittest.main()
