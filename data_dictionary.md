# Data Dictionary

| Table | Grain | Purpose |
|---|---|---|
| `workflow_candidates.csv` | AI agent workflow | Candidate workflows, problem statements, source systems, and scoring inputs. |
| `discovery_signals.csv` | Stakeholder signal | Discovery evidence used to size pain, urgency, and requirements clarity. |
| `agent_eval_cases.csv` | Evaluation case | Test prompts, expected behavior, pass rate, defect severity, and review notes. |
| `data_quality_checks.csv` | Data quality check | Readiness gates for source completeness, freshness, policy tags, and review evidence. |
| `training_plan.csv` | Training module | Internal enablement readiness by team, workflow, blocker, and next action. |
| `analysis/outputs/workflow_priority_queue.csv` | Workflow | Ranked decision queue for pilot, repair, discovery, or monitor. |
| `analysis/outputs/prd_workflow_spec.csv` | Spec section | PRD-ready workflow specification for the top-ranked agent. |
| `analysis/outputs/agent_evaluation_matrix.csv` | Evaluation case | Evaluation matrix for the top-ranked agent workflow. |
| `analysis/outputs/training_rollout_plan.csv` | Training action | Lowest-readiness enablement actions for rollout planning. |
