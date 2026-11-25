#!/usr/bin/env python3
"""Launch the compiled MIDx terminal in Termux."""
import asyncio
import os
import sys
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', 'python')
try:
    from midx_guard import verify, ensure_requirements
    verify()
    ensure_requirements()
    import midx_app
    asyncio.run(midx_app.main())
except KeyboardInterrupt:
    print('\n  Stopped.')
except Exception as exc:
    print('  Startup error: ' + str(exc), file=sys.stderr)
    raise SystemExit(1)
