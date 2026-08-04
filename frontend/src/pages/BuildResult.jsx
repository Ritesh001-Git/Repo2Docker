import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { FiArrowLeft } from "react-icons/fi";

import AIExplanationCard from "../components/AIExplanationCard";
import LogsCard from "../components/LogsCard";
import ProgressCard from "../components/ProgressCard";
import StatusCard from "../components/StatusCard";
import SuccessCard from "../components/SuccessCard";
import { getLogs, getStatus } from "../services/api";

export default function BuildResult() {
  const { buildId } = useParams();
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadResult() {
      try {
        const [statusResponse, logsResponse] = await Promise.all([
          getStatus(buildId),
          getLogs(buildId)
        ]);
        setStatus(statusResponse.data);
        setResult(logsResponse.data);
      } catch (err) {
        setError(err.response?.data?.detail || err.message);
      }
    }

    loadResult();
  }, [buildId]);

  return (
    <section className="space-y-6">
      <StatusCard status={status?.status || result?.status || "queued"} buildId={buildId} />

      {error && (
        <div className="rounded-xl border border-error/40 bg-error/10 px-4 py-3 text-sm text-red-200">
          {error}
        </div>
      )}

      <ProgressCard status={status?.status || result?.status || "queued"} logs={result?.logs || ""} />

      {result?.status === "success" && (
        <SuccessCard pullCommand={result.pull_command} runCommand={result.run_command} />
      )}

      {result?.status === "failed" && <AIExplanationCard explanation={result.gemini_explanation} />}

      {result && <LogsCard logs={result.logs} />}

      <Link to="/" className="inline-flex items-center gap-2 text-sm font-medium text-primary hover:text-blue-300">
        <FiArrowLeft className="h-4 w-4" />
        Start another build
      </Link>
    </section>
  );
}
