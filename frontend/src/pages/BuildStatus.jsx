import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { FiArrowLeft } from "react-icons/fi";

import LogsCard from "../components/LogsCard";
import ProgressCard from "../components/ProgressCard";
import StatusCard from "../components/StatusCard";
import { getLogs, getStatus } from "../services/api";

export default function BuildStatus() {
  const { buildId } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState(null);
  const [logs, setLogs] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    async function poll() {
      try {
        const [statusResponse, logsResponse] = await Promise.all([
          getStatus(buildId),
          getLogs(buildId)
        ]);

        if (!active) return;
        setStatus(statusResponse.data);
        setLogs(logsResponse.data.logs || "");

        if (["success", "failed"].includes(statusResponse.data.status)) {
          navigate(`/result/${buildId}`);
        }
      } catch (err) {
        if (active) setError(err.response?.data?.detail || err.message);
      }
    }

    poll();
    const timer = window.setInterval(poll, 4000);
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [buildId, navigate]);

  return (
    <section className="space-y-6">
      <StatusCard status={status?.status || "queued"} buildId={buildId} />

      {error && (
        <div className="rounded-xl border border-error/40 bg-error/10 px-4 py-3 text-sm text-red-200">
          {error}
        </div>
      )}

      <ProgressCard status={status?.status || "queued"} logs={logs} />
      <LogsCard logs={logs} />

      <Link to="/" className="inline-flex items-center gap-2 text-sm font-medium text-primary hover:text-blue-300">
        <FiArrowLeft className="h-4 w-4" />
        Start another build
      </Link>
    </section>
  );
}
