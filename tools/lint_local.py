#!/usr/bin/env python3
\"\"\"Local static checks + reminder for Spyglass / datapack-linter.\"\"\"
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

def main() -> int:
    print("→ Running generator static validation…")
    sys.path.insert(0, str(ROOT))
    try:
        import generate  # type: ignore
        generate.validate(ROOT)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 1
        return code or 0
    except Exception as ex:
        print("Import/validate failed:", ex)
        print("Run instead: python generate.py")
        return 1
    print()
    print("Local static validation passed.")
    print("Full language-server lint:")
    print("  • VS Code → install Spyglass / Datapack Helper Plus")
    print("  • GitHub  → ChenCMD/datapack-linter Action (already wired)")
    print("  • Optional: https://github.com/Bertie2011/DataPackChecker")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
