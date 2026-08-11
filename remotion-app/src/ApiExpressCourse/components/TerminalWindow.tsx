import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface TerminalWindowProps {
  title?: string;
  commands: { prompt?: string; text: string; output?: string[] }[];
}

export const TerminalWindow: React.FC<TerminalWindowProps> = ({
  title = "bash — terminal",
  commands,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.6 },
  });

  return (
    <div
      style={{
        transform: `scale(${entrance})`,
        width: "90%",
        maxWidth: "1350px",
        background: "#090d16",
        borderRadius: "16px",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 30px rgba(99, 102, 241, 0.15)",
        overflow: "hidden",
        fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
      }}
    >
      {/* Header Bar */}
      <div
        style={{
          background: "#1e293b",
          padding: "12px 20px",
          display: "flex",
          alignItems: "center",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        }}
      >
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
            fontSize: "14px",
            fontWeight: 600,
          }}
        >
          {title}
        </div>
      </div>

      {/* Terminal Content */}
      <div style={{ padding: "28px 36px", fontSize: "22px", lineHeight: 1.7, color: "#f8fafc" }}>
        {commands.map((cmd, idx) => {
          const delay = idx * 25;
          const typedChars = Math.max(0, Math.floor((frame - delay) * 1.5));
          const textToDisplay = cmd.text.substring(0, typedChars);
          if (frame < delay) return null;

          return (
            <div key={idx} style={{ marginBottom: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <span style={{ color: "#38bdf8", fontWeight: 700 }}>
                  {cmd.prompt || "user@laptop:~/api-express-curso$"}
                </span>
                <span style={{ color: "#4ade80", fontWeight: 600 }}>{textToDisplay}</span>
                {typedChars < cmd.text.length && (
                  <span
                    style={{
                      width: "10px",
                      height: "22px",
                      background: "#38bdf8",
                      display: "inline-block",
                      opacity: Math.floor(frame / 8) % 2 === 0 ? 1 : 0,
                    }}
                  />
                )}
              </div>

              {/* Output block */}
              {typedChars >= cmd.text.length && cmd.output && (
                <div style={{ color: "#94a3b8", marginTop: "8px", paddingLeft: "16px", borderLeft: "2px solid #334155" }}>
                  {cmd.output.map((outLine, oIdx) => (
                    <div key={oIdx}>{outLine}</div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
