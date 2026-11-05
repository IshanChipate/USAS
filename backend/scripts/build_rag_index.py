"""Build the local FAISS index from documents in data/knowledge_base."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.services.rag_service import build_index


if __name__ == "__main__":
    print(json.dumps(build_index(), indent=2))
