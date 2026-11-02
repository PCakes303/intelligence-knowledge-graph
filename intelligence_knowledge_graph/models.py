"""Typed graph records and strict, bounded validation."""
from collections.abc import Mapping
from dataclasses import dataclass
import math
import re
from types import MappingProxyType
from urllib.parse import urlsplit

ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
HEX = re.compile(r"^[a-f0-9]{64}$")
MAX_METADATA_KEYS = 50
MAX_METADATA_STRING = 1024
MAX_EVIDENCE_REFS = 100


def valid_time(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime_from_iso(value)
        return parsed.tzinfo is not None and parsed.utcoffset() is not None
    except (ValueError, OverflowError):
        return False


def datetime_from_iso(value):
    from datetime import datetime
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _valid_https_url(value):
    if not isinstance(value, str) or not value or len(value) > 2048 or any(ch.isspace() for ch in value):
        return False
    try:
        parts = urlsplit(value)
        parts.port
        return (
            parts.scheme == "https"
            and bool(parts.hostname)
            and parts.username is None
            and parts.password is None
            and not parts.fragment
        )
    except ValueError:
        return False


def _validated_metadata(value):
    if not isinstance(value, dict) or len(value) > MAX_METADATA_KEYS:
        raise ValueError("metadata must be an object with at most 50 keys")
    result = {}
    for key, item in value.items():
        if not isinstance(key, str) or not key or len(key) > 128:
            raise ValueError("metadata keys must be bounded strings")
        if isinstance(item, str):
            if len(item) > MAX_METADATA_STRING:
                raise ValueError("metadata string value exceeds 1024 characters")
        elif isinstance(item, bool) or item is None:
            pass
        elif isinstance(item, int):
            pass
        elif isinstance(item, float):
            if not math.isfinite(item):
                raise ValueError("metadata numeric values must be finite")
        else:
            raise ValueError("metadata values must be scalar JSON values")
        result[key] = item
    return MappingProxyType(result)


@dataclass(frozen=True)
class Node:
    id: str
    type: str
    label: str
    recorded_at: str
    data: Mapping

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
        if not isinstance(kind, str) or kind not in required:
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
        meta = _validated_metadata(raw.get("metadata", {}))
        data = {k: v for k, v in raw.items() if k not in {"id", "type", "label", "recorded_at"}}
        if "metadata" in data:
            data["metadata"] = meta
        if kind == "source":
            if not _valid_https_url(raw["canonical_url"]):
                raise ValueError("canonical_url must be a valid HTTPS URL without credentials")
            if not isinstance(raw["source_record_id"], str) or not ID.fullmatch(raw["source_record_id"]):
                raise ValueError("source_record_id must be a bounded identifier")
        elif kind == "evidence":
            if not isinstance(raw["sha256"], str) or not HEX.fullmatch(raw["sha256"]):
                raise ValueError("sha256 must be lowercase SHA-256")
            if not valid_time(raw["observed_at"]):
                raise ValueError("observed_at must be timezone-aware")
            for key in ("evidence_record_id", "source_node_id"):
                if not isinstance(raw[key], str) or not ID.fullmatch(raw[key]):
                    raise ValueError(f"{key} must be a bounded identifier")
        else:
            for key in ("entity_record_id", "entity_kind"):
                if not isinstance(raw[key], str) or not raw[key] or len(raw[key]) > 128:
                    raise ValueError(f"{key} must contain 1..128 characters")
            if not isinstance(raw["resolution_status"], str) or raw["resolution_status"] not in {"provisional", "resolved", "disputed", "withdrawn"}:
                raise ValueError("invalid resolution_status")
        return cls(raw["id"], kind, raw["label"], raw["recorded_at"], MappingProxyType(data))

    def to_dict(self):
        result = dict(self.data)
        if "metadata" in result:
            result["metadata"] = dict(result["metadata"])
        return {"id": self.id, "type": self.type, "label": self.label,
                "recorded_at": self.recorded_at, **result}


@dataclass(frozen=True)
class Edge:
    id: str
    from_id: str
    to_id: str
    predicate: str
    evidence_refs: tuple[str, ...]
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
        limits = {"id": 128, "from": 128, "to": 128, "predicate": 128, "uncertainty": 500}
        for key, maximum in limits.items():
            if not isinstance(raw[key], str) or not raw[key].strip() or len(raw[key]) > maximum:
                raise ValueError(f"{key} must contain 1..{maximum} characters")
        refs = raw["evidence_refs"]
        if not isinstance(refs, list) or not 1 <= len(refs) <= MAX_EVIDENCE_REFS:
            raise ValueError("evidence_refs must contain 1..100 entries")
        if any(not isinstance(x, str) or not x or len(x) > 128 for x in refs):
            raise ValueError("evidence_refs must contain bounded non-empty identifiers")
        if len(set(refs)) != len(refs):
            raise ValueError("evidence_refs must be unique")
        score = raw["confidence"]
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError("confidence must be finite and in [0,1]")
        if not valid_time(raw["observed_at"]) or not valid_time(raw["recorded_at"]):
            raise ValueError("timestamps must be timezone-aware")
        return cls(raw["id"], raw["from"], raw["to"], raw["predicate"], tuple(refs),
                   float(score), raw["uncertainty"], raw["observed_at"], raw["recorded_at"])

    def to_dict(self):
        return {"id": self.id, "from": self.from_id, "to": self.to_id,
                "predicate": self.predicate, "evidence_refs": list(self.evidence_refs),
                "confidence": self.confidence, "uncertainty": self.uncertainty,
                "observed_at": self.observed_at, "recorded_at": self.recorded_at}
