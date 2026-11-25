#!/usr/bin/env python3
"""Launch the account generator from the compiled BR module."""
import os
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', 'python')
from midx_guard import verify
verify()
from br_engine import generate_accounts_interactive
made = generate_accounts_interactive()
print(f'\n  Generated {len(made)} account(s). Guilds are not joined automatically.')
