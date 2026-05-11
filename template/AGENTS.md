# Boomi Integration Project

This is a Boomi-oriented workspace. Load and use the `boomi-integration` skill for all Boomi tasks.

The skill contains `.sh` CLI tools for all common tasks. Always look for these tools as a first option. The path to run them is `<skill-base-path>/scripts/*`.

If you find yourself needing to craft custom `curl` — stop and discuss with the user before proceeding. This is unexpected.

If you attempt to call into the Boomi platform and get an auth error — stop and discuss with the user before proceeding. Repeated calls with invalid auth will get us locked out of the platform.

## Canvas Arranging
After building or modifying a Boomi process, run the canvas arranger:

```bash
python3 <skill-base-path>/scripts/boomi-canvas-arrange.py active-development/processes/<process>.xml
```

## Make It Good
If the user asks you to "make it good," work through the task thoughtfully, accurately, and mindfully, thinking step by step.
