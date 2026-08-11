import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const FeaturesWindow: React.FC<{
  title: string;
  features?: string[];
}> = ({ title, features = ["Rápido y Ligero", "Ecosistema npm gigante", "Fácil de aprender"] }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 12 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        background: "rgba(15, 23, 42, 0.85)",
        backdropFilter: "blur(20px)",
        border: "1px solid rgba(168, 85, 247, 0.3)",
        borderRadius: "20px",
        padding: "36px 48px",
        boxShadow: "0 20px 40px rgba(0,0,0,0.6), 0 0 40px rgba(168, 85, 247, 0.2)",
        maxWidth: "1200px",
        width: "85%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <h2
        style={{
          color: "#a855f7",
          fontSize: "36px",
          fontWeight: 800,
          marginBottom: "32px",
          textAlign: "center",
          fontFamily: "'Inter', system-ui, sans-serif",
        }}
      >
        ✨ {title}
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "20px",
          width: "100%",
        }}
      >
        {features.map((feat, index) => {
          const itemDelay = index * 8;
          const itemScale = spring({ frame: Math.max(0, frame - itemDelay), fps, config: { damping: 12 } });

          return (
            <div
              key={index}
              style={{
                transform: `scale(${itemScale})`,
                background: "rgba(30, 41, 59, 0.7)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                borderRadius: "14px",
                padding: "20px 24px",
                color: "#f8fafc",
                fontSize: "20px",
                fontWeight: 600,
                display: "flex",
                alignItems: "center",
                gap: "14px",
              }}
            >
              <span style={{ color: "#22c55e", fontSize: "24px" }}>✔</span>
              <span>{feat}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
