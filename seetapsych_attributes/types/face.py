# -*- coding: utf-8 -*-

from typing import TypedDict


__all__ = [
    'BBox',
    'FaceDetection',
    'Landmarks',
    'FaceLandmarks',
    'Selection',
    'FaceSelection',
    'ActionUnits',
    'FaceActionUnits',
    'Expression',
    'FaceExpression',
    'DenseLandmarks',
    'FaceDenseLandmarks',
    'MeshLandmarks',
    'FaceMesh',
    'GazePoint',
    'GazeData',
    'GazeScreen',
    'FaceGazeScreen',
    'HeartRate',
    'FaceHeartRate',
    'DimensionalAffect',
    'FaceDimensionalAffect',
]


class BBox(TypedDict):
    xyxy: list[float]
    score: float


FaceDetection = list[BBox]


class Landmarks(TypedDict):
    landmarks: list[float]


FaceLandmarks = list[Landmarks]


class Selection(TypedDict):
    pid: int


FaceSelection = Selection


class ActionUnits(TypedDict, total=False):
    AU1: float
    AU2: float
    AU4: float
    AU5: float
    AU6: float
    AU7: float
    AU9: float
    AU10: float
    AU12: float
    AU15: float
    AU17: float
    AU20: float
    AU23: float
    AU24: float
    AU25: float
    AU26: float


FaceActionUnits = list[ActionUnits]


class Expression(TypedDict, total=False):
    neutral: float
    anger: float
    disgust: float
    fear: float
    happy: float
    sad: float
    surprise: float


FaceExpression = list[Expression]


class DenseLandmarks(TypedDict):
    landmarks: list[float]


FaceDenseLandmarks = list[DenseLandmarks]


class MeshLandmarks(TypedDict):
    normalized_3d_landmarks: list[float]


FaceMesh = list[MeshLandmarks]


class GazePoint(TypedDict):
    left_eye: list[float]
    right_eye: list[float]


class GazeData(TypedDict):
    success: bool
    gaze_screen_px: GazePoint
    gaze_cm: GazePoint


class GazeScreen(TypedDict):
    gaze: GazeData


FaceGazeScreen = list[GazeScreen]


class HeartRate(TypedDict, total=False):
    fps: float
    wait_seconds: float
    hr_bpm: float


FaceHeartRate = HeartRate


class DimensionalAffect(TypedDict):
    valence: float
    arousal: float


FaceDimensionalAffect = list[DimensionalAffect]
