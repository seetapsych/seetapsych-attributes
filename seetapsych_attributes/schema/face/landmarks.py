# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


__all__ = [
    'Report',
]


class Landmarks(BaseModel):
    landmarks: Annotated[list[float], Field(min_length=10, max_length=10)]


class Report(BaseModel):
    face_landmarks: list[Landmarks]

    model_config = ConfigDict(
        title="face/landmarks",
        json_schema_extra={
            "x-brief": "Get facial landmarks for basic alignment, "
                       "including the centers of the left and right eyes, "
                       "the nose tip, and the positions of the left and right mouth corners.",
            "examples": [{
                "face_landmarks": [
                    {
                        "landmarks": [100, 100, 200, 200, 300, 300, 400, 400, 500, 500],
                    }
                ]
            }]
        }
    )
