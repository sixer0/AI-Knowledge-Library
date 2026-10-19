---



name: gsp-dispatch-troubleshooting



description: Recover stuck GSP bridge dispatches and queue hangs.



version: 1.1.0


author: GSP Swarm



license: MIT



hermes:



  tags: [gsp, bridge, dispatch, troubleshooting, windows]



  related_skills: [gsp-orchestration-execution, gsp-fleet-smoke-test]



---







# GSP Dispatch Troubleshooting







## When to Use







Use when a GSP bridge dispatch is stuck or hung: tasks remain `running` without progress, bridge logs show repeated `cron list failed` / `request failed` timeouts, or queued work is blocked behind a hung dispatch.







## Detection







1. Query `AgentRequest` for tasks with `status='running'` older than expected.



2. Cross-check Windows process list: the dispatch's `hermes -p <profile> -z ...` process should have child Python/Node workers doing actual work. If CPU time is flat and no meaningful children exist, it is likely a zombie/hung delegation.



3. Bridge log tells the story: repeated `hermes CLI timeout after 15000ms: cron list --all` or `hermes CLI timeout after 1800000ms: -p <profile> -z ...` while one task is `running` means the bridge queue is blocked.







## Recovery Sequence







Do these in order; verify after each step.







### 1. Stop the zombie process tree







On Windows, `taskkill /F /T /PID <pid>` is required because child processes often survive parent termination.







```bash



# Replace with the actual stuck PID(s)



taskkill /F /T /PID <dispatch_pid>



taskkill /F /T /PID <child_pid_1>



taskkill /F /T /PID <child_pid_2>



```







Verify with `tasklist | grep <pid>` — must return empty.







### 2. Reset DB state







Update the stuck `AgentRequest` row from `running` to `failed` so the bridge queue can advance:







```sql



UPDATE "AgentRequest" SET status='failed', "updatedAt"=now() WHERE id='<request_id>' AND status='running';



```







Verify with a fresh query: the row must show `failed`, and no other rows should remain `running` or `queued`.







### 3. Confirm bridge and queue health







- `tail` the bridge log: new entries should appear after the previous timeout cluster.



- Re-run a lightweight bridge command (e.g., `hermes cron list --all`) to confirm the CLI is no longer blocked.



- Check `AgentRequest` again: no residual `running` rows, queued work should either stay queued for the next cycle or advance to `running`/`done`.







## Pitfalls







- **Do not restart the bridge mid-investigation.** Restarting while a stuck dispatch is still `running` in DB can cause duplicate kanban cards or orphaned contract records.



- **Bridge timeout cascade is a symptom, not the root cause.** Fixing the dispatch unblocks cron/status/daily-brief operations automatically.



- **On Windows, `Stop-Process` alone is insufficient.** Always use `taskkill /F /T /PID` for full tree termination.



- **Do not reset a running task to `done`.** Use `failed` unless you have independent proof the work actually completed.



- **Check child process command lines, not just parent PIDs.** A dispatch may spawn multiple `hermes -p <profile> -z ...` layers; kill the actual worker tree, not just the outermost wrapper.
- **Kartu ber-status `review` yang crash < 65 detik tanpa tool call dengan log `Unknown skill(s): ...`** = kelas review-claim-skill-crash (preseden S15 GAYA-AHLI 05-10): load `references/review-claim-skill-crash.md`. Re-run buta dipastikan mati identik - putuskan dari artefak beku dan/atau aktivasikan skill via jalur manifest.







## Verification Checklist



- Windows HQ/Bridge/Cron ops recipes (dispatch via DB, force-done gate, drift_skip cron, snapshot re-sync): load `references/windows-hq-bridge-ops.md`.








- [ ] No Windows processes remain for the stuck dispatch PID(s)



- [ ] DB row status changed from `running` to `failed`



- [ ] Bridge log resumes normal entries (no new timeout clusters)



- [ ] `hermes cron list --all` returns within normal time (<10s)



- [ ] No other `running` or `queued` tasks are blocked



- [ ] Kanban cards for the affected request are in a consistent state (complete/block, not orphaned)


## References

- Windows HQ/Bridge/Cron ops recipes (dispatch via DB, force-done gate, drift_skip cron, snapshot re-sync): load `references/windows-hq-bridge-ops.md`.

