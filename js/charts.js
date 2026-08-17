/**
 * Dynamic SVG & DOM Chart Visualizer for Composio App Toolkit Research Dashboard
 * Generates lightweight, responsive, dependency-free visualizations derived from JSON data.
 */

window.ChartRenderer = {
  /**
   * Renders stacked horizontal bar chart of Auth Methods by Category
   */
  renderAuthDistribution(containerId, categoryData, totalMetrics) {
    const container = document.getElementById(containerId);
    if (!container || !categoryData) return;

    const authColors = {
      OAuth2: '#ff6b35',
      'API Key': '#0ea5e9',
      Basic: '#f59e0b',
      CLI: '#10b981'
    };

    const oauthTotal = totalMetrics?.oauth2_dominant_count ?? 0;
    const apiKeyTotal = totalMetrics?.api_key_dominant_count ?? 0;
    const basicTotal = totalMetrics?.basic_auth_count ?? 0;
    const cliTotal = totalMetrics?.cli_local_count ?? 0;

    let html = `
      <div style="display: flex; gap: 1rem; margin-bottom: 0.85rem; font-size: 0.78rem; flex-wrap: wrap; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border-subtle, #27272a);">
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: ${authColors.OAuth2};"></span> <strong>OAuth2:</strong> ${oauthTotal} apps</div>
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: ${authColors['API Key']};"></span> <strong>API Key:</strong> ${apiKeyTotal} apps</div>
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: ${authColors.Basic};"></span> <strong>Basic Auth:</strong> ${basicTotal} apps</div>
        <div style="display: flex; align-items: center; gap: 0.35rem;"><span style="width: 10px; height: 10px; border-radius: 3px; background: ${authColors.CLI};"></span> <strong>Local CLI:</strong> ${cliTotal} apps</div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 0.65rem;">
    `;

    categoryData.forEach(cat => {
      const total = cat.total || (cat.OAuth2 + cat['API Key'] + cat.Basic + cat.CLI) || 1;
      const oauthPct = ((cat.OAuth2 || 0) / total) * 100;
      const apiKeyPct = ((cat['API Key'] || 0) / total) * 100;
      const basicPct = ((cat.Basic || 0) / total) * 100;
      const cliPct = ((cat.CLI || 0) / total) * 100;

      html += `
        <div class="chart-row">
          <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 0.25rem; color: #a1a1aa;">
            <span style="font-weight: 500; color: #f4f4f5;">${cat.category}</span>
            <span style="font-family: monospace; font-size: 0.72rem; color: #71717a;">
              ${cat.OAuth2 ? `${cat.OAuth2} OAuth ` : ''}${cat['API Key'] ? `${cat['API Key']} Key ` : ''}${cat.Basic ? `${cat.Basic} Basic ` : ''}${cat.CLI ? `${cat.CLI} CLI` : ''}
            </span>
          </div>
          <div style="display: flex; height: 12px; border-radius: 3px; overflow: hidden; background: #18181b; border: 1px solid #27272a;">
            ${oauthPct > 0 ? `<div style="width: ${oauthPct}%; background: ${authColors.OAuth2};" title="${cat.category}: ${cat.OAuth2} OAuth2 (${oauthPct.toFixed(0)}%)"></div>` : ''}
            ${apiKeyPct > 0 ? `<div style="width: ${apiKeyPct}%; background: ${authColors['API Key']};" title="${cat.category}: ${cat['API Key']} API Key (${apiKeyPct.toFixed(0)}%)"></div>` : ''}
            ${basicPct > 0 ? `<div style="width: ${basicPct}%; background: ${authColors.Basic};" title="${cat.category}: ${cat.Basic} Basic Auth (${basicPct.toFixed(0)}%)"></div>` : ''}
            ${cliPct > 0 ? `<div style="width: ${cliPct}%; background: ${authColors.CLI};" title="${cat.category}: ${cat.CLI} Local CLI (${cliPct.toFixed(0)}%)"></div>` : ''}
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
    if (!container || !gatingData) return;

    let html = `<div style="display: flex; flex-direction: column; gap: 0.65rem;">`;

    gatingData.forEach(cat => {
      const total = (cat.self_serve + cat.gated) || 1;
      const selfPct = ((cat.self_serve || 0) / total) * 100;
      const gatedPct = ((cat.gated || 0) / total) * 100;

      html += `
        <div class="chart-row">
          <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 0.25rem; color: #a1a1aa;">
            <span style="font-weight: 500; color: #f4f4f5;">${cat.category}</span>
            <span style="font-family: monospace; font-size: 0.72rem; color: #71717a;">${cat.self_serve} Self-Serve / ${cat.gated} Gated</span>
          </div>
          <div style="display: flex; height: 12px; border-radius: 3px; overflow: hidden; background: #18181b; border: 1px solid #27272a;">
            <div style="width: ${selfPct}%; background: #10b981;" title="${cat.category}: ${cat.self_serve} Self-Serve (${selfPct.toFixed(0)}%)"></div>
            <div style="width: ${gatedPct}%; background: #f43f5e;" title="${cat.category}: ${cat.gated} Gated (${gatedPct.toFixed(0)}%)"></div>
          </div>
        </div>
      `;
    });

    html += `</div>`;
    container.innerHTML = html;
  }
};
