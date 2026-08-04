import { useState } from "react";
import { FiCheck, FiCopy } from "react-icons/fi";

export default function CopyButton({ value, label = "Copy", copiedLabel = "Copied" }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    if (!value) return;
    await navigator.clipboard.writeText(value);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 2000);
  }

  return (
    <button
      type="button"
      onClick={copy}
      disabled={!value}
      className="inline-flex items-center gap-2 rounded-lg border border-border/90 bg-white/5 px-3 py-1.5 text-xs font-medium text-text transition hover:border-primary/70 hover:bg-primary/15 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {copied ? <FiCheck className="h-4 w-4 text-success" /> : <FiCopy className="h-4 w-4" />}
      {copied ? copiedLabel : label}
    </button>
  );
}
