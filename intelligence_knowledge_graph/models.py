"""Typed graph records and strict validation; standard library only."""
from dataclasses import dataclass
from datetime import datetime
import re

ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
HEX = re.compile(r"^[a-f0-9]{64}$")

def valid_time(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset() is not None
    except ValueError:
        return False

@dataclass(frozen=True)
class Node:
    id: str
    type: str
    label: str
    recorded_at: str
    data: dict

    @classmethod
    def from_dict(cls, raw):
        if not isinstance(raw, dict):
            raise ValueError("node must be an object")
        kind = raw.get("type")
        required = {
            "source": {"source_record_id", "canonical_url"},
            "evidence": {"evidence_record_id", "sha256", "observed_at", "source_node_id"},
            "entity": {"entity_record_id", "entity_kind", "resolution_status"},
        }
        if kind not in required:
            raise ValueError("unsupported node type")
        common = {"id", "type", "label", "recorded_at", "metadata"}
        if set(raw) - common - required[kind] or not required[kind].issubset(raw):
            raise ValueError("node fields do not match node type")
        if not isinstance(raw.get("id"), str) or not ID.fullmatch(raw["id"]):
            raise ValueError("invalid node id")
        if not isinstance(raw.get("label"), str) or not raw["label"].strip() or len(raw["label"]) > 300:
            raise ValueError("invalid node label")
        if not valid_time(raw.get("recorded_at")):
            raise ValueError("recorded_at must be timezone-aware")
        meta = raw.get("metadata", {})
        if not isinstance(meta, dict) or len(meta) > 50:
            raise ValueError("metadata must be an object with at most 50 keys")
        data = {k: v for k, v in raw.items() if k not in {"id", "type", "label", "recorded_at"}}
        if kind == "source":
            url = raw["canonical_url"]
            if not isinstance(url, str) or not url.startswith("https://") or len(url) > 2048:
                raise ValueError("canonical_url must be HTTPS")
            if not isinstance(raw["source_record_id"], str) or not raw["source_record_id"]:
                raise ValueError("source_record_id required")
        elif kind == "evidence":
            if not isinstance(raw["sha256"], str) or not HEX.fullmatch(raw["sha256"]):
                raise ValueError("sha256 must be lowercase SHA-256")
            if not valid_time(raw["observed_at"]):
                raise ValueError("observed_at must be timezone-aware")
            for key in ("evidence_record_id", "source_node_id"):
                if not isinstance(raw[key], str) or not raw[key]:
                    raise ValueError(f"{key} required")
        else:
            for key in ("entity_record_id", "entity_kind"):
                if not isinstance(raw[key], str) or not raw[key]:
                    raise ValueError(f"{key} required")
            if raw["resolution_status"] not in {"provisional", "resolved", "disputed", "withdrawn"}:
                raise ValueError("invalid resolution_status")
        return cls(raw["id"], kind, raw["label"], raw["recorded_at"], data)

    def to_dict(self):
        return {"id": self.id, "type": self.type, "label": self.label,
                "recorded_at": self.recorded_at, **self.data}

@dataclass(frozen=True)
class Edge:
    id: str
    from_id: str
    to_id: str
    predicate: str
    evidence_refs: tuple
    confidence: float
    uncertainty: str
    observed_at: str
    recorded_at: str

    @classmethod
    def from_dict(cls, raw):
        if not isinstance(raw, dict):
            raise ValueError("edge must be an object")
        allowed = {"id", "from", "to", "predicate", "evidence_refs", "confidence",
                   "uncertainty", "observed_at", "recorded_at"}
        if set(raw) != allowed:
            raise ValueError("edge fields must exactly match contract")
        for key in ("id", "from", "to", "predicate", "uncertainty"):
            if not isinstance(raw[key], str) or not raw[key].strip():
                raise ValueError(f"{key} must be a non-empty string")
        refs = raw["evidence_refs"]
        if not isinstance(refs, list) or not refs or len(set(refs)) != len(refs) or any(not isinstance(x, str) or not x for x in refs):
            raise ValueError("evidence_refs must be a non-empty unique list")
        score = raw["confidence"]
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 1:
            raise ValueError("confidence must be in [0,1]")
        if not valid_time(raw["observed_at"]) or not valid_time(raw["recorded_at"]):
            raise ValueError("timestamps must be timezone-aware")
        return cls(raw["id"], raw["from"], raw["to"], raw["predicate"], tuple(refs),
                   float(score), raw["uncertainty"], raw["observed_at"], raw["recorded_at"])

    def to_dict(self):
        return {"id": self.id, "from": self.from_id, "to": self.to_id,
                "predicate": self.predicate, "evidence_refs": list(self.evidence_refs),
                "confidence": self.confidence, "uncertainty": self.uncertainty,
                "observed_at": self.observed_at, "recorded_at": self.recorded_at}
