import { FiCheckCircle, FiExternalLink } from "react-icons/fi";

import Card from "./Card";
import CopyButton from "./CopyButton";

function CommandBlock({ title, command }) {
  return (
    <div className="overflow-hidden rounded-xl border border-border bg-canvas">
      <div className="flex items-center justify-between gap-3 border-b border-border px-4 py-3">
        <span className="text-sm font-medium text-muted">{title}</span>
        <CopyButton value={command || ""} />
      </div>
      <pre className="overflow-auto p-4 font-mono text-sm leading-6 text-emerald-200">{command}</pre>
    </div>
  );
}

export default function SuccessCard({ pullCommand, runCommand, previewUrl, previewStatus }) {
  return (
    <Card className="p-5 sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <FiCheckCircle className="h-8 w-8 text-success" />
          <div>
            <h2 className="text-xl font-semibold text-text">✅ Image Successfully Pushed</h2>
            <p className="mt-1 text-sm text-muted">Use these commands to pull and run the latest image.</p>
          </div>
        </div>
        {previewUrl && (
          <a
            href={previewUrl}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-xl bg-success px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:brightness-110"
          >
            <FiExternalLink className="h-4 w-4" />
            Open App
          </a>
        )}
      </div>
      {previewStatus && (
        <div className="mt-5 rounded-xl border border-primary/30 bg-primary/10 px-4 py-3 text-sm text-blue-100">
          Kubernetes preview status: {previewStatus}
        </div>
      )}
      <div className="mt-5 grid gap-4">
        <CommandBlock title="Docker Pull Command" command={pullCommand} />
        <CommandBlock title="Docker Run Command" command={runCommand} />
      </div>
    </Card>
  );
}
