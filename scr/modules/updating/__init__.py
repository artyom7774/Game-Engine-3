from ..updating import v3110to3120

versionsUpdatingTree = {
    "3.11.0": [
        "3.12.0"
    ]
}

versionsUpdatingFunctions = {
    "3.11.0 -> 3.12.0": lambda name: v3110to3120.updating(name)
}
