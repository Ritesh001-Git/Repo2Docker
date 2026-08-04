import { FiCheckCircle } from "react-icons/fi";

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

export default function SuccessCard({ pullCommand, runCommand }) {
  return (
    <Card className="p-5 sm:p-6">
      <div className="flex items-center gap-3">
        <FiCheckCircle className="h-8 w-8 text-success" />
        <div>
          <h2 className="text-xl font-semibold text-text">✅ Image Successfully Pushed</h2>
          <p className="mt-1 text-sm text-muted">Use these commands to pull and run the latest image.</p>
        </div>
      </div>
      <div className="mt-5 grid gap-4">
        <CommandBlock title="Docker Pull Command" command={pullCommand} />
        <CommandBlock title="Docker Run Command" command={runCommand} />
      </div>
    </Card>
  );
}
