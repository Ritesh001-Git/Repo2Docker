import { Outlet } from "react-router-dom";

import Navbar from "./Navbar";

export default function AppShell() {
  return (
    <div className="min-h-screen bg-transparent">
      <Navbar />
      <main className="mx-auto max-w-[1100px] px-4 py-8 sm:py-10">
        <Outlet />
      </main>
    </div>
  );
}
