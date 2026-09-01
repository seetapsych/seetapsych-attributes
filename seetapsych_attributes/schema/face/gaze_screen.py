# -*- coding: utf-8 -*-

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "Report",
]


class GazePoint(BaseModel):
    left_eye: Annotated[
        list[float],
        Field(
            min_length=0,
            max_length=3,
            description=(
                "Gaze-screen-px [x,y] or gaze-camera-mm [x,y(,z)]; "
                "2D or 3D depending on algorithm; empty list if unavailable."
            ),
        ),
    ]
    right_eye: Annotated[
        list[float],
        Field(
            min_length=0,
            max_length=3,
            description=(
                "Screen-px [x,y] or camera-mm [x,y(,z)]; 2D or 3D depending on algorithm; empty list if unavailable."
            ),
        ),
    ]

    model_config = ConfigDict(
        title="GazePoint",
        json_schema_extra={
            "description": (
                "Point-of-gaze coordinates for two eyes in either screen-pixel or camera-millimeter space."
            ),
        },
    )


class GazeData(BaseModel):
    success: bool = Field(..., description="Whether gaze estimation succeeded for this face.")
    gaze_screen_px: GazePoint = Field(
        ...,
        description=(
            "Per-eye point-of-gaze coordinates in screen-space pixels. "
            "The origin is at the left top corner of the screen. "
            "The coordinate system is shown as Fig. 1."
        ),
    )
    gaze_camera_mm: GazePoint = Field(
        ...,
        description=(
            "Per-eye point-of-gaze coordinates in the camera coordinate system, "
            "measured in millimeters. The coordinate origin is located at the camera "
            "optical center. Depending on the gaze estimation algorithm, the "
            "point-of-gaze can be represented either as a 2D coordinate on the "
            "camera image plane or as a 3D point in camera space. The coordinate "
            "definitions for 2D and 3D gaze_camera_mm are illustrated in Fig. 2 "
            "and Fig. 3, respectively. Different algorithms may natively output in "
            "different coordinate frames; all values are normalized to the "
            "conventions documented here before being returned."
        ),
    )

    model_config = ConfigDict(
        title="GazeData",
        json_schema_extra={
            "description": "Gaze estimation result for a single face.",
        },
    )


class GazeScreen(BaseModel):
    gaze: GazeData

    model_config = ConfigDict(
        title="GazeScreen",
        json_schema_extra={
            "description": "Wrapper for per-face gaze data in face/gaze_screen schema.",
        },
    )


class Report(BaseModel):
    face_gaze_screen: list[GazeScreen]

    model_config = ConfigDict(
        title="face/gaze_screen",
        json_schema_extra={
            "x-figures": [
                {
                    "title": "Coordinate system for **gaze_screen_px**",
                    "url": "assets/gaze_screen_px.png",
                    "width": "200px",
                },
                {
                    "title": "Coordinate system for **gaze_camera_mm(2D)**",
                    "url": "assets/gaze_camera_mm_2d.png",
                    "width": "200px",
                },
                {
                    "title": "Coordinate system for **gaze_camera_mm(3D)**",
                    "url": "assets/gaze_camera_mm_3d.png",
                    "width": "200px",
                },
            ],
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
