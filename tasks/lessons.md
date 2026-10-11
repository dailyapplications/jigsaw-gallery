# Lessons / working rules
- Inherit pdfreader's rules (see ../pdfreader/tasks/lessons.md): never touch ad SDKs / DataStore in `Application.onCreate` outside the main process; no ads over content or before content opens; smoke-test the R8 release build; check `adb logcat -s AndroidRuntime:E`.
- Shell cwd resets between Bash calls: always `cd` with absolute paths.
- Museum APIs rate-limit bursts (Met returns 403): throttle, back off, run few categories in parallel.
- Always write progress to tasks/status.md after each chunk (owner may be away; limits may hit).
- Positive AND negative tests for everything; no mutation testing.
