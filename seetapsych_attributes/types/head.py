# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    import numpy  # type: ignore[import-not-found]


__all__ = [
    "HeadBBox",
    "HeadDetection",
    "HeadSelection",
    "HeadGazePoint",
    "HeadGazePointList",
    "SocialGazePerson",
    "HeadSocialGaze",
]


class HeadBBox(TypedDict):
    """Multi-person head detection bounding box with integer pixel coordinates."""

    # [x1, y1, x2, y2] -- integer pixel bounding box
    xyxy: list[int]
    # head detection confidence in [0, 1]
    score: float


# List of all detected head bounding boxes.
HeadDetection = list[HeadBBox]


class HeadSelection(TypedDict):
    """Top-N head selection result with count and original indices."""

    # number of selected head detections
    count: int
    # indices into the original head_detection list, before reordering
    selected_indices: list[int]


class HeadGazePoint(TypedDict):
    """Per-head 2D scene gaze point with associated likelihood heatmap."""

    # [x1, y1, x2, y2] -- head bbox corresponding to this gaze estimate
    head_location_xyxy: list[int]
    # [x, y] -- predicted 2D gaze target on the scene image in pixels
    gaze_point_px: list[float]
    # 2D gaze likelihood heatmap over the scene. numpy.ndarray of float32,
    # shape [image_height, image_width], values in [0, 1] probability range.
    heatmap: "numpy.ndarray"


# List of per-head scene gaze results.
HeadGazePointList = list[HeadGazePoint]


class SocialGazePerson(TypedDict):
    """One participant in a dyadic social-gaze interaction."""

    # [x1, y1, x2, y2] -- this person's head bbox
    head_location_xyxy: list[int]
    # [x, y] -- this person's 2D gaze target in pixels
    gaze_point_px: list[float]
    # 2D gaze likelihood heatmap. numpy.ndarray of float32,
    # shape [image_height, image_width], values in [0, 1] probability range.
    heatmap: "numpy.ndarray"
    # integer class ID of the social gaze relation.
    # ordered mapping: 0=share, 1=mutual, 2=single, 3=miss, 4=void.
    social_gaze_id: int
    # human-readable social gaze label. possible values (index matches social_gaze_id):
    # share, mutual, single, miss, void.
    social_gaze_label: str


class HeadSocialGaze(TypedDict, total=False):
    """Dyadic social-gaze relation between two people.

    `principal` and `associate` represent the left-side and right-side
    participants in the detected interaction.
    """

    # whether at least two heads were detected to run dyadic inference
    success: bool
    # left-side / primary person in the dyadic interaction
    principal: SocialGazePerson
    # right-side / secondary person in the dyadic interaction
    associate: SocialGazePerson
