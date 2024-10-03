# The Protocol

## Data Types
|Name|Description|
|----|-----------|
|String| 1 byte that represents the length and then utf-8 encoded values|

## Message Types

### Hello World
|Name|Type|Description|
|----|----|-----------|
|Packet ID|Byte|0x00|

### Sync Brain Config
Goes from brain to controller with all config values
|Name|Type|Description|
|----|----|-----------|
|Packet ID|Byte|0x01|
|Websocket URL|String| The websocket url that the brain connects to/is currently connected to|
|Camera FPS|Integer||

### Movement
|Name|Type|Description|
|----|----|-----------|
|Packet ID|Byte|0x02|
|Direction|Vector2|The direction to move in (1,1) is NE|
