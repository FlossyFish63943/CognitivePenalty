import hashlib
import json
import os
import pefile
import threading

CACHE_FILE = "hash_cache.json"
_lock = threading.Lock()

# path -> sha256
_hash_cache = {}

def _load_cache():
    global _hash_cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                _hash_cache = json.load(f)
        except Exception:
            _hash_cache = {}

def _save_cache():
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(_hash_cache, f, indent=2)
    except Exception:
        pass

_load_cache()


def sha256_of_file(path, cache=True):
    path = path.lower()

    with _lock:
        if cache and path in _hash_cache:
            return _hash_cache[path]

    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)

        digest = h.hexdigest()

        if cache:
            with _lock:
                _hash_cache[path] = digest
                _save_cache()

        return digest
    except Exception:
        return None


def get_original_filename(path):
    try:
        pe = pefile.PE(path, fast_load=True)
        pe.parse_data_directories(
            directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']]
        )

        for fileinfo in pe.FileInfo:
            for entry in fileinfo:
                if entry.Key == b'StringFileInfo':
                    for st in entry.StringTable:
                        val = st.entries.get(b'OriginalFilename')
                        if val:
                            return val.decode(errors="ignore").lower()
    except Exception:
        pass

    return None