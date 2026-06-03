const money = new Intl.NumberFormat("en-US");

const byId = (id) => document.getElementById(id);

function scoreClass(value) {
  if (value >= 82) return "good";
  if (value >= 70) return "warn";
  return "risk";
}

function decisionClass(value) {
  if (value === "Pilot now") return "good";
  if (value === "Spec and repair") return "warn";
  if (value === "Discovery spike") return "info";
  return "muted";
}

function metric(label, value, helper) {
  return `
    <article class="metric">
      <span>${label}</span>
      <strong>${value}</strong>
      <small>${helper}</small>
    </article>
  `;
}

function renderSummary(payload) {
  const summary = payload.summary;
  byId("top-workflow").textContent = summary.top_workflow;
  byId("top-score").textContent = `${summary.top_priority_score} priority score`;
  byId("summary-metrics").innerHTML = [
    metric("Workflow candidates", money.format(summary.workflow_count), `${money.format(summary.signal_count)} discovery signals`),
    metric("Agent tests", money.format(summary.eval_case_count), `${summary.avg_eval_pass_rate}% avg pass rate`),
    metric("Pilot-ready", money.format(summary.pilot_now_count), "controlled workflow pilots"),
    metric("Training readiness", `${summary.avg_training_readiness}%`, "enablement signal"),
  ].join("");
}

function renderPriorityTable(rows) {
  byId("priority-table").innerHTML = rows
    .map(
      (row) => `
      <tr>
        <td>
          <b>${row.workflow_name}</b>
          <span>${row.team} owner, ${row.signal_count} signals</span>
        </td>
        <td>${row.domain}</td>
        <td><strong class="${scoreClass(row.priority_score)}">${row.priority_score}</strong></td>
        <td>${row.agent_eval_pass_rate}%</td>
        <td>${row.data_quality_pass_rate}%</td>
        <td>${row.training_readiness}%</td>
        <td><span class="pill ${decisionClass(row.recommendation)}">${row.recommendation}</span></td>
      </tr>
    `
    )
    .join("");
}

function renderSpec(payload) {
  const top = payload.topWorkflow;
  byId("spec-context").textContent = `${top.workflow_name}: ${top.problem}`;
  byId("spec-grid").innerHTML = payload.workflowSpec
    .map(
      (item, index) => `
      <article class="spec-card">
        <span>${String(index + 1).padStart(2, "0")}</span>
        <h3>${item.section}</h3>
        <p>${item.detail}</p>
        <footer>
          <b>${item.owner}</b>
          <small>${item.acceptance_criteria}</small>
        </footer>
      </article>
    `
    )
    .join("");
}

function renderEval(payload) {
  byId("eval-list").innerHTML = payload.agentEval
    .map(
      (item) => `
      <article class="test-row">
        <div>
          <span>${item.test_id}</span>
          <h3>${item.eval_type}</h3>
          <p>${item.expected_behavior}</p>
        </div>
        <aside>
          <strong class="${scoreClass(item.pass_rate)}">${item.pass_rate}%</strong>
          <small>${item.defect_severity}</small>
        </aside>
      </article>
    `
    )
    .join("");

  byId("gate-list").innerHTML = `
    <h3>Data Quality Gates</h3>
    ${payload.dataQuality
      .map(
        (item) => `
        <div class="gate-row">
          <span>${item.check_name}</span>
          <b class="${scoreClass(item.pass_rate)}">${item.pass_rate}%</b>
          <small>${item.gate}</small>
        </div>
      `
      )
      .join("")}
  `;
}

function renderTraining(rows) {
  byId("training-board").innerHTML = rows
    .map(
      (row) => `
      <article class="training-card">
        <header>
          <span>${row.team}</span>
          <strong class="${scoreClass(row.readiness_score)}">${row.readiness_score}%</strong>
        </header>
        <h3>${row.module}</h3>
        <p>${row.blocker}</p>
        <footer>
          <small>${row.attendees} attendees</small>
          <b>${row.next_action}</b>
        </footer>
      </article>
    `
    )
    .join("");
}

function bindTabs() {
  document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => {
      const view = button.dataset.view;
      document.querySelectorAll(".tab").forEach((item) => item.classList.toggle("is-active", item === button));
      document.querySelectorAll(".view").forEach((panel) => panel.classList.toggle("is-active", panel.dataset.panel === view));
    });
  });
}

async function boot() {
  bindTabs();
  const response = await fetch("analysis/outputs/app_payload.json");
  const payload = await response.json();
  renderSummary(payload);
  renderPriorityTable(payload.priorityQueue);
  renderSpec(payload);
  renderEval(payload);
  renderTraining(payload.trainingPlan);
}

boot().catch((error) => {
  document.body.innerHTML = `<main class="shell"><p>Unable to load artifact payload: ${error.message}</p></main>`;
});
