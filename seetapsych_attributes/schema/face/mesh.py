# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

__all__ = [
    'Report',
]


class MeshLandmarks(BaseModel):
    normalized_3d_landmarks: Annotated[list[float], Field(min_length=1404, max_length=1404)]


class Report(BaseModel):
    face_mesh: list[MeshLandmarks]

    model_config = ConfigDict(
        title="face/mesh",
        json_schema_extra={
            "description": "468-point 3D face mesh landmarks in normalized coordinates.",
            "examples": [{
                "face_mesh": [
                    {
                        "normalized_3d_landmarks": [0.5] * 1404,
                    }
                ]
            }]
        }
    )
