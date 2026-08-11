import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const SubtitleBanner: React.FC<{
  text: string;
}> = ({ text }) => {
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
        bottom: "48px",
        left: "50%",
        transform: "translateX(-50%)",
        width: "85%",
        maxWidth: "1400px",
        background: "rgba(15, 23, 42, 0.9)",
        backdropFilter: "blur(16px)",
        border: "1px solid rgba(99, 102, 241, 0.3)",
        borderRadius: "16px",
        padding: "24px 36px",
        boxShadow: "0 10px 30px rgba(0, 0, 0, 0.6)",
        overflow: "hidden",
      }}
    >
      <p
        style={{
          margin: 0,
          fontSize: "26px",
          color: "#f8fafc",
          fontWeight: 600,
          textAlign: "center",
          fontFamily: "'Inter', system-ui, sans-serif",
          lineHeight: 1.4,
        }}
      >
        {text}
      </p>

      {/* Progress Bar */}
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
