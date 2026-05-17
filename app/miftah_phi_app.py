#!/usr/bin/env python3
from __future__ import annotations

import json
import mimetypes
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.miftah_phi_engine import QuranCorpus, analyze_reference, build_domain_profiles
from core.project_paths import GENERATED_DIR, LIBRARY_DIR, WEBAPP_DIR
from core.sacred_text_engine import (
    GENERIC_DOMAINS,
    SCRIPT_CONFIGS,
    analyze_corpus_entry,
    analyze_generic_text,
    list_corpora,
    load_corpus,
    save_corpus,
)
from core.talisman_image_generator import render_talisman


BASE_DIR = ROOT_DIR
STATIC_DIR = WEBAPP_DIR
LIB_INDEX = LIBRARY_DIR / "quran_surah_library.json"

QURAN = QuranCorpus()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "MiftahPhiApp/1.0"

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return

    def _send(self, status: int, body: bytes, content_type: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: object, status: int = 200) -> None:
        self._send(status, json_bytes(payload))

    def _send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self._send_json({"error": "File not found"}, status=404)
            return
        mime, _ = mimetypes.guess_type(str(path))
        self._send(200, path.read_bytes(), mime or "application/octet-stream")

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/":
            return self._send_file(STATIC_DIR / "index.html")
        if path in {"/app.js", "/styles.css"}:
            return self._send_file(STATIC_DIR / path.lstrip("/"))
        if path.startswith("/generated/"):
            return self._send_file(GENERATED_DIR / path.removeprefix("/generated/"))
        if path == "/api/domains":
            return self._send_json(
                {
                    "quran_domains": {k: v.__dict__ for k, v in build_domain_profiles().items()},
                    "generic_domains": GENERIC_DOMAINS,
                    "schemes": {k: {"label": v["label"]} for k, v in SCRIPT_CONFIGS.items()},
                }
            )
        if path == "/api/quran/suras":
            payload = []
            for idx, meta in QURAN.suras.items():
                payload.append(
                    {
                        "index": idx,
                        "name_ar": meta.name,
                        "name_en": meta.ename,
                        "tname": meta.tname,
                        "ayas": meta.ayas,
                        "place": meta.place,
                    }
                )
            return self._send_json(payload)
        if path == "/api/corpora":
            return self._send_json(list_corpora())
        if path == "/api/corpus/refs":
            corpus_id = qs.get("corpus_id", [""])[0]
            corpus = load_corpus(corpus_id)
            return self._send_json([entry["ref"] for entry in corpus.entries])
        if path == "/api/library":
            if LIB_INDEX.exists():
                return self._send_file(LIB_INDEX)
            return self._send_json({"error": "Library not built yet"}, status=404)

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            payload = self._read_json()
            if path == "/api/analyze/quran":
                sura = int(payload["sura"])
                ayah = payload.get("ayah")
                end = payload.get("end")
                result = analyze_reference(
                    QURAN,
                    sura=sura,
                    ayah=int(ayah) if ayah not in (None, "", 0) else None,
                    end=int(end) if end not in (None, "", 0) else None,
                    domain_key=payload.get("domain", "richesse"),
                )
                return self._send_json(result)

            if path == "/api/analyze/text":
                result = analyze_generic_text(
                    text=payload["text"],
                    scheme=payload["scheme"],
                    domain=payload.get("domain", "richesse"),
                    source_ref=payload.get("ref_label", "custom-text"),
                    corpus_name=payload.get("corpus_name", "custom"),
                )
                return self._send_json(result)

            if path == "/api/import/corpus":
                corpus = save_corpus(
                    name=payload["name"],
                    scheme=payload["scheme"],
                    raw_entries=payload["raw_entries"],
                    description=payload.get("description", ""),
                )
                return self._send_json(corpus.__dict__)

            if path == "/api/analyze/corpus":
                result = analyze_corpus_entry(
                    corpus_id=payload["corpus_id"],
                    ref=payload["ref"],
                    domain=payload.get("domain", "richesse"),
                )
                return self._send_json(result)

            if path == "/api/render/talisman":
                result = payload["result"]
                title = payload.get("title")
                out = render_talisman(result, title=title)
                rel = out.relative_to(GENERATED_DIR).as_posix()
                return self._send_json({"path": f"/generated/{rel}"})

            if path == "/api/talisman/vivant":
                name = payload.get("name", "")
                domain = payload.get("domain", "richesse")
                date_str = payload.get("date", "")
                # Compute name abjad
                from core.miftah_phi_engine import abjad_sum, digital_root
                name_abjad = abjad_sum(name)
                name_root = digital_root(name_abjad)
                # Compute lunar mansion from date
                import datetime
                try:
                    d = datetime.date.fromisoformat(date_str) if date_str else datetime.date.today()
                    new_moon = datetime.date(2026, 5, 16)  # reference new moon
                    day_of_cycle = (d - new_moon).days % 29
                    mansion = (day_of_cycle % 28) + 1
                except Exception:
                    mansion = 1
                # Generate personalized talisman analysis
                suras_by_domain = {"richesse": 56, "sante": 17, "savoir": 20, "protection": 113, "occultes": 18}
                sura = suras_by_domain.get(domain, 56)
                result = analyze_reference(QURAN, sura=sura, domain_key=domain)
                # Override center with name abjad
                result["talisman"]["center"] = name_root
                result["talisman"]["inner_ring"][0] = name_abjad
                result["talisman"]["inner_ring"][1] = mansion
                result["signature"]["center"] = name_root
                result["signature"]["ring_inner"][0] = name_abjad
                result["signature"]["ring_inner"][1] = mansion
                result["vivant"] = {
                    "name": name,
                    "name_abjad": name_abjad,
                    "name_root": name_root,
                    "lunar_mansion": mansion,
                    "date": str(d) if date_str else str(datetime.date.today()),
                }
                return self._send_json(result)

        except Exception as exc:  # noqa: BLE001
            return self._send_json({"error": str(exc)}, status=500)

        self._send_json({"error": "Not found"}, status=404)


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Miftah Phi App running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
