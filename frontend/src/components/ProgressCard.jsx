import { motion } from "framer-motion";
import { FiCheck, FiCircle, FiLoader, FiX } from "react-icons/fi";

import Card from "./Card";
import { getStageStates } from "../utils/progress";

const stateStyles = {
  pending: "border-border bg-white/5 text-muted",
  running: "border-primary/60 bg-primary/15 text-primary",
  completed: "border-success/60 bg-success/15 text-success",
  failed: "border-error/60 bg-error/15 text-error"
};

const stateIcons = {
  pending: FiCircle,
  running: FiLoader,
  completed: FiCheck,
  failed: FiX
};

export default function ProgressCard({ status, logs }) {
  const stages = getStageStates(status, logs);
  const completed = stages.filter((stage) => stage.state === "completed").length;
  const progress = status === "failed" ? 100 : Math.round((completed / stages.length) * 100);

  return (
    <Card className="p-5 sm:p-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-text">Pipeline Progress</h2>
          <p className="mt-1 text-sm text-muted">Jenkins stages inferred from status and logs</p>
        </div>
        <span className="text-sm font-medium text-muted">{progress}%</span>
      </div>

      <div className="mt-5 h-2 overflow-hidden rounded-full bg-canvas">
        <motion.div
          className={`h-full rounded-full ${status === "failed" ? "bg-error" : "bg-gradient-to-r from-primary to-success"}`}
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.45 }}
        />
      </div>

      <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {stages.map((stage) => {
          const Icon = stateIcons[stage.state];
          return (
            <motion.div
              key={stage.key}
              whileHover={{ scale: 1.02 }}
              className={`flex items-center gap-3 rounded-xl border px-3 py-3 ${stateStyles[stage.state]}`}
            >
              <Icon className={`h-5 w-5 shrink-0 ${stage.state === "running" ? "animate-spin" : ""}`} />
              <span className="min-w-0 text-sm font-medium">{stage.label}</span>
            </motion.div>
          );
        })}
      </div>
    </Card>
  );
}
