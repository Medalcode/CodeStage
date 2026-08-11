import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene1Intro: React.FC<{
  title: string;
  subtitle: string;
  requirements?: string[];
}> = ({ title, subtitle, requirements = ["Node.js", "VS Code"] }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 12, mass: 0.5 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "rgba(15, 23, 42, 0.8)",
        backdropFilter: "blur(24px)",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        borderRadius: "24px",
        padding: "48px 64px",
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 50px rgba(99, 102, 241, 0.25)",
        maxWidth: "1350px",
        width: "90%",
      }}
    >
      <div
        style={{
          background: "linear-gradient(90deg, #6366f1, #a855f7)",
          color: "#ffffff",
          fontSize: "18px",
          fontWeight: 800,
          letterSpacing: "2px",
          padding: "8px 22px",
          borderRadius: "9999px",
          marginBottom: "24px",
          textTransform: "uppercase",
        }}
      >
        NODE.JS & EXPRESS TUTORIAL
      </div>

      <h1
        style={{
          fontSize: "60px",
          fontWeight: 800,
          color: "#ffffff",
          textAlign: "center",
          margin: 0,
          lineHeight: 1.15,
          fontFamily: "'Inter', system-ui, sans-serif",
          background: "linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}
      >
        {title}
      </h1>

      <p
        style={{
          fontSize: "26px",
          color: "#94a3b8",
          marginTop: "20px",
          marginBottom: "36px",
          textAlign: "center",
          fontFamily: "'Inter', system-ui, sans-serif",
        }}
      >
        {subtitle}
      </p>

      {/* Requirements Badges */}
      <div style={{ display: "flex", gap: "16px", alignItems: "center" }}>
        <span style={{ color: "#64748b", fontSize: "16px", fontWeight: 600 }}>REQUISITOS:</span>
        {requirements.map((req, idx) => (
          <span
            key={idx}
            style={{
              background: "#1e293b",
              color: "#38bdf8",
              border: "1px solid rgba(56, 189, 248, 0.3)",
              padding: "6px 16px",
              borderRadius: "8px",
              fontSize: "16px",
              fontWeight: 600,
            }}
          >
            ⚡ {req}
          </span>
        ))}
      </div>
    </div>
  );
};
