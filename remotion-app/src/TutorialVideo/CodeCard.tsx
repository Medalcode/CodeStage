import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const CodeCard: React.FC<{
  filename?: string;
  codeSnippet: string[];
}> = ({ filename = "tutorial.py", codeSnippet }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.6 },
  });

  // Reveal lines one by one over time
  const visibleLineCount = Math.min(
    codeSnippet.length,
    Math.floor(frame / 6) + 1
  );

  return (
    <div
      style={{
        transform: `scale(${entrance})`,
        width: "90%",
        maxWidth: "1300px",
        background: "#0f172a",
        borderRadius: "18px",
        border: "1px solid rgba(255, 255, 255, 0.1)",
        boxShadow: "0 20px 40px rgba(0, 0, 0, 0.6)",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', 'Fira Code', 'Courier New', monospace",
      }}
    >
      {/* Window Header */}
      <div
        style={{
          background: "#1e293b",
          padding: "14px 20px",
          display: "flex",
          alignItems: "center",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        }}
      >
        {/* macOS Buttons */}
        <div style={{ display: "flex", gap: "8px" }}>
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#ef4444" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#f59e0b" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#22c55e" }} />
        </div>
        <div
          style={{
            marginLeft: "auto",
            marginRight: "auto",
            color: "#94a3b8",
            fontSize: "15px",
            fontWeight: 600,
          }}
        >
          {filename}
        </div>
      </div>

      {/* Code Body */}
      <div style={{ padding: "28px 36px", fontSize: "24px", lineHeight: 1.6 }}>
        {codeSnippet.slice(0, visibleLineCount).map((line, idx) => (
          <div key={idx} style={{ display: "flex", gap: "20px" }}>
            <span style={{ color: "#475569", width: "40px", textAlign: "right", userSelect: "none" }}>
              {idx + 1}
            </span>
            <span style={{ color: line.startsWith("#") ? "#64748b" : "#e2e8f0" }}>
              {line}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
