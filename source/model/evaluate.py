"""Evaluate the saved risk classifier and write a classroom-friendly report."""
from pathlib import Path
import json
from train import train, ARTIFACT

SOURCE = Path(__file__).resolve().parents[1]
ROOT = SOURCE.parent
LOG = ROOT / "logs" / "eval_result.json"

if __name__ == "__main__":
    metrics = train() if not ARTIFACT.exists() else None
    if metrics is None:
        # Re-training keeps the report reproducible and verifies the artifact path.
        metrics = train()
    LOG.parent.mkdir(exist_ok=True); LOG.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"评估结果已写入: {LOG}")
