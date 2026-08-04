import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FiCheckCircle, FiGitBranch, FiLayers } from "react-icons/fi";

import BuildForm from "../components/BuildForm";
import Card from "../components/Card";
import { createBuild } from "../services/api";

const initialForm = {
  repository_url: "",
  image_name: "",
  port: "3000"
};

export default function Dashboard() {
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  function updateField(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!form.repository_url.trim() || !form.image_name.trim() || !form.port.trim()) {
      setError("All fields are required.");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      const response = await createBuild({
        repository_url: form.repository_url,
        image_name: form.image_name,
        port: Number(form.port)
      });
      navigate(`/status/${response.data.build_id}`);
    } catch (err) {
      setError(err.response?.data?.detail?.[0]?.msg || err.response?.data?.detail || err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="grid gap-8 lg:grid-cols-[1fr_360px]">
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}>
        <div className="mb-8">
          <span className="inline-flex rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-semibold uppercase text-blue-200">
            One-click CI pipeline
          </span>
          <h1 className="mt-4 max-w-3xl text-4xl font-semibold text-text sm:text-5xl">
            Build and push Docker images from GitHub.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-muted">
            Trigger a Jenkins pipeline, stream console logs, and get AI-assisted failure
            explanations from one focused DevOps dashboard.
          </p>
        </div>

        <BuildForm
          form={form}
          error={error}
          submitting={submitting}
          onChange={updateField}
          onSubmit={handleSubmit}
        />
      </motion.div>

      <div className="space-y-5">
        <Card className="p-5">
          <div className="flex items-center gap-3">
            <FiGitBranch className="h-6 w-6 text-primary" />
            <h2 className="text-base font-semibold text-text">Pipeline Contract</h2>
          </div>
          <ul className="mt-5 space-y-4 text-sm leading-6 text-muted">
            <li className="flex gap-3">
              <FiCheckCircle className="mt-0.5 h-5 w-5 shrink-0 text-success" />
              Public GitHub repositories with a root Dockerfile.
            </li>
            <li className="flex gap-3">
              <FiCheckCircle className="mt-0.5 h-5 w-5 shrink-0 text-success" />
              Jenkins owns Docker Hub credentials and image publishing.
            </li>
            <li className="flex gap-3">
              <FiCheckCircle className="mt-0.5 h-5 w-5 shrink-0 text-success" />
              Polling keeps the UI simple and reliable for the MVP.
            </li>
          </ul>
        </Card>

        <Card className="p-5">
          <div className="flex items-center gap-3">
            <FiLayers className="h-6 w-6 text-success" />
            <h2 className="text-base font-semibold text-text">Build Flow</h2>
          </div>
          <div className="mt-5 grid gap-3 text-sm text-muted">
            {["Checkout", "Validate Dockerfile", "Docker Login", "Build Image", "Push Image"].map((item, index) => (
              <div key={item} className="flex items-center gap-3 rounded-xl border border-border bg-white/[0.03] px-3 py-2.5">
                <span className="grid h-6 w-6 place-items-center rounded-full bg-primary/15 text-xs font-semibold text-primary">
                  {index + 1}
                </span>
                {item}
              </div>
            ))}
          </div>
        </Card>
      </div>
    </section>
  );
}
