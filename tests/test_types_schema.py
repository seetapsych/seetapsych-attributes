# -*- coding: utf-8 -*-
"""Consistency tests between TypedDict declarations in types/ and BaseModel declarations in schema/.

Verifies:
1. Field name sets match between paired TypedDict and BaseModel classes.
2. Required / optional flag of each field matches between pair.
3. Pydantic validation accepts a full-fields payload built from the TypedDict contract.
4. Pydantic validation accepts a minimal payload containing only required fields.
5. Pydantic validation rejects a payload missing a required field.

Python-version compatibility (3.10 <= ver <= 3.14):
    * ``Required`` / ``NotRequired`` come from ``typing`` on 3.11+ and from
      ``typing_extensions`` on 3.10 (PEP 655 semantics are identical).
    * CPython 3.10's TypedDict metaclass computes ``__required_keys__`` from
      ``total=`` alone and ignores explicit ``Required`` / ``NotRequired``
      wrappers; helpers therefore check wrapper origin first and fall back
      to ``__required_keys__`` only for unwrapped fields.
    * ``typing.get_type_hints``, ``get_origin``, and ``get_args`` are
      stable typing APIs unchanged across 3.10..3.14.
"""

from __future__ import annotations

import typing
from typing import Any, get_args, get_origin

import numpy as np
import pytest
from pydantic import BaseModel, ValidationError

try:
    from typing import NotRequired as _NotRequiredT
    from typing import Required as _RequiredT
except ImportError:  # pragma: no cover - py<3.11
    from typing_extensions import NotRequired as _NotRequiredT
    from typing_extensions import Required as _RequiredT

import seetapsych_attributes.types as td_types
import seetapsych_attributes.types.head as _td_head_mod
from seetapsych_attributes.schema import schema as SCHEMA_REGISTRY
from seetapsych_attributes.schema.face import (
    action_units as face_au_mod,
)
from seetapsych_attributes.schema.face import (
    dense_landmarks as face_dense_lm_mod,
)
from seetapsych_attributes.schema.face import (
    detection as face_det_mod,
)
from seetapsych_attributes.schema.face import (
    dimensional_affect as face_dim_mod,
)
from seetapsych_attributes.schema.face import (
    expression as face_expr_mod,
)
from seetapsych_attributes.schema.face import (
    gaze_screen as face_gaze_mod,
)
from seetapsych_attributes.schema.face import (
    heart_rate as face_hr_mod,
)
from seetapsych_attributes.schema.face import (
    landmarks as face_lm_mod,
)
from seetapsych_attributes.schema.face import (
    mesh as face_mesh_mod,
)
from seetapsych_attributes.schema.face import (
    selection as face_sel_mod,
)
from seetapsych_attributes.schema.head import (
    detection as head_det_mod,
)
from seetapsych_attributes.schema.head import (
    gaze_point as head_gp_mod,
)
from seetapsych_attributes.schema.head import (
    selection as head_sel_mod,
)
from seetapsych_attributes.schema.head import (
    social_gaze as head_sg_mod,
)

# Resolve forward refs like ``"numpy.ndarray"`` in types/head.py by injecting
# numpy into that module's globals (it is imported only under TYPE_CHECKING).
_td_head_mod.numpy = np


# ---------------------------------------------------------------------------
# Helpers: TypedDict field introspection
# ---------------------------------------------------------------------------


def _is_typeddict(tp: Any) -> bool:
    """Return True if *tp* is a TypedDict class."""
    if not isinstance(tp, type):
        return False
    return issubclass(tp, dict) and hasattr(tp, "__annotations__") and hasattr(tp, "__required_keys__")


def _typeddict_fields(td_cls: type) -> dict[str, tuple[type, bool]]:
    """Return {field_name: (annotated_type, is_required)} for a TypedDict class.

    Checks explicit ``Required[]`` / ``NotRequired[]`` wrappers first (via
    ``get_type_hints(include_extras=True)``) and falls back to the class
    ``__required_keys__`` set for unwrapped fields. Injects ``numpy`` into
    the resolver namespace so TYPE_CHECKING-only forward references like
    ``"numpy.ndarray"`` can be resolved.
    """
    import sys as _sys

    module_ns: dict[str, Any] = {}
    mod = _sys.modules.get(getattr(td_cls, "__module__", None))
    if mod is not None and hasattr(mod, "__dict__"):
        module_ns = vars(mod)
    extra_ns: dict[str, Any] = {"numpy": np}
    combined_ns = {**module_ns, **extra_ns}
    raw_hints = typing.get_type_hints(td_cls, globalns=combined_ns, include_extras=True)
    required_keys: set[str] = set(getattr(td_cls, "__required_keys__", set()) or set())
    out: dict[str, tuple[type, bool]] = {}
    for name, hint in raw_hints.items():
        origin = get_origin(hint)
        inner_type = hint
        if origin is _RequiredT:
            inner_type = get_args(hint)[0]
            is_req = True
        elif origin is _NotRequiredT:
            inner_type = get_args(hint)[0]
            is_req = False
        else:
            is_req = name in required_keys
        out[name] = (inner_type, is_req)
    return out


def _basemodel_fields(model_cls: type[BaseModel]) -> dict[str, tuple[Any, bool]]:
    """Return {field_name: (field_annotation, is_required)} for a Pydantic BaseModel."""
    out: dict[str, tuple[Any, bool]] = {}
    for name, fi in model_cls.model_fields.items():
        out[name] = (fi.annotation, fi.is_required())
    return out


def _unpack_list_type(tp: Any) -> Any | None:
    """If *tp* is ``list[X]`` (or ``List[X]``), return ``X``; else return None."""
    origin = get_origin(tp)
    if origin is list or origin is typing.List:
        args = get_args(tp)
        if args:
            return args[0]
    return None


# ---------------------------------------------------------------------------
# Fixture: pair registry
# ---------------------------------------------------------------------------


def _np_heatmap(height: int = 4, width: int = 4) -> np.ndarray:
    """Small synthetic heatmap used in place of real algorithm output."""
    return np.zeros((height, width), dtype=np.float32)


SCHEMA_KEY_TO_TD_TYPE: dict[str, Any] = {
    "face/detection": td_types.FaceDetection,
    "face/landmarks": td_types.FaceLandmarks,
    "face/selection": td_types.FaceSelection,
    "face/action_units": td_types.FaceActionUnits,
    "face/expression": td_types.FaceExpression,
    "face/dense_landmarks": td_types.FaceDenseLandmarks,
    "face/mesh": td_types.FaceMesh,
    "face/gaze_screen": td_types.FaceGazeScreen,
    "face/heart_rate": td_types.FaceHeartRate,
    "face/dimensional_affect": td_types.FaceDimensionalAffect,
    "face/feature": td_types.FaceFeature,
    "head/detection": td_types.HeadDetection,
    "head/selection": td_types.HeadSelection,
    "head/gaze_point": td_types.HeadGazePointList,
    "head/social_gaze": td_types.HeadSocialGaze,
}

# Pairs of (BaseModel, TypedDict) for nested inner classes that must agree on
# field names, required-ness and (roughly) element types.
INNER_CLASS_PAIRS: list[tuple[str, type[BaseModel], type]] = [
    ("BBox", face_det_mod.BBox, td_types.BBox),
    ("Landmarks", face_lm_mod.Landmarks, td_types.Landmarks),
    ("Selection", face_sel_mod.Selection, td_types.Selection),
    ("ActionUnits", face_au_mod.ActionUnits, td_types.ActionUnits),
    ("Expression", face_expr_mod.Expression, td_types.Expression),
    ("DenseLandmarks", face_dense_lm_mod.DenseLandmarks, td_types.DenseLandmarks),
    ("MeshLandmarks", face_mesh_mod.MeshLandmarks, td_types.MeshLandmarks),
    ("GazePoint", face_gaze_mod.GazePoint, td_types.GazePoint),
    ("GazeData", face_gaze_mod.GazeData, td_types.GazeData),
    ("GazeScreen", face_gaze_mod.GazeScreen, td_types.GazeScreen),
    ("HeartRate", face_hr_mod.HeartRate, td_types.HeartRate),
    ("DimensionalAffect", face_dim_mod.DimensionalAffect, td_types.DimensionalAffect),
    ("HeadBBox", head_det_mod.HeadBBox, td_types.HeadBBox),
    ("HeadSelection", head_sel_mod.HeadSelection, td_types.HeadSelection),
    ("HeadGazePoint", head_gp_mod.HeadGazePoint, td_types.HeadGazePoint),
    ("SocialGazePerson", head_sg_mod.SocialGazePerson, td_types.SocialGazePerson),
    ("HeadSocialGaze", head_sg_mod.HeadSocialGaze, td_types.HeadSocialGaze),
]


# ---------------------------------------------------------------------------
# Helpers: example value factories
# ---------------------------------------------------------------------------


_FLOAT_VAL = 0.5
_INT_VAL = 1
_BOOL_VAL = True
_STR_VAL = "ok"


def _example_for_type(tp: Any) -> Any:
    """Build a small valid Python value for a type annotation.

    Handles primitives, ``list[T]`` / ``dict[K,V]``, ``numpy.ndarray`` (including
    string forward ref), ``X | None`` unions, ``Any``, and known TypedDict /
    BaseModel subclasses. Callers (e.g. _example_typeddict) patch specific
    field names afterwards for Pydantic length constraints.
    """
    if tp is Any or tp is None or tp is type(None):
        return None
    origin = get_origin(tp)
    args = get_args(tp)
    if origin is typing.Union or (origin is None and args and len(args) == 2 and type(None) in args):
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            return _example_for_type(non_none[0])
        return None
    if isinstance(tp, type) and issubclass(tp, BaseModel):
        return _example_basemodel_instance(tp)
    if _is_typeddict(tp):
        return _example_typeddict(tp)
    if origin is list or origin is typing.List:
        inner = args[0] if args else float
        length = 1
        if inner is float:
            return [_FLOAT_VAL] * length
        if inner is int:
            return [_INT_VAL] * length
        if origin is list and args and _is_typeddict(args[0]):
            return [_example_for_type(args[0])]
        return [_example_for_type(inner)]
    if origin is dict or origin is typing.Dict:
        key_tp, val_tp = args or (str, float)
        return {_example_for_type(key_tp) if key_tp is not str else "a": _example_for_type(val_tp)}
    if isinstance(tp, type):
        if issubclass(tp, np.ndarray):
            return _np_heatmap()
        if issubclass(tp, float):
            return _FLOAT_VAL
        if issubclass(tp, int) and not issubclass(tp, bool):
            return _INT_VAL
        if issubclass(tp, bool):
            return _BOOL_VAL
        if issubclass(tp, str):
            return _STR_VAL
    # Last resort: assume ``numpy.ndarray`` via string forward ref annotation.
    if isinstance(tp, str) and "ndarray" in tp:
        return _np_heatmap()
    return _FLOAT_VAL


def _example_typeddict(td_cls: type, include_optional: bool = True) -> dict[str, Any]:
    """Construct an example dict matching a TypedDict definition.

    If *include_optional* is False then only required fields are populated.
    """
    fields = _typeddict_fields(td_cls)
    result: dict[str, Any] = {}
    for name, (field_type, required) in fields.items():
        if required or include_optional:
            value = _example_for_type(field_type)
            # Patch known length-constrained list fields by field name.
            # Covers both the direct class (e.g. BBox.xyxy) and nested
            # head classes (HeadGazePoint.head_location_xyxy, etc.).
            if name == "xyxy":
                base_type = int if td_cls in (td_types.HeadBBox,) else float
                value = [(_INT_VAL if issubclass(base_type, int) else _FLOAT_VAL)] * 4
            elif name == "head_location_xyxy":
                value = [_INT_VAL] * 4
            elif name == "gaze_point_px":
                value = [_FLOAT_VAL] * 2
            elif name == "landmarks" and td_cls is td_types.Landmarks:
                value = [_FLOAT_VAL] * 10
            elif name == "landmarks" and td_cls is td_types.DenseLandmarks:
                value = [_FLOAT_VAL] * 560
            elif name == "normalized_3d_landmarks":
                value = [_FLOAT_VAL] * 1404
            elif name in ("left_eye", "right_eye"):
                value = [_FLOAT_VAL] * 2
            result[name] = value
    return result


def _example_basemodel_instance(model_cls: type[BaseModel]) -> Any:
    """Instantiate *model_cls* using a valid example payload (full fields)."""
    pair: tuple[str, type[BaseModel], type] | None = next((p for p in INNER_CLASS_PAIRS if p[1] is model_cls), None)
    if pair is None:
        return model_cls(**{})
    _label, _bm, td_cls = pair
    return model_cls(**_example_typeddict(td_cls, include_optional=True))


# ---------------------------------------------------------------------------
# 1. Per-schema-key: report-level field type matches TypedDict alias
# ---------------------------------------------------------------------------


def test_schema_registry_keys_match_typedict_alias_map() -> None:
    """Every key registered in schema/__init__.py has a matching TypedDict alias entry."""
    for key in SCHEMA_REGISTRY:
        assert key in SCHEMA_KEY_TO_TD_TYPE, f"Missing TypedDict alias mapping for schema key {key!r}"


def test_report_top_field_name_matches_types_report() -> None:
    """The single top-level field name of each schema.Report appears in types.Report."""
    report_td_fields = _typeddict_fields(td_types.Report)
    for key, report_model in SCHEMA_REGISTRY.items():
        top_fields = _basemodel_fields(report_model)
        assert len(top_fields) == 1, f"{key}: expected exactly one top-level Report field, got {list(top_fields)}"
        field_name = next(iter(top_fields))
        assert field_name in report_td_fields, f"{key}: Report field {field_name!r} not found in types.Report TypedDict"


# ---------------------------------------------------------------------------
# 2. Inner-class structural consistency
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("label", "bm_cls", "td_cls"), INNER_CLASS_PAIRS)
def test_inner_class_field_names_match(label: str, bm_cls: type[BaseModel], td_cls: type) -> None:
    """Paired BaseModel and TypedDict expose the same field name set."""
    bm_fields = _basemodel_fields(bm_cls)
    td_fields = _typeddict_fields(td_cls)
    bm_names = set(bm_fields)
    td_names = set(td_fields)
    missing_in_bm = td_names - bm_names
    extra_in_bm = bm_names - td_names
    assert not missing_in_bm and not extra_in_bm, (
        f"{label}: field name mismatch. "
        f"TypedDict-only fields: {sorted(missing_in_bm)!r}. "
        f"BaseModel-only fields: {sorted(extra_in_bm)!r}."
    )


@pytest.mark.parametrize(("label", "bm_cls", "td_cls"), INNER_CLASS_PAIRS)
def test_inner_class_required_optional_match(label: str, bm_cls: type[BaseModel], td_cls: type) -> None:
    """Each field has the same required/optional status between paired classes."""
    bm_fields = _basemodel_fields(bm_cls)
    td_fields = _typeddict_fields(td_cls)
    mismatches: list[str] = []
    for name in td_fields:
        _bm_tp, bm_required = bm_fields[name]
        _td_tp, td_required = td_fields[name]
        if bm_required != td_required:
            mismatches.append(f"{name}: TD required={td_required}, BM required={bm_required}")
    assert not mismatches, f"{label}: required/optional mismatch -> {'; '.join(mismatches)}"


# ---------------------------------------------------------------------------
# 3. Validation: full payload accepted
# ---------------------------------------------------------------------------


def _build_report_payload(schema_key: str, include_optional: bool) -> dict[str, Any]:
    """Build a payload dict for the top-level schema Report of *schema_key*."""
    report_model = SCHEMA_REGISTRY[schema_key]
    top_fields = _basemodel_fields(report_model)
    top_field_name = next(iter(top_fields))
    td_top_type = SCHEMA_KEY_TO_TD_TYPE[schema_key]
    element_td = _unpack_list_type(td_top_type)

    if element_td is not None and _is_typeddict(element_td):
        items = [_example_typeddict(element_td, include_optional=include_optional)]
        return {top_field_name: items}

    if _is_typeddict(td_top_type):
        return {top_field_name: _example_typeddict(td_top_type, include_optional=include_optional)}

    # FaceFeature is a raw alias list[list[float]]; no TypedDict backing
    if schema_key == "face/feature":
        inner_len = 5
        if not include_optional:
            inner_len = 0
        sample = [[_FLOAT_VAL] * 5] if inner_len else []
        return {top_field_name: sample}

    pytest.skip(f"No TypedDict example strategy for {schema_key}")
    return {}


@pytest.mark.parametrize("schema_key", list(SCHEMA_REGISTRY.keys()))
def test_full_payload_passes_validation(schema_key: str) -> None:
    """A payload including every declared field validates via Pydantic."""
    model = SCHEMA_REGISTRY[schema_key]
    payload = _build_report_payload(schema_key, include_optional=True)
    instance = model.model_validate(payload)
    assert isinstance(instance, model)


@pytest.mark.parametrize("schema_key", list(SCHEMA_REGISTRY.keys()))
def test_minimal_required_payload_passes_validation(schema_key: str) -> None:
    """A payload containing only required fields validates via Pydantic."""
    model = SCHEMA_REGISTRY[schema_key]
    payload = _build_report_payload(schema_key, include_optional=False)
    instance = model.model_validate(payload)
    assert isinstance(instance, model)


# ---------------------------------------------------------------------------
# 4. Validation: missing a required field is rejected
# ---------------------------------------------------------------------------


def _required_inner_examples() -> list[tuple[str, type[BaseModel], type, str]]:
    """Enumerate (label, BaseModel, TypedDict, required_field_name) for drop-one tests."""
    cases: list[tuple[str, type[BaseModel], type, str]] = []
    for label, bm_cls, td_cls in INNER_CLASS_PAIRS:
        td_fields = _typeddict_fields(td_cls)
        required = [n for n, (_t, r) in td_fields.items() if r]
        for field_name in required:
            cases.append((label, bm_cls, td_cls, field_name))
    return cases


@pytest.mark.parametrize(
    ("label", "bm_cls", "td_cls", "drop_field"),
    _required_inner_examples(),
)
def test_drop_required_field_rejected(
    label: str,
    bm_cls: type[BaseModel],
    td_cls: type,
    drop_field: str,
) -> None:
    """Removing a single required field from a full payload raises ValidationError."""
    full = _example_typeddict(td_cls, include_optional=True)
    assert drop_field in full
    del full[drop_field]
    with pytest.raises(ValidationError):
        bm_cls.model_validate(full)


# ---------------------------------------------------------------------------
# 5. HeartRate negative sentinel contract
# ---------------------------------------------------------------------------


_HEART_RATE_NEGATIVE_CASES: list[tuple[float, float]] = [
    (-1.0, -1.0),
    (-1.0, 5.2),
    (30.0, -1.0),
]


@pytest.mark.parametrize(("fps", "wait_seconds"), _HEART_RATE_NEGATIVE_CASES)
def test_heart_rate_negative_sentinel_accepted(fps: float, wait_seconds: float) -> None:
    """fps / wait_seconds negative sentinel values validate without the optional HR fields."""
    from seetapsych_attributes.schema.face.heart_rate import (
        Report as HeartRateReport,
    )

    payload = {"face_heart_rate": {"fps": fps, "wait_seconds": wait_seconds}}
    instance = HeartRateReport.model_validate(payload)
    assert instance.face_heart_rate.fps == fps
    assert instance.face_heart_rate.wait_seconds == wait_seconds
    assert instance.face_heart_rate.hr_bpm is None
    assert instance.face_heart_rate.roi_hr_bpm is None


def test_heart_rate_negative_sentinel_matches_typeddict_keys() -> None:
    """Negative-sentinel payload also satisfies the HeartRate TypedDict key contract."""
    td_fields = _typeddict_fields(td_types.HeartRate)
    payload_keys = {"fps", "wait_seconds"}
    # fps + wait_seconds are Required; hr_bpm + roi_hr_bpm are NotRequired and may be absent.
    assert payload_keys == {n for n, (_t, r) in td_fields.items() if r}
