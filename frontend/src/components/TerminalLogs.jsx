import CopyButton from "./CopyButton";

function highlightLogs(logs) {
  if (!logs) return null;
  return logs.split("\n").map((line, index) => {
    const lower = line.toLowerCase();
    let color = "text-slate-300";
    if (lower.includes("error") || lower.includes("failed") || lower.includes("failure")) color = "text-red-300";
    if (lower.includes("success") || lower.includes("pushed")) color = "text-emerald-300";
    if (lower.includes("warning") || lower.includes("deprecated")) color = "text-amber-300";
    if (lower.includes("[pipeline]") || lower.includes("docker")) color = "text-cyan-200";

    return (
      <span key={`${index}-${line.slice(0, 12)}`} className={color}>
        {line || " "}
        {"\n"}
      </span>
    );
  });
}

export default function TerminalLogs({ logs, title = "Jenkins Console Logs" }) {
  return (
    <div className="overflow-hidden rounded-xl border border-border bg-panel/80 shadow-card">
      <div className="flex items-center justify-between gap-3 border-b border-border bg-white/[0.03] px-4 py-3">
        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-error" />
          <span className="h-3 w-3 rounded-full bg-warning" />
          <span className="h-3 w-3 rounded-full bg-success" />
          <span className="ml-2 text-sm font-medium text-muted">{title}</span>
        </div>
        <CopyButton value={logs || ""} label="Copy" copiedLabel="Copied!" />
      </div>
      <pre className="min-h-[380px] max-h-[560px] overflow-auto bg-black px-4 py-4 font-mono text-sm leading-6">
        {logs ? highlightLogs(logs) : <span className="text-muted">Waiting for Jenkins logs...</span>}
      </pre>
    </div>
  );
}
