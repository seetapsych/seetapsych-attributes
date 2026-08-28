# -*- coding: utf-8 -*-

from typing import TypedDict

from .face import (
    BBox,
    FaceDetection,
    Landmarks,
    FaceLandmarks,
    Selection,
    FaceSelection,
    ActionUnits,
    FaceActionUnits,
    Expression,
    FaceExpression,
    DenseLandmarks,
    FaceDenseLandmarks,
    MeshLandmarks,
    FaceMesh,
    GazePoint,
    GazeData,
    GazeScreen,
    FaceGazeScreen,
    HeartRate,
    FaceHeartRate,
    DimensionalAffect,
    FaceDimensionalAffect,
)
from .head import (
    HeadBBox,
    HeadDetection,
    HeadSelection,
    HeadGazePoint,
    HeadGazePointList,
    SocialGazePerson,
    HeadSocialGaze,
)

__all__ = [
    # face
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
    # head
    'HeadBBox',
    'HeadDetection',
    'HeadSelection',
    'HeadGazePoint',
    'HeadGazePointList',
    'SocialGazePerson',
    'HeadSocialGaze',
    # top-level
    'Report',
]


class Report(TypedDict, total=False):
    face_detection: FaceDetection
    face_landmarks: FaceLandmarks
    face_selection: FaceSelection
    face_action_units: FaceActionUnits
    face_expression: FaceExpression
    face_dense_landmarks: FaceDenseLandmarks
    face_mesh: FaceMesh
    face_gaze_screen: FaceGazeScreen
    face_heart_rate: FaceHeartRate
    face_dimensional_affect: FaceDimensionalAffect
    head_detection: HeadDetection
    head_selection: HeadSelection
    head_gaze_point: HeadGazePointList
    head_social_gaze: HeadSocialGaze
    timestamp: float
    frame_tick: int
