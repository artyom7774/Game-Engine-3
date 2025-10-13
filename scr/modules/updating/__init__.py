from ..updating import v3110to3120, v3120to3121, v3121to3122, v3122to3123, v3123to3124, v3124to3125, v3125to3126, v3126to3130, v3130to3131, v3131to3132

versionsUpdatingTree = {
    "3.11.0": [
        "3.12.0"
    ],
    "3.12.0": [
        "3.12.1"
    ],
    "3.12.1": [
        "3.12.2"
    ],
    "3.12.2": [
        "3.12.3"
    ],
    "3.12.3": [
        "3.12.4"
    ],
    "3.12.4": [
        "3.12.5"
    ],
    "3.12.5": [
        "3.12.6"
    ],
    "3.12.6": [
        "3.13.0"
    ],
    "3.13.0": [
        "3.13.1"
    ],
    "3.13.1": [
        "3.13.2"
    ]
}

versionsUpdatingFunctions = {
    "3.11.0 -> 3.12.0": lambda name: v3110to3120.updating(name),
    "3.12.0 -> 3.12.1": lambda name: v3120to3121.updating(name),
    "3.12.1 -> 3.12.2": lambda name: v3121to3122.updating(name),
    "3.12.2 -> 3.12.3": lambda name: v3122to3123.updating(name),
    "3.12.3 -> 3.12.4": lambda name: v3123to3124.updating(name),
    "3.12.4 -> 3.12.5": lambda name: v3124to3125.updating(name),
    "3.12.5 -> 3.12.6": lambda name: v3125to3126.updating(name),
    "3.12.6 -> 3.13.0": lambda name: v3126to3130.updating(name),
    "3.13.0 -> 3.13.1": lambda name: v3130to3131.updating(name),
    "3.13.1 -> 3.13.2": lambda name: v3130to3131.updating(name)
}
