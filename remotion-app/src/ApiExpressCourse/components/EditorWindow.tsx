import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface EditorWindowProps {
  filename?: string;
  codeLines: string[];
}

export const EditorWindow: React.FC<EditorWindowProps> = ({
  filename = "index.js",
  codeLines,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.6 },
  });

  const visibleLines = Math.min(codeLines.length, Math.floor(frame / 8) + 1);

  return (
    <div
      style={{
        transform: `scale(${entrance})`,
        width: "90%",
        maxWidth: "1350px",
        background: "#0f172a",
        borderRadius: "16px",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 30px rgba(99, 102, 241, 0.15)",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
      }}
    >
      {/* VS Code File Tab Bar */}
      <div
        style={{
          background: "#1e293b",
          display: "flex",
          alignItems: "center",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        }}
      >
        <div
          style={{
            background: "#0f172a",
            padding: "12px 24px",
            color: "#38bdf8",
            fontSize: "15px",
            fontWeight: 600,
            borderTop: "2px solid #38bdf8",
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <span>📄</span> {filename}
        </div>
      </div>

      {/* Editor Body */}
      <div style={{ padding: "28px 36px", fontSize: "22px", lineHeight: 1.6 }}>
        {codeLines.slice(0, visibleLines).map((line, idx) => {
          let color = "#e2e8f0";
          if (line.startsWith("//")) color = "#64748b"; // Comments
          else if (line.includes("const ") || line.includes("let ") || line.includes("require")) color = "#c084fc"; // Keywords
          else if (line.includes("'") || line.includes('"') || line.includes("`")) color = "#4ade80"; // Strings

          return (
            <div key={idx} style={{ display: "flex", gap: "24px" }}>
              <span style={{ color: "#475569", width: "40px", textAlign: "right", userSelect: "none" }}>
                {idx + 1}
              </span>
              <span style={{ color }}>{line}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
