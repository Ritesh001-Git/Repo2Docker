import { motion } from "framer-motion";
import { FiArrowRight, FiGithub, FiHash, FiPackage } from "react-icons/fi";

import Card from "./Card";
import Spinner from "./Spinner";

const fields = [
  {
    name: "repository_url",
    label: "GitHub Repository URL",
    placeholder: "https://github.com/user/project",
    type: "url",
    icon: FiGithub
  },
  {
    name: "image_name",
    label: "Docker Image Name",
    placeholder: "my-app",
    type: "text",
    icon: FiPackage
  },
  {
    name: "port",
    label: "Application Port",
    placeholder: "3000",
    type: "number",
    icon: FiHash
  }
];

export default function BuildForm({ form, error, submitting, onChange, onSubmit }) {
  return (
    <Card className="p-5 sm:p-6">
      <form onSubmit={onSubmit} className="space-y-5">
        {fields.map((field) => {
          const Icon = field.icon;
          return (
            <label key={field.name} className="block">
              <span className="text-sm font-medium text-muted">{field.label}</span>
              <span className="mt-2 flex items-center gap-3 rounded-xl border border-border bg-canvas/70 px-3 py-3 transition focus-within:border-primary/70 focus-within:ring-4 focus-within:ring-primary/10">
                <Icon className="h-5 w-5 shrink-0 text-muted" />
                <input
                  name={field.name}
                  value={form[field.name]}
                  onChange={onChange}
                  disabled={submitting}
                  required
                  min={field.type === "number" ? "1" : undefined}
                  max={field.type === "number" ? "65535" : undefined}
                  type={field.type}
                  placeholder={field.placeholder}
                  className="min-w-0 flex-1 bg-transparent text-sm text-text outline-none placeholder:text-muted/60 disabled:cursor-not-allowed"
                />
              </span>
            </label>
          );
        })}

        {error && (
          <div className="rounded-xl border border-error/40 bg-error/10 px-4 py-3 text-sm text-red-200">
            {error}
          </div>
        )}

        {submitting && (
          <div className="space-y-3 rounded-xl border border-primary/30 bg-primary/10 p-4">
            <div className="flex items-center gap-3 text-sm font-medium text-text">
              <Spinner />
              Building Docker Image...
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-canvas">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-primary via-cyan-400 to-success"
                initial={{ x: "-100%" }}
                animate={{ x: "100%" }}
                transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
              />
            </div>
          </div>
        )}

        <motion.button
          whileHover={{ scale: submitting ? 1 : 1.01 }}
          whileTap={{ scale: submitting ? 1 : 0.99 }}
          type="submit"
          disabled={submitting}
          className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-cyan-500 px-4 py-3 font-semibold text-white shadow-glow transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {submitting ? <Spinner className="h-4 w-4" /> : <FiArrowRight className="h-5 w-5" />}
          {submitting ? "Starting build..." : "Build and Push Image"}
        </motion.button>
      </form>
    </Card>
  );
}
