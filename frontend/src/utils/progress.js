export const pipelineStages = [
  { key: "checkout", label: "Checkout", tokens: ["checkout", "git clone"] },
  { key: "validate", label: "Dockerfile Validation", tokens: ["validate dockerfile", "source/dockerfile"] },
  { key: "login", label: "Docker Login", tokens: ["docker login", "login"] },
  { key: "build", label: "Build Image", tokens: ["build image", "docker build"] },
  { key: "push", label: "Push Image", tokens: ["push image", "docker push"] },
  { key: "complete", label: "Complete", tokens: ["success:", "finished: success"] }
];

export function getStageStates(status = "queued", logs = "") {
  const normalizedLogs = logs.toLowerCase();

  if (status === "success") {
    return pipelineStages.map((stage) => ({ ...stage, state: "completed" }));
  }

  if (status === "failed") {
    let latestStartedIndex = pipelineStages.findIndex((stage) =>
      stage.tokens.some((token) => normalizedLogs.includes(token))
    );
    pipelineStages.forEach((stage, index) => {
      if (stage.tokens.some((token) => normalizedLogs.includes(token))) {
        latestStartedIndex = index;
      }
    });
    return pipelineStages.map((stage, index) => ({
      ...stage,
      state: index < latestStartedIndex ? "completed" : index === latestStartedIndex ? "failed" : "pending"
    }));
  }

  if (status === "running") {
    let latestStartedIndex = 0;
    pipelineStages.forEach((stage, index) => {
      if (stage.tokens.some((token) => normalizedLogs.includes(token))) {
        latestStartedIndex = index;
      }
    });
    return pipelineStages.map((stage, index) => ({
      ...stage,
      state: index < latestStartedIndex ? "completed" : index === latestStartedIndex ? "running" : "pending"
    }));
  }

  return pipelineStages.map((stage) => ({ ...stage, state: "pending" }));
}
