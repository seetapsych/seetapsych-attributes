# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Report",
]


class Landmarks(BaseModel):
    landmarks: Annotated[list[float], Field(min_length=10, max_length=10)]


class Report(BaseModel):
    face_landmarks: list[Landmarks]

    model_config = ConfigDict(
        title="face/landmarks",
        json_schema_extra={
            "description": (
                "Facial landmarks for basic alignment: L-eye, R-eye, nose, L-mouth, R-mouth (10 interleaved floats)."
            ),
            "examples": [
                {
                    "face_landmarks": [
                        {
                            "landmarks": [100, 100, 200, 200, 300, 300, 400, 400, 500, 500],
                        }
                    ]
                }
            ],
        },
    )
