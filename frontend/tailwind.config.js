/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#0B1220",
        panel: "#111827",
        primary: "#3B82F6",
        success: "#22C55E",
        error: "#EF4444",
        warning: "#F59E0B",
        border: "#1F2937",
        text: "#F9FAFB",
        muted: "#9CA3AF"
      },
      boxShadow: {
        glow: "0 18px 60px rgba(59, 130, 246, 0.18)",
        card: "0 20px 60px rgba(0, 0, 0, 0.35)"
      }
    }
  },
  plugins: []
};
