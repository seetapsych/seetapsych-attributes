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
    gaze_camera_mm: GazePoint


class GazeScreen(BaseModel):
    gaze: GazeData


class Report(BaseModel):
    face_gaze_screen: list[GazeScreen]

    model_config = ConfigDict(
        title="face/gaze_screen",
        json_schema_extra={
            "description": (
                "Per-eye screen-space point-of-gaze coordinates in pixels "
                "and camera-space point-of-gaze coordinates in millimeters. "
                "Camera-space coordinates may be 2D or 3D depending on the algorithm; "
                "origin is at the camera center."
            ),
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
                                "gaze_camera_mm": {
                                    "left_eye": [155.0, 50.0, 25.0],
                                    "right_eye": [155.0, 50.0, 25.0],
                                },
                            }
                        }
                    ]
                }
            ],
        },
    )
