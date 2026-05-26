#!/usr/bin/env python3
import sys, base64, zlib, marshal, traceback
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class LicenseBypass:
    """Intercept license prompts and auto-bypass them"""
    def __init__(self, original_input):
        self.original_input = original_input
        
    def __call__(self, prompt=''):
        prompt_str = str(prompt).lower()
        if 'license' in prompt_str or 'key' in prompt_str or 'device' in prompt_str:
            print(prompt, end='', flush=True)
            print("BYPASSED_AUTO")
            return "bypassed_auto_key_12345"
        return self.original_input(prompt)

def aesgcm_decrypt(blob: bytes, key: bytes) -> bytes:
    nonce = blob[:12]
    ct = blob[12:]
    return AESGCM(key).decrypt(nonce, ct, associated_data=None)

try:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    print(f"[*] Base path: {base}")
    
    mods = base / "modules"
    print(f"[*] Looking for modules in: {mods}")
    
    if not mods.exists():
        print(f"[ERROR] Modules folder not found at {mods}")
        sys.exit(1)
    
    files = sorted(mods.glob("p*.bin"))
    print(f"[*] Found {len(files)} module files: {[f.name for f in files]}")
    
    if not files:
        print("[ERROR] No p*.bin files found")
        sys.exit(1)
    
    blob = b"".join(p.read_bytes() for p in files)
    print(f"[*] Total blob size: {len(blob)} bytes")
    
    if b"." not in blob:
        print("[ERROR] Blob format invalid - missing separator")
        sys.exit(1)
    
    parts = blob.split(b".", 2)
    print(f"[*] Blob parts count: {len(parts)}")
    
    sig_b64, enc_b64, sym_b64 = parts
    print(f"[*] Signature size: {len(sig_b64)}")
    print(f"[*] Encrypted data size: {len(enc_b64)}")
    print(f"[*] Symmetric key size: {len(sym_b64)}")
    
    enc = base64.b64decode(enc_b64)
    sym_key = base64.b64decode(sym_b64)
    
    print(f"[*] Decoded encrypted size: {len(enc)}")
    print(f"[*] Decoded key size: {len(sym_key)}")
    print(f"[*] Attempting decryption...")
    
    data = zlib.decompress(aesgcm_decrypt(enc, sym_key))
    print(f"[*] Decompressed data size: {len(data)}")
    
    print(f"[*] Attempting to load code...")
    try:
        code = marshal.loads(data)
        print(f"[*] Successfully loaded marshal code")
    except Exception as e:
        print(f"[*] Marshal failed ({e}), trying compile...")
        code = compile(data.decode('utf-8'), "<run>", "exec")
    
    print(f"[*] Executing code with license bypass...")
    bypass = LicenseBypass(__builtins__['input'])
    exec(code, {'__name__': '__main__', 'input': bypass})
    print(f"[+] Code execution completed!")
    
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
