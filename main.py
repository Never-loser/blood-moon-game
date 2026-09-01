"""Blood Moon Ritual — entry point.

Run with:  python main.py
Optional:  python main.py --windowed   (debug window instead of fullscreen)
"""
from __future__ import annotations

import sys


def main() -> None:
    from game.app import BloodMoonApp

    app = BloodMoonApp(windowed="--windowed" in sys.argv)
    try:
        app.run()
    except Exception:
        import traceback

        traceback.print_exc()
        try:
            app.quit()
        except Exception:
            pass
        raise


if __name__ == "__main__":
    main()
