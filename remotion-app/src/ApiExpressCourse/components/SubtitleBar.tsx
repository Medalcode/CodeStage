import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const SubtitleBar: React.FC<{
  speechText: string;
}> = ({ speechText }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: "40px",
        left: "50%",
        transform: "translateX(-50%)",
        width: "88%",
        maxWidth: "1450px",
        background: "rgba(15, 23, 42, 0.92)",
        backdropFilter: "blur(20px)",
        border: "1px solid rgba(99, 102, 241, 0.35)",
        borderRadius: "18px",
        padding: "22px 36px",
        boxShadow: "0 20px 40px rgba(0, 0, 0, 0.7)",
        overflow: "hidden",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "16px", marginBottom: "8px" }}>
        <div style={{ width: "10px", height: "10px", borderRadius: "50%", background: "#6366f1" }} />
        <span style={{ color: "#6366f1", fontSize: "14px", fontWeight: 700, letterSpacing: "1px" }}>
          NARRACIÓN / GUION
        </span>
      </div>
      <p
        style={{
          margin: 0,
          fontSize: "23px",
          color: "#f8fafc",
          fontWeight: 500,
          textAlign: "left",
          fontFamily: "'Inter', system-ui, sans-serif",
          lineHeight: 1.45,
        }}
      >
        "{speechText}"
      </p>

      {/* Animated Bottom Line */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          height: "4px",
          width: `${progress}%`,
          background: "linear-gradient(90deg, #6366f1, #a855f7)",
        }}
      />
    </div>
  );
};
