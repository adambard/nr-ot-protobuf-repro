This repo reproduces an issue using the newrelic library together with the opentelemetry

### Setup

This project uses [Poetry](https://python-poetry.org/) cuz it's what I had handy. Install poetry,
then checkout the repo and run `poetry install` to install the deps (newrelic and opentelemetry).

### Issue reproduction

The files `repro1.py`, `repro2.py`, and `repro3.py` in the `nr_ot_protobuf_repro` directory
 create 3 different scenarios. They can be run with poetry like: 

```
poetry run python nr_ot_protobuf_repro/reproX.py
```

#### `repro1.py`

This file simply imports the two libraries to demonstrate the error that occurs.

#### `repro2.py`

This file attempts to use the workaround specified in [this comment](https://github.com/newrelic/newrelic-python-agent/issues/1154)
on a similar issue from newrelic-python-agent's github. It does not change the outcome,
probably because protobuf registration happens at import time

In both of the above cases, the traceback is the same:

```
  File "/home/adam/Projects/experiments/nr-ot-protobuf-repro/nr_ot_protobuf_repro/repro2.py", line 5, in <module>
    import opentelemetry.exporter.otlp.proto.http.metric_exporter;
  File "/home/adam/.cache/pypoetry/virtualenvs/nr-ot-protobuf-repro-epjq6xo_-py3.10/lib/python3.10/site-packages/opentelemetry/exporter/otlp/proto/http/metric_exporter/__init__.py", line 25, in <module>
    from opentelemetry.exporter.otlp.proto.common._internal import (
  File "/home/adam/.cache/pypoetry/virtualenvs/nr-ot-protobuf-repro-epjq6xo_-py3.10/lib/python3.10/site-packages/opentelemetry/exporter/otlp/proto/common/_internal/__init__.py", line 31, in <module>
    from opentelemetry.proto.common.v1.common_pb2 import (
  File "/home/adam/.cache/pypoetry/virtualenvs/nr-ot-protobuf-repro-epjq6xo_-py3.10/lib/python3.10/site-packages/opentelemetry/proto/common/v1/common_pb2.py", line 17, in <module>
    DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*opentelemetry/proto/common/v1/common.proto\x12\x1dopentelemetry.proto.common.v1\"\x8c\x02\n\x08\x41nyValue\x12\x16\n\x0cstring_value\x18\x01 \x01(\tH\x00\x12\x14\n\nbool_value\x18\x02 \x01(\x08H\x00\x12\x13\n\tint_value\x18\x03 \x01(\x03H\x00\x12\x16\n\x0c\x64ouble_value\x18\x04 \x01(\x01H\x00\x12@\n\x0b\x61rray_value\x18\x05 \x01(\x0b\x32).opentelemetry.proto.common.v1.ArrayValueH\x00\x12\x43\n\x0ckvlist_value\x18\x06 \x01(\x0b\x32+.opentelemetry.proto.common.v1.KeyValueListH\x00\x12\x15\n\x0b\x62ytes_value\x18\x07 \x01(\x0cH\x00\x42\x07\n\x05value\"E\n\nArrayValue\x12\x37\n\x06values\x18\x01 \x03(\x0b\x32\'.opentelemetry.proto.common.v1.AnyValue\"G\n\x0cKeyValueList\x12\x37\n\x06values\x18\x01 \x03(\x0b\x32\'.opentelemetry.proto.common.v1.KeyValue\"O\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32\'.opentelemetry.proto.common.v1.AnyValue\"\x94\x01\n\x14InstrumentationScope\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12;\n\nattributes\x18\x03 \x03(\x0b\x32\'.opentelemetry.proto.common.v1.KeyValue\x12 \n\x18\x64ropped_attributes_count\x18\x04 \x01(\rB{\n io.opentelemetry.proto.common.v1B\x0b\x43ommonProtoP\x01Z(go.opentelemetry.io/proto/otlp/common/v1\xaa\x02\x1dOpenTelemetry.Proto.Common.V1b\x06proto3')
TypeError: Couldn't build proto file into descriptor pool: duplicate file name opentelemetry/proto/common/v1/common.proto

#### `repro3.py`

This file imports `newrelic.agent` after `opentelemetry.exporter.otlp.proto.http.metric_exporter`.
This seems to avert the issue and is probably the superior workaround. Will test further.
