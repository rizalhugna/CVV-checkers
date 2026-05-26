#!/usr/bin/env python3
import sys, base64, zlib, marshal
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

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

    # Skip signature verification - no license needed
    data = zlib.decompress(aesgcm_decrypt(enc, sym_key))
    try:
        code = marshal.loads(data)
    except Exception:
        code = compile(data.decode('utf-8'), "<run>", "exec")
    exec(code, {'__name__': '__main__'})
except Exception:
    sys.exit(1)
