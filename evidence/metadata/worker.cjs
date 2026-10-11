
const fs = require('node:fs');
const task = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const output = process.argv[3];
const trace = [];
const nativeFetch = globalThis.fetch;
globalThis.fetch = async (input, options = {}) => {
  const url = typeof input === 'string' ? input : (input.url || String(input));
  if (/\/tile\//i.test(url)) throw new Error('Imagery tile request blocked: metadata-only task');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 15000);
  const record = {url, started_utc:new Date().toISOString()};
  trace.push(record);
  try {
    const response = await nativeFetch(input, {...options, signal:controller.signal});
    record.http_status = response.status;
    const body = await response.clone().text();
    if (body.length <= 4000000) {
      try { record.body = JSON.parse(body); } catch { record.body_excerpt = body.slice(0,1000); }
    } else { record.note = 'Response exceeds trace size limit'; }
    if (!response.ok) throw new Error('HTTP '+response.status);
    return response;
  } catch (e) { record.error = String(e); throw e; }
  finally { clearTimeout(timer); }
};
(async () => {
  let result;
  try {
    const imported = await import('@esri/wayback-core');
    const api = imported.getMetadata ? imported : imported.default;
    if (task.config) api.setCustomWaybackConfig({waybackConfigData:task.config});
    const data = task.mode === 'catalogue'
      ? await api.getWaybackItems()
      : await api.getMetadata(task.point, task.zoom, task.releaseNumber);
    result = {ok:true, data:data ?? null};
  } catch (e) { result = {ok:false,error:String(e)}; }
  result.trace = trace;
  fs.writeFileSync(output, JSON.stringify(result,null,2));
  process.exit(result.ok ? 0 : 1);
})();
