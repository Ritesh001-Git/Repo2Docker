import { FiAlertTriangle, FiHelpCircle, FiTool } from "react-icons/fi";

import Card from "./Card";

const sections = [
  { title: "What happened", icon: FiAlertTriangle, className: "border-error/40 bg-error/10 text-red-100" },
  { title: "Why it happened", icon: FiHelpCircle, className: "border-warning/40 bg-warning/10 text-amber-100" },
  { title: "How to fix it", icon: FiTool, className: "border-primary/40 bg-primary/10 text-blue-100" }
];

function extractSection(text, title, nextTitle) {
  const start = text.toLowerCase().indexOf(title.toLowerCase());
  if (start === -1) return "";
  const contentStart = start + title.length;
  const end = nextTitle ? text.toLowerCase().indexOf(nextTitle.toLowerCase(), contentStart) : -1;
  return text.slice(contentStart, end === -1 ? undefined : end).replace(/^[:\s*-]+/, "").trim();
}

export default function AIExplanationCard({ explanation }) {
  if (!explanation) return null;

  const parsed = sections.map((section, index) => ({
    ...section,
    content:
      extractSection(explanation, section.title, sections[index + 1]?.title) ||
      (index === 0 ? explanation : "")
  }));

  return (
    <Card className="p-5 sm:p-6">
      <h2 className="text-xl font-semibold text-text">🤖 AI Explanation</h2>
      <div className="mt-5 grid gap-4">
        {parsed.map((section) => {
          const Icon = section.icon;
          return (
            <div key={section.title} className={`rounded-xl border p-4 ${section.className}`}>
              <div className="flex items-center gap-2 text-sm font-semibold">
                <Icon className="h-5 w-5" />
                {section.title}
              </div>
              <div className="mt-3 whitespace-pre-wrap text-sm leading-6 text-current/90">
                {section.content || "Gemini did not provide a separate section for this item."}
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
