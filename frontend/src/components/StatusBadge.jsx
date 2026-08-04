import { motion } from "framer-motion";
import { FiCheckCircle, FiClock, FiLoader, FiXCircle } from "react-icons/fi";

const statusConfig = {
  queued: {
    label: "Queued",
    className: "border-warning/40 bg-warning/10 text-warning",
    icon: FiClock
  },
  running: {
    label: "Running",
    className: "border-primary/40 bg-primary/10 text-primary",
    icon: FiLoader
  },
  success: {
    label: "Success",
    className: "border-success/40 bg-success/10 text-success",
    icon: FiCheckCircle
  },
  failed: {
    label: "Failed",
    className: "border-error/40 bg-error/10 text-error",
    icon: FiXCircle
  }
};

export default function StatusBadge({ status }) {
  const config = statusConfig[status] || statusConfig.queued;
  const Icon = config.icon;

  return (
    <motion.span
      initial={{ opacity: 0, x: 10 }}
      animate={{ opacity: 1, x: 0 }}
      className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm font-semibold ${config.className}`}
    >
      <Icon className={`h-4 w-4 ${status === "running" ? "animate-spin" : ""}`} />
      {config.label}
    </motion.span>
  );
}
