# -*- coding: utf-8 -*-

from typing import TypedDict


__all__ = [
    'HeadBBox',
    'HeadDetection',
    'HeadSelection',
    'HeadGazePoint',
    'HeadGazePointList',
    'SocialGazePerson',
    'HeadSocialGaze',
]


class HeadBBox(TypedDict):
    xyxy: list[int]
    score: float


HeadDetection = list[HeadBBox]


class HeadSelection(TypedDict):
    count: int
    selected_indices: list[int]


class HeadGazePoint(TypedDict):
    head_location_xyxy: list[int]
    gaze_point_px: list[float]
    heatmap: list[list[float]]


HeadGazePointList = list[HeadGazePoint]


class SocialGazePerson(TypedDict):
    head_location_xyxy: list[int]
    gaze_point_px: list[float]
    heatmap: list[list[float]]
    social_gaze_id: int
    social_gaze_label: str


class HeadSocialGaze(TypedDict, total=False):
    success: bool
    principal: SocialGazePerson
    associate: SocialGazePerson
