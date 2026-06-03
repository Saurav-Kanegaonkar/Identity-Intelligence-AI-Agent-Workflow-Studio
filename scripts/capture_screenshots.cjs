const path = require("path");
const { chromium } = require("../../CRM-Audience-Segmentation-QA-Console/node_modules/playwright");

const root = path.resolve(__dirname, "..");
const baseUrl = process.env.APP_URL || "http://localhost:4173";
const imageDir = path.join(root, "docs", "images");

async function capture(page, view, fileName) {
  await page.click(`[data-view="${view}"]`);
  await page.waitForTimeout(350);
  await page.screenshot({
    path: path.join(imageDir, fileName),
    fullPage: true,
  });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  await page.goto(baseUrl, { waitUntil: "networkidle" });
  await capture(page, "cockpit", "priority-cockpit.png");
  await capture(page, "spec", "workflow-spec.png");
  await capture(page, "eval", "evaluation-lab.png");
  await capture(page, "training", "training-rollout.png");
  await browser.close();
  console.log("Captured identity intelligence AI agent workflow studio screenshots.");
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
