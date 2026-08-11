import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const DiagramWindow: React.FC<{
  title: string;
  nodes?: string[];
}> = ({ title, nodes = ["Cliente HTTP", "Servidor Express", "Base de Datos"] }) => {
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
        border: "1px solid rgba(56, 189, 248, 0.3)",
        borderRadius: "20px",
        padding: "36px 48px",
        boxShadow: "0 20px 40px rgba(0,0,0,0.6), 0 0 40px rgba(56, 189, 248, 0.2)",
        maxWidth: "1200px",
        width: "85%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <h2
        style={{
          color: "#38bdf8",
          fontSize: "36px",
          fontWeight: 800,
          marginBottom: "36px",
          textAlign: "center",
          fontFamily: "'Inter', system-ui, sans-serif",
        }}
      >
        🗺️ {title}
      </h2>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "24px",
          width: "100%",
        }}
      >
        {nodes.map((node, index) => {
          const nodeDelay = index * 10;
          const nodeScale = spring({ frame: Math.max(0, frame - nodeDelay), fps, config: { damping: 10 } });

          return (
            <React.Fragment key={index}>
              <div
                style={{
                  transform: `scale(${nodeScale})`,
                  background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
                  border: "2px solid #38bdf8",
                  borderRadius: "16px",
                  padding: "24px 32px",
                  color: "#f8fafc",
                  fontSize: "22px",
                  fontWeight: 700,
                  boxShadow: "0 10px 25px rgba(56, 189, 248, 0.2)",
                  textAlign: "center",
                  minWidth: "200px",
                }}
              >
                {node}
              </div>
              {index < nodes.length - 1 && (
                <div
                  style={{
                    color: "#38bdf8",
                    fontSize: "32px",
                    fontWeight: 900,
                  }}
                >
                  ➔
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
