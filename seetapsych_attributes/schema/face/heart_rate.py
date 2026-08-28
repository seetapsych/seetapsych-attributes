# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class HeartRate(BaseModel):
    fps: float = Field(..., description="Current estimated frames per second.")
    wait_seconds: float = Field(..., description="Seconds remaining until enough data is buffered. 0.0 when HR is ready.")
    hr_bpm: Optional[float] = Field(None, description="Estimated heart rate in beats per minute. Present only when ready.")


class Report(BaseModel):
    face_heart_rate: HeartRate

    model_config = ConfigDict(
        title="face/heart_rate",
        json_schema_extra={
            "x-brief": "Estimate heart rate (BPM) from face video frames using rPPG or model-based methods.",
            "examples": [{
                "face_heart_rate": {
                    "fps": 30.0,
                    "wait_seconds": 0.0,
                    "hr_bpm": 72.5,
                }
            }, {
                "face_heart_rate": {
                    "fps": 30.0,
                    "wait_seconds": 5.2,
                }
            }]
        }
    )
