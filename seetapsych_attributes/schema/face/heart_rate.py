# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Report",
]


class HeartRate(BaseModel):
    fps: float = Field(
        ...,
        description=(
            "Measured frames per second of the processing stream, averaged over a recent sliding window for stability."
        ),
    )
    wait_seconds: float = Field(
        ...,
        description=(
            "Rough estimate of remaining seconds until the next heart-rate update "
            "may be emitted. A value of 0.0 does not guarantee a result; use the presence "
            "of hr_bpm to determine whether a valid prediction is available."
        ),
    )
    hr_bpm: float | None = Field(
        None,
        description=(
            "Final integrated heart-rate prediction in beats per minute. The combination "
            "strategy is algorithm-specific; this field is omitted entirely when the current "
            "payload does not carry a reliable estimate."
        ),
    )
    roi_hr_bpm: dict[str, float] | None = Field(
        None,
        description=(
            "Per-region heart-rate estimates keyed by the region identifier. Some regions "
            "may be absent from the mapping when no valid estimate can be produced for them, "
            "and the field as a whole is omitted for algorithms that do not expose ROI-level results."
        ),
    )


class Report(BaseModel):
    face_heart_rate: HeartRate

    model_config = ConfigDict(
        title="face/heart_rate",
        json_schema_extra={
            "description": "Heart rate (BPM) estimated from buffered face video frames.",
            "examples": [
                {
                    "face_heart_rate": {
                        "fps": 30.0,
                        "wait_seconds": 0.0,
                        "hr_bpm": 72.5,
                        "roi_hr_bpm": {
                            "skin_legacy": 72.5,
                            "skin_a_fixed_forehead": 72.5,
                            "skin_b_adaptive_forehead": 72.5,
                            "skin_c_connected_components": 72.5,
                        },
                    }
                },
                {
                    "face_heart_rate": {
                        "fps": 30.0,
                        "wait_seconds": 5.2,
                    }
                },
            ],
        },
    )
