# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class DenseLandmarks(BaseModel):
    landmarks: Annotated[list[float], Field(min_length=560, max_length=560)]


class Report(BaseModel):
    face_dense_landmarks: list[DenseLandmarks]

    model_config = ConfigDict(
        title="face/dense_landmarks",
        json_schema_extra={
            "x-brief": "Predict 280 dense facial landmarks from bounding box with optional refinement.",
            "examples": [{
                "face_dense_landmarks": [
                    {
                        "landmarks": [100.0] * 560,
                    }
                ]
            }]
        }
    )
