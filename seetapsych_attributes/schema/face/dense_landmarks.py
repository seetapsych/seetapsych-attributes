# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Report",
]


class DenseLandmarks(BaseModel):
    landmarks: Annotated[list[float], Field(min_length=560, max_length=560)]


class Report(BaseModel):
    face_dense_landmarks: list[DenseLandmarks]

    model_config = ConfigDict(
        title="face/dense_landmarks",
        json_schema_extra={
            "description": "280-point dense facial landmarks (560 interleaved [x,y] floats).",
            "examples": [
                {
                    "face_dense_landmarks": [
                        {
                            "landmarks": [100.0] * 560,
                        }
                    ]
                }
            ],
        },
    )
