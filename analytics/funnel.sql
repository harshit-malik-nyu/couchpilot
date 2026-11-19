-- Event rows are task-scoped; cohort inclusion starts with request_started.
-- Synthetic demonstration, not product adoption or human behavioral evidence.
WITH tasks AS (
 SELECT session_id, request_id,
 MAX(event='request_started') initiated,
 MAX(event='proposal_ready') ready,
 MAX(event='actions_applied') applied,
 MAX(event='seek_undone') undone,
 MAX(event='request_cancelled') cancelled
 FROM events GROUP BY session_id,request_id
)
SELECT SUM(initiated) initiated_tasks,
 SUM(initiated*ready) reviewed_proposals,
 SUM(initiated*applied) applied_tasks,
 SUM(initiated*applied*(1-undone)) applied_not_undone,
 SUM(initiated*cancelled) cancelled_tasks
FROM tasks;
-- applied_not_undone is only a proxy; it does not prove intended-task success.
