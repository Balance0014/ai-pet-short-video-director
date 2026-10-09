# Behavioral evaluation

These cases test the decisions this skill is meant to change. They are **not** recorded model results.

For each case, start a fresh agent session with the skill installed, send only its `prompt`, save the full response, and grade each `checks` item against visible output. A check fails if the response merely implies the behavior or contradicts it elsewhere. Keep the response and grade as evidence before reporting a pass rate. Do not grade several cases in one carried-over session.

Package validation is separate: `python3 scripts/check_package.py` checks files and portability, not model behavior or film quality. Real creative and audience claims require inspected media and comparable published data.
