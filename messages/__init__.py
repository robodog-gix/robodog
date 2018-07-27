from enum import Enum
from .mockMsg_pb2 import MockMsg
from .cameraFrameMsg_pb2 import CameraFrameMsg
from .sensorMsg_pb2 import SensorMsg

class MsgType(Enum):
    MOCK_MSG = 0
    CAMERA_FRAME_MSG = 1
    SENSOR_MSG = 2

message_buffers = {
    MsgType.MOCK_MSG: MockMsg,
    MsgType.CAMERA_FRAME_MSG: CameraFrameMsg,
    MsgType.SENSOR_MSG: SensorMsg
}

__all__ = ['MsgType', 'message_buffers', 'MockMsg', 'CameraFrameMsg', 'SensorMsg']
