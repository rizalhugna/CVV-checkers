#!/usr/bin/env python3
import sys, base64, zlib, marshal
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from io import StringIO

class LicenseBypass:
    """Intercept license prompts and auto-bypass them"""
    def __init__(self, original_input):
        self.original_input = original_input
        self.license_detected = False
        
    def __call__(self, prompt=''):
        if 'license' in str(prompt).lower() or 'key' in str(prompt).lower():
            print(prompt, end='', flush=True)
            print("BYPASSED")
            return "bypassed"
        return self.original_input(prompt)

def aesgcm_decrypt(blob: bytes, key: bytes) -> bytes:
    nonce = blob[:12]
    ct = blob[12:]
    return AESGCM(key).decrypt(nonce, ct, associated_data=None)

try:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    mods = base / "modules"
    files = sorted(mods.glob("p*.bin"))
    blob = b"".join(p.read_bytes() for p in files)
    
    if b"." not in blob:
        sys.exit(1)
    
    sig_b64, enc_b64, sym_b64 = blob.split(b".", 2)
    enc = base64.b64decode(enc_b64)
    sym_key = base64.b64decode(sym_b64)

    data = zlib.decompress(aesgcm_decrypt(enc, sym_key))
    try:
        code = marshal.loads(data)
    except Exception:
        code = compile(data.decode('utf-8'), "<run>", "exec")
    
    # Bypass license by intercepting input()
    bypass = LicenseBypass(__builtins__['input'])
    exec(code, {'__name__': '__main__', 'input': bypass})
    
except Exception as e:
    sys.exit(1)
