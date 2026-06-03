import csv
import json
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"
OUTPUTS = ANALYSIS / "outputs"
SEED = 5262026
random.seed(SEED)


def clamp(value, low, high):
    return max(low, min(high, value))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


WORKFLOWS = [
    {
        "workflow_id": "AGT-001",
        "workflow_name": "Identity Resolution Intake Agent",
        "domain": "Identity infrastructure",
        "team": "Product",
        "stakeholder": "Platform product manager",
        "problem": "Platform teams need to convert broad data onboarding requests into precise identity match requirements before engineering starts.",
        "agent_goal": "Read discovery notes and produce a source-to-match specification with identifiers, confidence thresholds, exception handling, and approval gates.",
        "source_systems": "CRM notes, data dictionary, API docs, sample files",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 92,
        "data_sensitivity": 74,
        "process_complexity": 76,
        "automation_fit": 84,
        "adoption_pull": 88,
        "effort": 54,
    },
    {
        "workflow_id": "AGT-002",
        "workflow_name": "Fraud Signal Reason Code Agent",
        "domain": "Fraud and risk",
        "team": "Risk products",
        "stakeholder": "Risk product lead",
        "problem": "Risk teams need explainable reason-code summaries when phone, email, address, and identity signals point to elevated risk.",
        "agent_goal": "Summarize risk drivers, confidence, and human review needs from structured signal outputs and policy notes.",
        "source_systems": "Risk score exports, policy notes, product catalog",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 88,
        "data_sensitivity": 86,
        "process_complexity": 82,
        "automation_fit": 78,
        "adoption_pull": 81,
        "effort": 67,
    },
    {
        "workflow_id": "AGT-003",
        "workflow_name": "Lead Builder Audience QA Agent",
        "domain": "Marketing intelligence",
        "team": "Growth product",
        "stakeholder": "Sales enablement lead",
        "problem": "Sales and marketing teams need to validate audience filters, expected volume, pricing, and suppression rules before a lead list is activated.",
        "agent_goal": "Inspect the requested audience, flag impossible or risky criteria, and produce a buyer-ready fulfillment brief.",
        "source_systems": "Audience filter export, pricing table, suppression rules",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 84,
        "data_sensitivity": 68,
        "process_complexity": 63,
        "automation_fit": 90,
        "adoption_pull": 86,
        "effort": 46,
    },
    {
        "workflow_id": "AGT-004",
        "workflow_name": "Investigation Research Brief Agent",
        "domain": "Investigations",
        "team": "Customer operations",
        "stakeholder": "Investigation support manager",
        "problem": "Research teams need structured briefs that separate verified identity context from leads that still require review.",
        "agent_goal": "Turn research notes and public-record extracts into a concise brief with citations, confidence labels, and unresolved questions.",
        "source_systems": "Research notes, search exports, case templates",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 79,
        "data_sensitivity": 89,
        "process_complexity": 85,
        "automation_fit": 69,
        "adoption_pull": 72,
        "effort": 70,
    },
    {
        "workflow_id": "AGT-005",
        "workflow_name": "Data Delivery Onboarding Agent",
        "domain": "Data delivery",
        "team": "Implementation",
        "stakeholder": "Implementation manager",
        "problem": "Implementation teams need faster handoffs for API, batch, Snowflake, and cloud-storage data delivery decisions.",
        "agent_goal": "Synthesize client requirements into delivery mode, schema mapping, refresh cadence, test plan, and launch blockers.",
        "source_systems": "Implementation forms, schema registry, client notes",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 91,
        "data_sensitivity": 78,
        "process_complexity": 80,
        "automation_fit": 86,
        "adoption_pull": 83,
        "effort": 58,
    },
    {
        "workflow_id": "AGT-006",
        "workflow_name": "Compliance Exception Review Agent",
        "domain": "Governance",
        "team": "Compliance",
        "stakeholder": "Compliance operations lead",
        "problem": "Teams need a repeatable review of data-use exceptions before a customer-facing workflow is approved.",
        "agent_goal": "Classify the request, identify policy conflicts, draft reviewer questions, and route to the right approver.",
        "source_systems": "Policy docs, request forms, contract notes",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 77,
        "data_sensitivity": 94,
        "process_complexity": 88,
        "automation_fit": 66,
        "adoption_pull": 70,
        "effort": 72,
    },
    {
        "workflow_id": "AGT-007",
        "workflow_name": "Customer Training Workshop Agent",
        "domain": "Enablement",
        "team": "Customer success",
        "stakeholder": "Enablement lead",
        "problem": "Customer-facing teams need role-specific training packs when new identity intelligence workflows launch.",
        "agent_goal": "Convert release notes, FAQs, and workflow examples into workshop agendas, scripts, and practice exercises.",
        "source_systems": "Release notes, FAQs, support macros",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 73,
        "data_sensitivity": 42,
        "process_complexity": 48,
        "automation_fit": 92,
        "adoption_pull": 89,
        "effort": 34,
    },
    {
        "workflow_id": "AGT-008",
        "workflow_name": "Data Quality Drift Digest Agent",
        "domain": "Data quality",
        "team": "Data operations",
        "stakeholder": "Data operations lead",
        "problem": "Data operations teams need digestible drift summaries when source freshness, match rates, and exception volumes move together.",
        "agent_goal": "Review quality metrics, explain likely drivers, draft follow-up checks, and prepare the weekly stakeholder note.",
        "source_systems": "Quality dashboard exports, incident queue, source status notes",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 87,
        "data_sensitivity": 71,
        "process_complexity": 74,
        "automation_fit": 88,
        "adoption_pull": 80,
        "effort": 52,
    },
    {
        "workflow_id": "AGT-009",
        "workflow_name": "Sales Discovery Call Synthesizer",
        "domain": "Sales intelligence",
        "team": "Sales",
        "stakeholder": "Sales leader",
        "problem": "Sales teams need reliable discovery summaries that identify use case, data need, urgency, decision process, and next action.",
        "agent_goal": "Turn call notes into structured opportunity intelligence and product feedback without losing customer nuance.",
        "source_systems": "Call notes, CRM fields, product taxonomy",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 82,
        "data_sensitivity": 51,
        "process_complexity": 57,
        "automation_fit": 91,
        "adoption_pull": 91,
        "effort": 38,
    },
    {
        "workflow_id": "AGT-010",
        "workflow_name": "Internal AI Agent Review Coach",
        "domain": "AI operations",
        "team": "Product operations",
        "stakeholder": "AI program lead",
        "problem": "Teams need a common rubric for reviewing agent outputs before internal workflows spread across departments.",
        "agent_goal": "Score agent drafts, identify missing guardrails, suggest prompt improvements, and prepare coaching notes for builders.",
        "source_systems": "Agent specs, test outputs, review rubric",
        "delivery_surface": "Claude Cowork workspace",
        "base_impact": 89,
        "data_sensitivity": 62,
        "process_complexity": 69,
        "automation_fit": 87,
        "adoption_pull": 94,
        "effort": 41,
    },
]


SIGNAL_TYPES = [
    "stakeholder interview",
    "support escalation",
    "sales note",
    "operations retro",
    "training request",
    "quality review",
]
EVAL_TYPES = [
    "spec completeness",
    "source grounding",
    "sensitive data handling",
    "workflow accuracy",
    "human handoff clarity",
    "repeatability",
]
TRAINING_TEAMS = [
    "Product",
    "Risk products",
    "Customer operations",
    "Implementation",
    "Sales",
    "Customer success",
    "Data operations",
    "Compliance",
]


def build_source_data():
    workflow_rows = []
    for item in WORKFLOWS:
        workflow_rows.append(
            {
                "workflow_id": item["workflow_id"],
                "workflow_name": item["workflow_name"],
                "domain": item["domain"],
                "team": item["team"],
                "stakeholder": item["stakeholder"],
                "problem": item["problem"],
                "agent_goal": item["agent_goal"],
                "source_systems": item["source_systems"],
                "delivery_surface": item["delivery_surface"],
                "base_impact": item["base_impact"],
                "data_sensitivity": item["data_sensitivity"],
                "process_complexity": item["process_complexity"],
                "automation_fit": item["automation_fit"],
                "adoption_pull": item["adoption_pull"],
                "effort": item["effort"],
            }
        )

    signals = []
    start = date(2026, 1, 5)
    for idx in range(260):
        workflow = random.choices(WORKFLOWS, weights=[w["base_impact"] for w in WORKFLOWS])[0]
        signal_type = random.choice(SIGNAL_TYPES)
        urgency = clamp(random.gauss(workflow["adoption_pull"] / 12, 1.5), 1, 10)
        pain = clamp(random.gauss(workflow["base_impact"] / 11, 1.3), 1, 10)
        clarity = clamp(random.gauss(7.6 - workflow["process_complexity"] / 35, 1.2), 1, 10)
        signals.append(
            {
                "signal_id": f"SIG-{idx + 1:04d}",
                "signal_date": (start + timedelta(days=idx % 112)).isoformat(),
                "workflow_id": workflow["workflow_id"],
                "signal_type": signal_type,
                "stakeholder_team": workflow["team"],
                "pain_score": round(pain, 1),
                "urgency_score": round(urgency, 1),
                "requirements_clarity": round(clarity, 1),
                "sample_note": f"{workflow['stakeholder']} needs {workflow['workflow_name'].lower()} to reduce manual handoff and preserve review control.",
            }
        )

    eval_cases = []
    for workflow in WORKFLOWS:
        for idx, eval_type in enumerate(EVAL_TYPES, start=1):
            base = (
                workflow["automation_fit"] * 0.34
                + workflow["base_impact"] * 0.18
                + workflow["adoption_pull"] * 0.18
                + (100 - workflow["process_complexity"]) * 0.16
                + (100 - workflow["data_sensitivity"]) * 0.14
            )
            noise = random.gauss(0, 6)
            pass_rate = clamp(base + noise, 35, 98)
            severity = "High" if pass_rate < 62 else "Medium" if pass_rate < 78 else "Low"
            eval_cases.append(
                {
                    "test_id": f"TST-{workflow['workflow_id'][-3:]}-{idx:02d}",
                    "workflow_id": workflow["workflow_id"],
                    "eval_type": eval_type,
                    "test_prompt": f"Review the {workflow['workflow_name']} output for {eval_type}.",
                    "expected_behavior": "Use only supplied source files, state confidence, and route unresolved decisions to a human owner.",
                    "pass_rate": round(pass_rate, 1),
                    "defect_severity": severity,
                    "review_note": "Ready for pilot" if severity == "Low" else "Needs prompt guardrail and reviewer checklist update",
                }
            )

    data_checks = []
    check_names = [
        "Identifier completeness",
        "Source freshness",
        "Consent and use-case tag",
        "Reason code coverage",
        "Schema mapping coverage",
        "Suppression rule coverage",
        "Human approval evidence",
        "Sensitive field masking",
        "Reviewer traceability",
        "Output citation coverage",
    ]
    for workflow in WORKFLOWS:
        for idx, check_name in enumerate(check_names[:3], start=1):
            score = clamp(random.gauss(84 - workflow["data_sensitivity"] / 8 + workflow["automation_fit"] / 12, 7), 42, 98)
            data_checks.append(
                {
                    "check_id": f"DQ-{workflow['workflow_id'][-3:]}-{idx}",
                    "workflow_id": workflow["workflow_id"],
                    "check_name": check_name,
                    "pass_rate": round(score, 1),
                    "owner": workflow["team"],
                    "gate": "Pilot blocker" if score < 70 else "Monitor" if score < 84 else "Clear",
                }
            )

    training_rows = []
    for team in TRAINING_TEAMS:
        for wave in range(1, 5):
            workflow = random.choice(WORKFLOWS)
            readiness = clamp(random.gauss(workflow["adoption_pull"] - wave * 2, 9), 35, 96)
            training_rows.append(
                {
                    "training_id": f"TRN-{team[:3].upper()}-{wave}",
                    "team": team,
                    "workflow_id": workflow["workflow_id"],
                    "module": random.choice(["Agent basics", "Workflow scoping", "Review rubric", "Prompt repair"]),
                    "readiness_score": round(readiness, 1),
                    "attendees": random.randint(6, 24),
                    "blocker": random.choice(["None", "Needs examples", "Needs manager sponsor", "Needs policy review"]),
                    "next_action": random.choice(["Run workshop", "Publish playbook", "Schedule review lab", "Create office hours"]),
                }
            )

    return workflow_rows, signals, eval_cases, data_checks, training_rows


def build_analysis(workflows, signals, eval_cases, data_checks, training_rows):
    signal_summary = defaultdict(lambda: {"count": 0, "pain": 0.0, "urgency": 0.0, "clarity": 0.0})
    for row in signals:
        bucket = signal_summary[row["workflow_id"]]
        bucket["count"] += 1
        bucket["pain"] += float(row["pain_score"])
        bucket["urgency"] += float(row["urgency_score"])
        bucket["clarity"] += float(row["requirements_clarity"])

    eval_summary = defaultdict(lambda: {"count": 0, "pass_rate": 0.0, "high_defects": 0})
    for row in eval_cases:
        bucket = eval_summary[row["workflow_id"]]
        bucket["count"] += 1
        bucket["pass_rate"] += float(row["pass_rate"])
        bucket["high_defects"] += 1 if row["defect_severity"] == "High" else 0

    dq_summary = defaultdict(lambda: {"count": 0, "pass_rate": 0.0, "blockers": 0})
    for row in data_checks:
        bucket = dq_summary[row["workflow_id"]]
        bucket["count"] += 1
        bucket["pass_rate"] += float(row["pass_rate"])
        bucket["blockers"] += 1 if row["gate"] == "Pilot blocker" else 0

    training_summary = defaultdict(lambda: {"readiness": 0.0, "count": 0, "attendees": 0})
    for row in training_rows:
        bucket = training_summary[row["workflow_id"]]
        bucket["readiness"] += float(row["readiness_score"])
        bucket["count"] += 1
        bucket["attendees"] += int(row["attendees"])

    priority_rows = []
    workflow_lookup = {row["workflow_id"]: row for row in workflows}
    for row in workflows:
        sid = row["workflow_id"]
        sig = signal_summary[sid]
        ev = eval_summary[sid]
        dq = dq_summary[sid]
        trn = training_summary[sid]
        signal_count = sig["count"]
        avg_pain = sig["pain"] / signal_count
        avg_urgency = sig["urgency"] / signal_count
        avg_clarity = sig["clarity"] / signal_count
        eval_pass = ev["pass_rate"] / ev["count"]
        dq_pass = dq["pass_rate"] / dq["count"]
        training_readiness = trn["readiness"] / trn["count"] if trn["count"] else 68
        value_score = (
            float(row["base_impact"]) * 0.18
            + avg_pain * 3.2
            + avg_urgency * 2.8
            + float(row["automation_fit"]) * 0.16
            + float(row["adoption_pull"]) * 0.13
        )
        risk_penalty = (
            float(row["data_sensitivity"]) * 0.14
            + float(row["process_complexity"]) * 0.12
            + float(row["effort"]) * 0.13
            + ev["high_defects"] * 4.2
            + dq["blockers"] * 6.5
        )
        readiness = eval_pass * 0.38 + dq_pass * 0.32 + training_readiness * 0.18 + avg_clarity * 1.2
        priority_score = clamp(value_score + readiness * 0.25 - risk_penalty, 0, 100)
        if priority_score >= 74 and dq["blockers"] == 0 and ev["high_defects"] <= 1:
            recommendation = "Pilot now"
        elif priority_score >= 66:
            recommendation = "Spec and repair"
        elif avg_urgency >= 7.4:
            recommendation = "Discovery spike"
        else:
            recommendation = "Monitor"
        priority_rows.append(
            {
                "workflow_id": sid,
                "workflow_name": row["workflow_name"],
                "domain": row["domain"],
                "team": row["team"],
                "stakeholder": row["stakeholder"],
                "signal_count": signal_count,
                "avg_pain_score": round(avg_pain, 1),
                "avg_urgency_score": round(avg_urgency, 1),
                "requirements_clarity": round(avg_clarity, 1),
                "automation_fit": row["automation_fit"],
                "data_sensitivity": row["data_sensitivity"],
                "process_complexity": row["process_complexity"],
                "effort": row["effort"],
                "agent_eval_pass_rate": round(eval_pass, 1),
                "data_quality_pass_rate": round(dq_pass, 1),
                "training_readiness": round(training_readiness, 1),
                "priority_score": round(priority_score, 1),
                "recommendation": recommendation,
                "problem": row["problem"],
                "agent_goal": row["agent_goal"],
            }
        )

    priority_rows.sort(key=lambda item: item["priority_score"], reverse=True)
    top = priority_rows[0]
    top_workflow = workflow_lookup[top["workflow_id"]]

    spec_rows = [
        {
            "section": "Problem",
            "owner": top_workflow["stakeholder"],
            "detail": top_workflow["problem"],
            "acceptance_criteria": "A non-technical stakeholder can confirm the workflow, required inputs, output format, and approval gate.",
        },
        {
            "section": "Agent Job",
            "owner": "Product manager",
            "detail": top_workflow["agent_goal"],
            "acceptance_criteria": "Agent output includes confidence, source references, unresolved questions, and next action.",
        },
        {
            "section": "Inputs",
            "owner": top_workflow["team"],
            "detail": top_workflow["source_systems"],
            "acceptance_criteria": "Every input has a named source owner, refresh expectation, and sensitive-field handling rule.",
        },
        {
            "section": "Human Gate",
            "owner": "Workflow reviewer",
            "detail": "Human reviewer approves external-facing language, policy-sensitive decisions, and any low-confidence recommendation.",
            "acceptance_criteria": "No consequential decision leaves the workflow without a reviewer trace.",
        },
        {
            "section": "Jira Handoff",
            "owner": "Engineering and design",
            "detail": "Build a repeatable Cowork folder template, review checklist, sample input pack, and audit log export.",
            "acceptance_criteria": "Delivery team can size setup, test coverage, permissions, and rollout tasks in one planning session.",
        },
    ]

    selected_eval = [row for row in eval_cases if row["workflow_id"] == top["workflow_id"]]
    selected_training = sorted(training_rows, key=lambda row: float(row["readiness_score"]))[:10]
    selected_dq = [row for row in data_checks if row["workflow_id"] == top["workflow_id"]]

    summary = {
        "seed": SEED,
        "workflow_count": len(workflows),
        "signal_count": len(signals),
        "eval_case_count": len(eval_cases),
        "training_plan_count": len(training_rows),
        "top_workflow": top["workflow_name"],
        "top_priority_score": top["priority_score"],
        "pilot_now_count": sum(1 for row in priority_rows if row["recommendation"] == "Pilot now"),
        "avg_eval_pass_rate": round(sum(float(row["agent_eval_pass_rate"]) for row in priority_rows) / len(priority_rows), 1),
        "avg_training_readiness": round(sum(float(row["training_readiness"]) for row in priority_rows) / len(priority_rows), 1),
    }

    app_payload = {
        "summary": summary,
        "priorityQueue": priority_rows,
        "workflowSpec": spec_rows,
        "agentEval": selected_eval,
        "trainingPlan": selected_training,
        "dataQuality": selected_dq,
        "topWorkflow": top,
    }

    return priority_rows, spec_rows, selected_eval, selected_training, selected_dq, summary, app_payload


def write_analysis_docs(summary, top):
    write_text(
        ANALYSIS / "analysis_plan.md",
        f"""
# Analysis Plan

1. Generate deterministic synthetic workflow evidence for identity intelligence AI agent candidates.
2. Aggregate stakeholder signals by workflow to size pain, urgency, and requirements clarity.
3. Score each agent candidate on impact, automation fit, adoption pull, data sensitivity, process complexity, delivery effort, evaluation pass rate, data quality, and training readiness.
4. Convert the highest-ranked workflow into a PRD-ready workflow specification, agent evaluation matrix, data quality gate, and internal training plan.
5. Use the priority queue to decide whether each workflow should pilot now, enter spec repair, run a discovery spike, or stay monitored.
""",
    )

    write_text(
        ANALYSIS / "executive_findings.md",
        f"""
# Executive Findings

## What I Analyzed

I modeled {summary['workflow_count']} identity intelligence AI agent workflow candidates, {summary['signal_count']} stakeholder signals, {summary['eval_case_count']} agent evaluation cases, and {summary['training_plan_count']} internal enablement records.

## Findings

- The top workflow is {summary['top_workflow']} with a priority score of {summary['top_priority_score']}.
- {summary['pilot_now_count']} workflows are ready for a controlled pilot after review gates are confirmed.
- Average agent evaluation pass rate is {summary['avg_eval_pass_rate']} and average training readiness is {summary['avg_training_readiness']}.
- The best artifact story is not automation volume alone. It is showing how discovery, specification, review, and enablement prevent risky agent sprawl.

## Recommendation

Start with the highest-ranked workflow and treat it as a craft example for the rest of the organization. Require a documented input pack, human approval gate, prompt repair log, evaluation matrix, and workshop plan before scaling more internal agents.
""",
    )

    write_text(
        ANALYSIS / "sql_checks.sql",
        """
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
""",
    )

    write_text(
        DATA / "README.md",
        f"""
# Data Sources

All datasets are deterministic synthetic data for a public portfolio artifact. They do not represent real customers, people, identity records, lead lists, fraud signals, investigations, contracts, employees, internal tools, or production company performance.

The generator uses fixed seed `{SEED}`. The data is modeled on common identity intelligence operating structures: identity resolution, fraud and risk reason codes, contact enrichment, lead audience QA, investigations research, data delivery onboarding, compliance exception review, data quality drift, sales discovery, and internal AI agent review.

Files:

- `workflow_candidates.csv`: AI agent workflow candidates with domain, owner, problem, source systems, impact, sensitivity, complexity, automation fit, adoption pull, and effort.
- `discovery_signals.csv`: Stakeholder interviews, support escalations, sales notes, operations retros, training requests, and quality reviews.
- `agent_eval_cases.csv`: Evaluation cases for completeness, grounding, sensitive data handling, workflow accuracy, human handoff clarity, and repeatability.
- `data_quality_checks.csv`: Workflow-level readiness checks for identifiers, freshness, consent and use-case tags.
- `training_plan.csv`: Internal training modules, readiness scores, blockers, and next actions by team.
""",
    )

    write_text(
        ROOT / "data_dictionary.md",
        """
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
""",
    )

    write_text(
        ROOT / "STATUS.md",
        """
# Status

- Project: Identity Intelligence AI Agent Workflow Studio
- GitHub: https://github.com/Saurav-Kanegaonkar/Identity-Intelligence-AI-Agent-Workflow-Studio
- Status: upgraded through the Portfolio Artifact Upgrade Workflow.
- Safe to link as an identity intelligence AI agent product management portfolio artifact after changes are pushed.
- Resume Link Ready: Yes
""",
    )


def write_readme(summary):
    write_text(
        ROOT / "README.md",
        f"""
# Identity Intelligence AI Agent Workflow Studio

An interactive product management portfolio artifact for an identity intelligence and data analytics platform team. The studio shows how a product manager can discover internal AI agent opportunities, convert the best one into a workflow specification, evaluate agent quality, and plan training before scaling adoption.

## What This Project Shows

Identity-data organizations do not need random internal agents. They need repeatable agent workflows with clear inputs, human review gates, quality checks, and training. This artifact demonstrates that product loop:

- Prioritize agent workflows by stakeholder pain, automation fit, adoption pull, data sensitivity, process complexity, effort, evaluation quality, data readiness, and training readiness.
- Translate discovery into a PRD-ready workflow specification with source systems, acceptance criteria, reviewer gates, and delivery handoff.
- Review agent outputs with a test matrix for source grounding, sensitive data handling, workflow accuracy, human handoff clarity, and repeatability.
- Plan internal workshops so teams adopt the agent workflow safely and consistently.

## Screenshots

![Priority cockpit](docs/images/priority-cockpit.png)

Caption: The priority cockpit ranks identity intelligence AI agent opportunities and shows whether each workflow should pilot, enter prompt and spec repair, run discovery, or stay monitored.

![Workflow spec](docs/images/workflow-spec.png)

Caption: The workflow spec surface turns the top-ranked agent into a PRD-ready handoff with problem framing, agent job, input pack, human gate, and Jira-style delivery criteria.

![Evaluation lab](docs/images/evaluation-lab.png)

Caption: The evaluation lab shows agent test cases, pass rates, defect severity, data quality gates, and reviewer notes before the workflow can be expanded.

![Training rollout](docs/images/training-rollout.png)

Caption: The training rollout surface identifies the teams and modules that need workshops, examples, policy review, or office hours before broad adoption.

## Data Strategy

All data is deterministic synthetic data generated for a public portfolio artifact. It does not represent real customers, people, identity records, lead lists, fraud signals, investigations, contracts, employees, internal tools, or production company performance.

The generator uses fixed seed `{summary['seed']}`. The synthetic structure is modeled on common identity intelligence operating patterns: identity resolution, fraud and risk reason codes, contact enrichment, lead audience QA, investigations research, data delivery onboarding, compliance exception review, data quality drift, sales discovery, and internal AI agent review.

The scoring model combines stakeholder signal volume, pain, urgency, requirements clarity, automation fit, adoption pull, data sensitivity, process complexity, delivery effort, agent evaluation pass rate, data quality pass rate, and training readiness.

## Files

- `index.html`: Static app shell with four product artifact surfaces.
- `src/app.js`: Loads the generated app payload and renders the cockpit, workflow spec, evaluation lab, and training rollout.
- `src/styles.css`: Responsive product-studio styling.
- `scripts/score_operating_data.py`: Regenerates synthetic data, analysis outputs, documentation, and app payload.
- `scripts/capture_screenshots.cjs`: Captures README screenshots.
- `data/`: Synthetic source-style datasets.
- `analysis/outputs/`: Ranked workflow queue, PRD spec, evaluation matrix, training plan, summary, and app payload.

## Role Connection

This artifact demonstrates product management for agentic AI work: discovery conversations, cross-functional prioritization, structured workflow specification, hands-on agent review, human approval gates, Jira-ready handoff, and internal training. It is intentionally more than a dashboard because the job is about building and scaling useful AI agent workflows across teams.

## Run Locally

```bash
npm run analyze
npm run start
```

Then open `http://localhost:4173`.

## Scope

This is a static public portfolio artifact with reproducible synthetic data and transparent scoring logic. It does not connect to live identity data, production APIs, Snowflake, cloud storage, CRM systems, support queues, fraud tools, lead platforms, investigation products, AI services, Claude Cowork, Jira, or private company data. It shows how a product manager can structure the evidence, decisions, review gates, and enablement plan for internal AI agent workflows before production implementation.
""",
    )


def main():
    workflows, signals, eval_cases, data_checks, training_rows = build_source_data()
    priority_rows, spec_rows, selected_eval, selected_training, selected_dq, summary, app_payload = build_analysis(
        workflows, signals, eval_cases, data_checks, training_rows
    )

    write_csv(
        DATA / "workflow_candidates.csv",
        workflows,
        [
            "workflow_id",
            "workflow_name",
            "domain",
            "team",
            "stakeholder",
            "problem",
            "agent_goal",
            "source_systems",
            "delivery_surface",
            "base_impact",
            "data_sensitivity",
            "process_complexity",
            "automation_fit",
            "adoption_pull",
            "effort",
        ],
    )
    write_csv(
        DATA / "discovery_signals.csv",
        signals,
        [
            "signal_id",
            "signal_date",
            "workflow_id",
            "signal_type",
            "stakeholder_team",
            "pain_score",
            "urgency_score",
            "requirements_clarity",
            "sample_note",
        ],
    )
    write_csv(
        DATA / "agent_eval_cases.csv",
        eval_cases,
        ["test_id", "workflow_id", "eval_type", "test_prompt", "expected_behavior", "pass_rate", "defect_severity", "review_note"],
    )
    write_csv(DATA / "data_quality_checks.csv", data_checks, ["check_id", "workflow_id", "check_name", "pass_rate", "owner", "gate"])
    write_csv(DATA / "training_plan.csv", training_rows, ["training_id", "team", "workflow_id", "module", "readiness_score", "attendees", "blocker", "next_action"])

    write_csv(
        OUTPUTS / "workflow_priority_queue.csv",
        priority_rows,
        [
            "workflow_id",
            "workflow_name",
            "domain",
            "team",
            "stakeholder",
            "signal_count",
            "avg_pain_score",
            "avg_urgency_score",
            "requirements_clarity",
            "automation_fit",
            "data_sensitivity",
            "process_complexity",
            "effort",
            "agent_eval_pass_rate",
            "data_quality_pass_rate",
            "training_readiness",
            "priority_score",
            "recommendation",
            "problem",
            "agent_goal",
        ],
    )
    write_csv(OUTPUTS / "prd_workflow_spec.csv", spec_rows, ["section", "owner", "detail", "acceptance_criteria"])
    write_csv(OUTPUTS / "agent_evaluation_matrix.csv", selected_eval, ["test_id", "workflow_id", "eval_type", "test_prompt", "expected_behavior", "pass_rate", "defect_severity", "review_note"])
    write_csv(OUTPUTS / "training_rollout_plan.csv", selected_training, ["training_id", "team", "workflow_id", "module", "readiness_score", "attendees", "blocker", "next_action"])
    write_csv(OUTPUTS / "data_quality_gates.csv", selected_dq, ["check_id", "workflow_id", "check_name", "pass_rate", "owner", "gate"])
    write_json(OUTPUTS / "summary.json", summary)
    write_json(OUTPUTS / "app_payload.json", app_payload)

    write_analysis_docs(summary, priority_rows[0])
    write_readme(summary)

    print(f"Generated {len(workflows)} workflows and {len(priority_rows)} priority rows.")
    print(f"Top workflow: {summary['top_workflow']} ({summary['top_priority_score']}).")


if __name__ == "__main__":
    main()
