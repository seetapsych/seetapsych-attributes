# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Report",
]


class GazePoint(BaseModel):
    left_eye: Annotated[list[float], Field(min_length=0, max_length=3)]
    right_eye: Annotated[list[float], Field(min_length=0, max_length=3)]


class GazeData(BaseModel):
    success: bool
    gaze_screen_px: GazePoint
    gaze_cm: GazePoint


class GazeScreen(BaseModel):
    gaze: GazeData


class Report(BaseModel):
    face_gaze_screen: list[GazeScreen]

    model_config = ConfigDict(
        title="face/gaze_screen",
        json_schema_extra={
            "description": "Per-eye screen-space gaze coordinates and camera-space gaze vectors.",
            "examples": [
                {
                    "face_gaze_screen": [
                        {
                            "gaze": {
                                "success": True,
                                "gaze_screen_px": {
                                    "left_eye": [960.0, 540.0],
                                    "right_eye": [960.0, 540.0],
                                },
                                "gaze_cm": {
                                    "left_eye": [15.5, 5.0, 2.5],
                                    "right_eye": [15.5, 5.0, 2.5],
                                },
                            }
                        }
                    ]
                }
            ],
        },
    )
