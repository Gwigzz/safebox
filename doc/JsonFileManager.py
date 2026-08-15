import json
import os
import tempfile
import stat
from pathlib import Path
from typing import Any

# fais par github copilote, pour rendre certaine fonctions plus modulaire
# not integretated in safebox for the moment

class JsonFileManager:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def load(self, filename: str) -> dict[str, Any]:
        path = self.base_dir / filename
        return self._read_json(path)

    def save(self, filename: str, data: dict[str, Any]) -> None:
        path = self.base_dir / filename
        self._write_json_atomic(path, data)

    def exists(self, filename: str) -> bool:
        return (self.base_dir / filename).exists()

    def delete(self, filename: str) -> None:
        path = self.base_dir / filename
        if path.exists():
            path.unlink()

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as handle:
            try:
                data = json.load(handle)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Fichier JSON corrompu : {path}") from exc

        if not isinstance(data, dict):
            raise ValueError(f"Contenu JSON invalide dans {path}")
        return data

    def _write_json_atomic(self, path: Path, data: dict[str, Any]) -> None:
        os.makedirs(path.parent, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=4, ensure_ascii=False)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_path, path)
            self._set_secure_permissions(path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _set_secure_permissions(self, path: Path) -> None:
        try:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass