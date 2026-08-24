import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const FileExplorerWindow: React.FC<{
  projectName?: string;
  files?: Array<{ name: string; type: "folder" | "file"; active?: boolean }>;
  activeFileDetails?: {
    name: string;
    path: string;
    size: string;
    lines: number;
  };
}> = ({
  projectName = "proyecto-demo",
  files = [
    { name: "src/", type: "folder", active: false },
    { name: "  components/", type: "folder", active: false },
    { name: "    Header.tsx", type: "file", active: false },
    { name: "    Dashboard.tsx", type: "file", active: false },
    { name: "  server.js", type: "file", active: true },
    { name: "  database.sqlite", type: "file", active: false },
    { name: "Dockerfile", type: "file", active: false },
    { name: "package.json", type: "file", active: false },
    { name: ".env", type: "file", active: false },
  ],
  activeFileDetails = {
    name: "server.js",
    path: "src/server.js",
    size: "3.4 KB",
    lines: 142,
  },
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  return (
    <div
      style={{
        transform: `scale(${scale})`,
        width: "90%",
        maxWidth: "1150px",
        height: "650px",
        borderRadius: "16px",
        overflow: "hidden",
        boxShadow: "0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 35px rgba(168, 85, 247, 0.2)",
        background: "#0f172a",
        border: "1px solid rgba(168, 85, 247, 0.3)",
        display: "flex",
        flexDirection: "column",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* Explorer Header */}
      <div
        style={{
          background: "#1e1b4b",
          padding: "12px 20px",
          display: "flex",
          alignItems: "center",
          gap: "12px",
          borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
        }}
      >
        <div style={{ display: "flex", gap: "8px" }}>
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#ef4444" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#f59e0b" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#10b981" }} />
        </div>
        <span style={{ color: "#c084fc", fontWeight: "bold", fontSize: "15px" }}>
          📁 Explorador de Archivos del Proyecto — {projectName}
        </span>
      </div>

      {/* Main Grid: Tree Sidebar + Active File Detail */}
      <div style={{ flex: 1, display: "flex", background: "#090d16" }}>
        {/* Tree Sidebar */}
        <div
          style={{
            width: "320px",
            background: "#0f172a",
            borderRight: "1px solid rgba(255, 255, 255, 0.1)",
            padding: "20px",
            display: "flex",
            flexDirection: "column",
            gap: "10px",
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: "14px",
          }}
        >
          <div style={{ color: "#94a3b8", fontSize: "12px", fontWeight: "bold", letterSpacing: "1px", marginBottom: "8px" }}>
            ESTRUCTURA DE ARCHIVOS
          </div>
          {files.map((item, idx) => (
            <div
              key={idx}
              style={{
                padding: "6px 12px",
                borderRadius: "6px",
                background: item.active ? "rgba(168, 85, 247, 0.25)" : "transparent",
                color: item.active ? "#c084fc" : "#cbd5e1",
                fontWeight: item.active ? "bold" : "normal",
                display: "flex",
                alignItems: "center",
                gap: "8px",
                border: item.active ? "1px solid rgba(168, 85, 247, 0.4)" : "1px solid transparent",
              }}
            >
              <span>{item.type === "folder" ? "📁" : "📄"}</span>
              <span>{item.name}</span>
            </div>
          ))}
        </div>

        {/* File Detail Main Display */}
        <div
          style={{
            flex: 1,
            padding: "36px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            textAlign: "center",
            color: "#ffffff",
          }}
        >
          <div style={{ fontSize: "64px", marginBottom: "16px" }}>⚡</div>
          <h2 style={{ fontSize: "32px", color: "#c084fc", marginBottom: "8px" }}>
            {activeFileDetails.name}
          </h2>
          <p style={{ color: "#94a3b8", fontSize: "16px", marginBottom: "24px" }}>
            Ubicación: <code style={{ color: "#38bdf8", background: "rgba(56, 189, 248, 0.1)", padding: "2px 8px", borderRadius: "4px" }}>{activeFileDetails.path}</code>
          </p>

          <div style={{ display: "flex", gap: "20px" }}>
            <div
              style={{
                background: "#1e293b",
                padding: "16px 28px",
                borderRadius: "12px",
                border: "1px solid rgba(255,255,255,0.1)",
              }}
            >
              <div style={{ color: "#94a3b8", fontSize: "12px" }}>TAMAÑO ARCHIVO</div>
              <div style={{ fontSize: "20px", fontWeight: "bold", color: "#34d399", marginTop: "4px" }}>
                {activeFileDetails.size}
              </div>
            </div>
            <div
              style={{
                background: "#1e293b",
                padding: "16px 28px",
                borderRadius: "12px",
                border: "1px solid rgba(255,255,255,0.1)",
              }}
            >
              <div style={{ color: "#94a3b8", fontSize: "12px" }}>LÍNEAS DE CÓDIGO</div>
              <div style={{ fontSize: "20px", fontWeight: "bold", color: "#38bdf8", marginTop: "4px" }}>
                {activeFileDetails.lines} Líneas
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
