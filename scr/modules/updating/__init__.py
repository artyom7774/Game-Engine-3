from ..updating import v3110to3120, v3120to3121

versionsUpdatingTree = {
    "3.11.0": [
        "3.12.0"
    ],
    "3.12.0": [
        "3.12.1"
    ]
}

versionsUpdatingFunctions = {
    "3.11.0 -> 3.12.0": lambda name: v3110to3120.updating(name),
    "3.12.0 -> 3.12.1": lambda name: v3120to3121.updating(name)
}
