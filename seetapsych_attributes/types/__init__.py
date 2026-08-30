# -*- coding: utf-8 -*-

from typing import TypedDict

from .face import (
    ActionUnits,
    BBox,
    DenseLandmarks,
    DimensionalAffect,
    Expression,
    FaceActionUnits,
    FaceDenseLandmarks,
    FaceDetection,
    FaceDimensionalAffect,
    FaceExpression,
    FaceGazeScreen,
    FaceHeartRate,
    FaceLandmarks,
    FaceMesh,
    FaceSelection,
    GazeData,
    GazePoint,
    GazeScreen,
    HeartRate,
    Landmarks,
    MeshLandmarks,
    Selection,
)
from .head import (
    HeadBBox,
    HeadDetection,
    HeadGazePoint,
    HeadGazePointList,
    HeadSelection,
    HeadSocialGaze,
    SocialGazePerson,
)

__all__ = [
    # face
    "BBox",
    "FaceDetection",
    "Landmarks",
    "FaceLandmarks",
    "Selection",
    "FaceSelection",
    "ActionUnits",
    "FaceActionUnits",
    "Expression",
    "FaceExpression",
    "DenseLandmarks",
    "FaceDenseLandmarks",
    "MeshLandmarks",
    "FaceMesh",
    "GazePoint",
    "GazeData",
    "GazeScreen",
    "FaceGazeScreen",
    "HeartRate",
    "FaceHeartRate",
    "DimensionalAffect",
    "FaceDimensionalAffect",
    # head
    "HeadBBox",
    "HeadDetection",
    "HeadSelection",
    "HeadGazePoint",
    "HeadGazePointList",
    "SocialGazePerson",
    "HeadSocialGaze",
    # top-level
    "Report",
]


class Report(TypedDict, total=False):
    """Aggregated per-frame SeetaPsych attribute report.

    Combines all face and head module outputs plus capture-time metadata.
    All fields are optional since each module can be enabled independently.
    """

    # list of detected face bounding boxes with confidence scores
    face_detection: FaceDetection
    # list of 5-point basic landmarks per detected face
    face_landmarks: FaceLandmarks
    # currently selected face PID (1-based)
    face_selection: FaceSelection
    # per-face Facial Action Unit (FACS) confidence values
    face_action_units: FaceActionUnits
    # per-face 7-class discrete expression confidences
    face_expression: FaceExpression
    # per-face 280-point dense landmarks (560 floats)
    face_dense_landmarks: FaceDenseLandmarks
    # per-face 468-point 3D mesh (1404 normalized floats)
    face_mesh: FaceMesh
    # per-face per-eye screen-space + camera-space gaze vectors
    face_gaze_screen: FaceGazeScreen
    # heart rate in BPM, present when buffered
    face_heart_rate: FaceHeartRate
    # per-face continuous valence / arousal affect scores
    face_dimensional_affect: FaceDimensionalAffect
    # list of multi-person head bounding boxes
    head_detection: HeadDetection
    # top-N head selection result (count + original indices)
    head_selection: HeadSelection
    # per-head 2D scene gaze target point with associated heatmap
    head_gaze_point: HeadGazePointList
    # dyadic social gaze relations between two detected people
    head_social_gaze: HeadSocialGaze
    # frame capture timestamp in seconds since epoch
    timestamp: float
    # monotonic frame counter since stream start
    frame_tick: int
