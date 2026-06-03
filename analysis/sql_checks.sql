-- Workflow priority review
select
  workflow_id,
  workflow_name,
  domain,
  priority_score,
  recommendation
from workflow_priority_queue
order by priority_score desc;

-- Agent evaluation defects
select
  workflow_id,
  eval_type,
  pass_rate,
  defect_severity
from agent_evaluation_matrix
where defect_severity in ('High', 'Medium')
order by pass_rate asc;

-- Training readiness queue
select
  team,
  module,
  readiness_score,
  blocker,
  next_action
from training_rollout_plan
where readiness_score < 75
order by readiness_score asc;
