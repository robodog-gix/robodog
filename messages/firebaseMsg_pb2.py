# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: firebaseMsg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='firebaseMsg.proto',
  package='robodogs',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x11\x66irebaseMsg.proto\x12\x08robodogs\"\x1b\n\x0b\x46irebaseMsg\x12\x0c\n\x04json\x18\x01 \x01(\tb\x06proto3')
)




_FIREBASEMSG = _descriptor.Descriptor(
  name='FirebaseMsg',
  full_name='robodogs.FirebaseMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='json', full_name='robodogs.FirebaseMsg.json', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=58,
)

DESCRIPTOR.message_types_by_name['FirebaseMsg'] = _FIREBASEMSG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FirebaseMsg = _reflection.GeneratedProtocolMessageType('FirebaseMsg', (_message.Message,), dict(
  DESCRIPTOR = _FIREBASEMSG,
  __module__ = 'firebaseMsg_pb2'
  # @@protoc_insertion_point(class_scope:robodogs.FirebaseMsg)
  ))
_sym_db.RegisterMessage(FirebaseMsg)


# @@protoc_insertion_point(module_scope)
