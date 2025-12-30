COMMAND_SCHEMA = {
    "robotId": "string",
    "cmd": ["forward", "backward", "left", "right", "rotate", "rotate-reverse", "slow speed", "fast speed"],
    "value": "array[float]",
    "timeStamp": "string",  # point: this type in input must be datetime
}
ERROR_SCHEMA = {
    "robotId": "string",
    "error-code": ["400", "404", "500"],
    "severity": ["low", "medium", "high"],
    "notification": {
        "success": "boolean",
        "message": "string"
    },
    "timeStamp": "string",  # point: this type in input must be datetime
}
STATE_SCHEMA = {
    "robotId": "string",
    "battery": "int",
    "speed": "float",
    "mode": ["human", "ai", "emergency"],
    "currentLocation": "string",
    "status": ["good", "perfect", "have problem"],
    "timeStamp": "string",  # point: this type in input must be datetime
}
GROUP_SCHEMA = {
    "robotLeaderId": "string",
    "cmds": [COMMAND_SCHEMA],
    "timeStamp": "string",  # point: this type in input must be datetime
}

WARNING_SCHEMA = {
    "robotId": "string",
    # 300: low battery, 301: connectivity problem, 302: high power voltage
    "warning-code": ["300", "301", "302"],
    "severity": ["low", "medium", "high"],
    "notification": {
        "success": "boolean",
        "message": "string"
    },
    "timeStamp": "string",  # point: this type in input must be datetime
}

STREAM_STATE_SCHEMA = {
    "robotId": "string",
    "resolution": "int",
    "internetStatus": ["low", "good", "perfect"],
    "timeStamp": "string",
    "port": "int"
}
