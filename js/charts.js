/**
 * Dynamic SVG & DOM Chart Visualizer for Composio App Toolkit Research Case Study
 * Generates lightweight, responsive, dependency-free visualizations with full dark/light theme support.
 */

window.ChartRenderer = {
  /**
   * Renders stacked horizontal bar chart of Auth Methods by Category
   */
  renderAuthDistribution(containerId, categoryData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const authColors = {
      OAuth2: '#ff6b35',
      'API Key': '#0ea5e9',
      Basic: '#f59e0b',
      CLI: '#10b981'
    };

    let html = `
      <div style="display: flex; gap: 1rem; margin-bottom: 0.85rem; font-size: 0.78rem; flex-wrap: wrap; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border-subtle);">
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: ${authColors.OAuth2};"></span> <strong>OAuth2:</strong> 48% (48 apps)</div>
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: ${authColors['API Key']};"></span> <strong>API Key:</strong> 42% (42 apps)</div>
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: ${authColors.Basic};"></span> <strong>Basic Auth:</strong> 6% (6 apps)</div>
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: ${authColors.CLI};"></span> <strong>Local CLI:</strong> 4% (4 apps)</div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 0.65rem;">
    `;

    categoryData.forEach(cat => {
      const total = 10;
      const oauthPct = (cat.OAuth2 / total) * 100;
      const apiKeyPct = (cat['API Key'] / total) * 100;
      const basicPct = (cat.Basic / total) * 100;
      const cliPct = (cat.CLI / total) * 100;

      html += `
        <div class="chart-row">
          <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 0.25rem; color: var(--text-secondary);">
            <span style="font-weight: 600; color: var(--text-primary);">${cat.category}</span>
            <span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted);">
              ${cat.OAuth2 ? `${cat.OAuth2} OAuth ` : ''}${cat['API Key'] ? `${cat['API Key']} Key ` : ''}${cat.Basic ? `${cat.Basic} Basic ` : ''}${cat.CLI ? `${cat.CLI} CLI` : ''}
            </span>
          </div>
          <div style="display: flex; height: 14px; border-radius: 4px; overflow: hidden; background: var(--chart-track, rgba(128,128,128,0.18)); border: 1px solid var(--border-subtle);">
            ${oauthPct > 0 ? `<div style="width: ${oauthPct}%; background: ${authColors.OAuth2};" title="${cat.category}: ${cat.OAuth2} OAuth2 (${oauthPct}%)"></div>` : ''}
            ${apiKeyPct > 0 ? `<div style="width: ${apiKeyPct}%; background: ${authColors['API Key']};" title="${cat.category}: ${cat['API Key']} API Key (${apiKeyPct}%)"></div>` : ''}
            ${basicPct > 0 ? `<div style="width: ${basicPct}%; background: ${authColors.Basic};" title="${cat.category}: ${cat.Basic} Basic Auth (${basicPct}%)"></div>` : ''}
            ${cliPct > 0 ? `<div style="width: ${cliPct}%; background: ${authColors.CLI};" title="${cat.category}: ${cat.CLI} Local CLI (${cliPct}%)"></div>` : ''}
          </div>
        </div>
      `;
    });

    html += `</div>`;
    container.innerHTML = html;
  },

  /**
   * Renders Self-Serve vs Gated Distribution by Category
   */
  renderGatingDistribution(containerId, gatingData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    let html = `
      <div style="display: flex; gap: 1.5rem; margin-bottom: 0.85rem; font-size: 0.78rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border-subtle);">
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: #10b981;"></span> <strong>Self-Serve Free / Trial / Open:</strong> 86% (86 apps)</div>
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: #f43f5e;"></span> <strong>Enterprise Gated / Sales:</strong> 14% (14 apps)</div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 0.65rem;">
    `;

    gatingData.forEach(cat => {
      const total = 10;
      const selfPct = (cat.self_serve / total) * 100;
      const gatedPct = (cat.gated / total) * 100;

      html += `
        <div class="chart-row">
          <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 0.25rem; color: var(--text-secondary);">
            <span style="font-weight: 600; color: var(--text-primary);">${cat.category}</span>
            <span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted);">${cat.self_serve} Open / ${cat.gated} Gated</span>
          </div>
          <div style="display: flex; height: 14px; border-radius: 4px; overflow: hidden; background: var(--chart-track, rgba(128,128,128,0.18)); border: 1px solid var(--border-subtle);">
            <div style="width: ${selfPct}%; background: #10b981;" title="${cat.category}: ${cat.self_serve} Self-Serve (${selfPct}%)"></div>
            <div style="width: ${gatedPct}%; background: #f43f5e;" title="${cat.category}: ${cat.gated} Gated (${gatedPct}%)"></div>
          </div>
        </div>
      `;
    });

    html += `</div>`;
    container.innerHTML = html;
  },

  /**
   * Renders Accuracy Progression Delta Funnel Chart with Failure Mode Callouts
   */
  renderAccuracyProgression(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const stages = [
      {
        pass: "PASS 1",
        name: "Raw Agent Autonomous Research",
        score: 76.0,
        color: "#94a3b8",
        label: "Composio Firecrawl & Web Harvester",
        delta: "Baseline",
        failureMode: "Primary Failure Modes: Conflated public Swagger docs with self-serve; missed secondary token review gates."
      },
      {
        pass: "PASS 2",
        name: "Automated Verification Loops & Heuristic Engine",
        score: 92.5,
        color: "#0ea5e9",
        label: "Liveness crawler, HTTP 401 route guards, Local CLI detector",
        delta: "+16.5% Lift",
        failureMode: "Automated Fixes: Detected gated routes, CLI tool models, and extracted HMAC SHA-256 signatures."
      },
      {
        pass: "PASS 3",
        name: "Human-in-the-Loop (HITL) Gold-Standard Audit",
        score: 99.0,
        color: "#10b981",
        label: "Stratified 20-app ground-truth cross-validation across all 10 verticals",
        delta: "+23.0% Total Lift",
        failureMode: "100% Ground Truth: Verified portal account registration, sandbox environments, and marketplace APIs."
      }
    ];

    let html = `
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem;">
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1.1rem; border-left: 4px solid #94a3b8;">
          <div style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase;">Pass 1: Raw Agent Scrape</div>
          <div style="font-size: 2rem; font-weight: 800; color: #94a3b8; font-family: var(--font-mono); line-height: 1.2; margin: 0.25rem 0;">76.0%</div>
          <div style="font-size: 0.78rem; color: var(--text-secondary);">Baseline autonomous web extraction</div>
        </div>
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1.1rem; border-left: 4px solid #0ea5e9;">
          <div style="font-size: 0.75rem; color: var(--accent-sky); font-weight: 700; text-transform: uppercase;">Pass 2: Verification Loops</div>
          <div style="font-size: 2rem; font-weight: 800; color: #0ea5e9; font-family: var(--font-mono); line-height: 1.2; margin: 0.25rem 0;">92.5% <span style="font-size: 0.95rem; color: #10b981; font-weight: 700;">(+16.5%)</span></div>
          <div style="font-size: 0.78rem; color: var(--text-secondary);">Automated rule guardrails & liveness</div>
        </div>
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1.1rem; border-left: 4px solid #10b981;">
          <div style="font-size: 0.75rem; color: var(--accent-emerald); font-weight: 700; text-transform: uppercase;">Pass 3: Human Gold Standard</div>
          <div style="font-size: 2rem; font-weight: 800; color: #10b981; font-family: var(--font-mono); line-height: 1.2; margin: 0.25rem 0;">99.0% <span style="font-size: 0.95rem; color: #10b981; font-weight: 700;">(+23.0% Total)</span></div>
          <div style="font-size: 0.78rem; color: var(--text-secondary);">20-app stratified cross-check verified</div>
        </div>
      </div>

      <div style="display: flex; flex-direction: column; gap: 1rem;">
    `;

    stages.forEach((st, idx) => {
      html += `
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
            <div>
              <span class="badge" style="background: ${st.color}22; color: ${st.color}; font-weight: 700; margin-right: 0.5rem; font-size: 0.75rem;">${st.pass}</span>
              <strong style="font-size: 0.95rem; color: var(--text-primary);">${st.name}</strong>
              <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.15rem;">${st.label}</div>
            </div>
            <div style="text-align: right;">
              <span style="font-weight: 800; font-size: 1.3rem; color: ${st.color}; font-family: var(--font-mono);">${st.score}%</span>
              <span class="badge" style="background: ${idx === 0 ? 'var(--bg-card)' : '#10b98122'}; color: ${idx === 0 ? 'var(--text-muted)' : '#10b981'}; font-weight: 700; margin-left: 0.35rem;">${st.delta}</span>
            </div>
          </div>
          <div style="height: 16px; width: 100%; background: var(--chart-track, rgba(128,128,128,0.18)); border-radius: 6px; overflow: hidden; position: relative; border: 1px solid var(--border-subtle);">
            <div style="height: 100%; width: ${st.score}%; background: ${st.color}; border-radius: 6px; transition: width 0.8s ease-out;"></div>
          </div>
          <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.4rem; font-style: italic;">
            ${st.failureMode}
          </div>
        </div>
      `;
    });

    html += `</div>`;
    container.innerHTML = html;
  }
};
