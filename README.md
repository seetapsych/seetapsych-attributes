# FaboPsy Attributes

> Face and body based psychology analysis

FaboPsy Lib is a Python library for face- and body-based psychology analysis.
It provides a modular Pipeline/Runner runtime and an optional Streamlit WebUI.

This project is used to manage the specifications for various attribute outputs,
providing a unified standard so that different algorithm implementations can produce interchangeable and reusable module outputs.

## Catalog

- [face/detection](#facedetection) Obtain the face detection results, represented as rectangular bounding boxes.
- [face/landmarks](#facelandmarks) Get facial landmarks for basic alignment, including the centers of the left and right eyes, the nose tip, and the positions of the left and right mouth corners.

<a id="facedetection"></a>

## face/detection

### Properties

- <a id="properties/face_detection"></a>**`face_detection`** *(array, required)*
  - <a id="properties/face_detection/items"></a>**Items**: Refer to *[#/$defs/BBox](#%24defs/BBox)*.

### Definitions

- <a id="%24defs/BBox"></a>**`BBox`** *(object)*
  - <a id="%24defs/BBox/properties/xyxy"></a>**`xyxy`** *(array, required)*: Length must be equal to 4.
    - <a id="%24defs/BBox/properties/xyxy/items"></a>**Items** *(number)*
  - <a id="%24defs/BBox/properties/score"></a>**`score`** *(number, required)*

### Examples

  ```json
  {
      "face_detection": [
          {
              "score": 0.5,
              "xyxy": [
                  100,
                  200,
                  300,
                  400
              ]
          }
      ]
  }
  ```



<a id="facelandmarks"></a>

## face/landmarks

### Properties

- <a id="properties/face_landmarks"></a>**`face_landmarks`** *(array, required)*
  - <a id="properties/face_landmarks/items"></a>**Items**: Refer to *[#/$defs/Landmarks](#%24defs/Landmarks)*.

### Definitions

- <a id="%24defs/Landmarks"></a>**`Landmarks`** *(object)*
  - <a id="%24defs/Landmarks/properties/landmarks"></a>**`landmarks`** *(array, required)*: Length must be equal to 10.
    - <a id="%24defs/Landmarks/properties/landmarks/items"></a>**Items** *(number)*

### Examples

  ```json
  {
      "face_landmarks": [
          {
              "landmarks": [
                  100,
                  100,
                  200,
                  200,
                  300,
                  300,
                  400,
                  400,
                  500,
                  500
              ]
          }
      ]
  }
  ```
