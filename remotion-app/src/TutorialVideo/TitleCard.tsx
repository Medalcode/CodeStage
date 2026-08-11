import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const TitleCard: React.FC<{
  title: string;
  subtitle: string;
  category?: string;
}> = ({ title, subtitle, category = "TUTORIAL AUTOMATION" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance spring animation
  const scale = spring({
    frame,
    fps,
    config: { damping: 12, mass: 0.5 },
  });

  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(frame, [0, 20], [40, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale}) translateY(${translateY}px)`,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "rgba(15, 23, 42, 0.75)",
        backdropFilter: "blur(20px)",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        borderRadius: "24px",
        padding: "48px 64px",
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px rgba(99, 102, 241, 0.2)",
        maxWidth: "1400px",
        width: "90%",
      }}
    >
      {/* Category Badge */}
      <div
        style={{
          background: "linear-gradient(90deg, #6366f1, #a855f7)",
          color: "#ffffff",
          fontSize: "18px",
          fontWeight: 700,
          letterSpacing: "2px",
          padding: "8px 20px",
          borderRadius: "9999px",
          marginBottom: "24px",
          boxShadow: "0 4px 14px rgba(168, 85, 247, 0.4)",
          textTransform: "uppercase",
        }}
      >
        {category}
      </div>

      {/* Main Title */}
      <h1
        style={{
          fontSize: "64px",
          fontWeight: 800,
          color: "#ffffff",
          textAlign: "center",
          margin: 0,
          lineHeight: 1.15,
          fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
          background: "linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}
      >
        {title}
      </h1>

      {/* Subtitle */}
      <p
        style={{
          fontSize: "28px",
          color: "#94a3b8",
          marginTop: "20px",
          marginBottom: 0,
          textAlign: "center",
          fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
          fontWeight: 400,
        }}
      >
        {subtitle}
      </p>
    </div>
  );
};
