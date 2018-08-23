from enum import Enum
from .mockMsg_pb2 import MockMsg
from .cameraFrameMsg_pb2 import CameraFrameMsg
from .sensorMsg_pb2 import SensorMsg
from .firebaseMsg_pb2 import FirebaseMsg

class MsgType(Enum):
    MOCK_MSG = 0
    CAMERA_FRAME_MSG = 1
    SENSOR_MSG = 2
    FIREBASE_MSG = 3

message_buffers = {
    MsgType.MOCK_MSG: MockMsg,
    MsgType.CAMERA_FRAME_MSG: CameraFrameMsg,
    MsgType.SENSOR_MSG: SensorMsg,
    MsgType.FIREBASE_MSG: FirebaseMsg
}

__all__ = ['MsgType', 'message_buffers', 'MockMsg', 'CameraFrameMsg', 'SensorMsg', 'FirebaseMsg']
