import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import AppShell from "./components/AppShell";
import Dashboard from "./pages/Dashboard";
import BuildStatus from "./pages/BuildStatus";
import BuildResult from "./pages/BuildResult";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/status/:buildId" element={<BuildStatus />} />
          <Route path="/result/:buildId" element={<BuildResult />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
