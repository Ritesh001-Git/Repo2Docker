import { Link } from "react-router-dom";
import { FiBox } from "react-icons/fi";
import { motion } from "framer-motion";

export default function Navbar() {
  return (
    <header className="border-b border-border/80 bg-canvas/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-[1100px] items-center justify-between gap-4 px-4 py-5">
        <Link to="/" className="flex min-w-0 items-center gap-3">
          <motion.span
            whileHover={{ scale: 1.06 }}
            className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-gradient-to-br from-primary to-cyan-400 shadow-glow"
          >
            <FiBox className="h-6 w-6 text-white" />
          </motion.span>
          <span className="min-w-0">
            <span className="block text-lg font-semibold text-text">Repo2Docker</span>
            <span className="block truncate text-sm text-muted">Build Docker Images from GitHub</span>
          </span>
        </Link>
        <span className="hidden rounded-full border border-border bg-white/5 px-3 py-1 text-xs font-medium text-muted sm:inline-flex">
          Jenkins powered
        </span>
      </div>
    </header>
  );
}
