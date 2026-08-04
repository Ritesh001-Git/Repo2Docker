import { FiActivity, FiCheckCircle, FiClock, FiXCircle } from "react-icons/fi";

import Card from "./Card";
import Spinner from "./Spinner";
import StatusBadge from "./StatusBadge";

const statusMeta = {
  queued: { title: "Waiting in queue", icon: FiClock, color: "text-warning" },
  running: { title: "Building Docker Image...", icon: FiActivity, color: "text-primary" },
  success: { title: "Image build completed", icon: FiCheckCircle, color: "text-success" },
  failed: { title: "Build failed", icon: FiXCircle, color: "text-error" }
};

export default function StatusCard({ status = "queued", buildId }) {
  const meta = statusMeta[status] || statusMeta.queued;
  const Icon = meta.icon;

  return (
    <Card className="p-5 sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase text-muted">Current Status</p>
          <div className="mt-3 flex items-center gap-3">
            {status === "running" ? <Spinner className="h-8 w-8" /> : <Icon className={`h-8 w-8 ${meta.color}`} />}
            <div>
              <h1 className="text-2xl font-semibold text-text">{meta.title}</h1>
              <p className="mt-1 text-sm text-muted">Build #{buildId}</p>
            </div>
          </div>
        </div>
        <StatusBadge status={status} />
      </div>
    </Card>
  );
}
