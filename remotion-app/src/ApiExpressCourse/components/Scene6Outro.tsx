import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const Scene6Outro: React.FC<{
  title: string;
  subtitle: string;
  githubRepo?: string;
}> = ({ title, subtitle, githubRepo = "github.com/Medalcode/api-express-curso" }) => {
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
        background: "rgba(15, 23, 42, 0.85)",
        backdropFilter: "blur(24px)",
        border: "1px solid rgba(168, 85, 247, 0.3)",
        borderRadius: "24px",
        padding: "48px 64px",
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 50px rgba(168, 85, 247, 0.25)",
        maxWidth: "1350px",
        width: "90%",
      }}
    >
      <div
        style={{
          background: "#22c55e",
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
        ¡TUTORIAL COMPLETADO!
      </div>

      <h1
        style={{
          fontSize: "56px",
          fontWeight: 800,
          color: "#ffffff",
          textAlign: "center",
          margin: 0,
          lineHeight: 1.15,
          fontFamily: "'Inter', system-ui, sans-serif",
        }}
      >
        {title}
      </h1>

      <p
        style={{
          fontSize: "24px",
          color: "#94a3b8",
          marginTop: "18px",
          marginBottom: "32px",
          textAlign: "center",
          fontFamily: "'Inter', system-ui, sans-serif",
        }}
      >
        {subtitle}
      </p>

      {/* GitHub Repo Card */}
      <div
        style={{
          background: "#1e293b",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          padding: "16px 32px",
          borderRadius: "14px",
          color: "#38bdf8",
          fontSize: "20px",
          fontWeight: 600,
          display: "flex",
          alignItems: "center",
          gap: "12px",
        }}
      >
        <span>⭐ Código Fuente:</span>
        <span style={{ color: "#f8fafc" }}>{githubRepo}</span>
      </div>
    </div>
  );
};
