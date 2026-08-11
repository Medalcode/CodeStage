import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface HttpClientProps {
  method: "GET" | "POST";
  url: string;
  statusCode?: string;
  requestBody?: string;
  responseBody: string;
}

export const HttpClientWindow: React.FC<HttpClientProps> = ({
  method,
  url,
  statusCode = "200 OK",
  requestBody,
  responseBody,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.6 },
  });

  const isPost = method === "POST";
  const methodColor = isPost ? "#f59e0b" : "#6366f1";
  const statusBg = statusCode.includes("201") || statusCode.includes("200") ? "#166534" : "#991b1b";

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
      {/* Client Header Bar */}
      <div
        style={{
          background: "#1e293b",
          padding: "16px 24px",
          display: "flex",
          alignItems: "center",
          gap: "16px",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        }}
      >
        <span
          style={{
            background: methodColor,
            color: "#ffffff",
            fontWeight: 800,
            fontSize: "16px",
            padding: "6px 14px",
            borderRadius: "8px",
          }}
        >
          {method}
        </span>
        <div
          style={{
            background: "#090d16",
            color: "#f8fafc",
            padding: "8px 18px",
            borderRadius: "8px",
            fontSize: "16px",
            flexGrow: 1,
            border: "1px solid rgba(255, 255, 255, 0.1)",
          }}
        >
          {url}
        </div>
        <span
          style={{
            background: statusBg,
            color: "#ffffff",
            fontWeight: 700,
            fontSize: "14px",
            padding: "6px 14px",
            borderRadius: "8px",
          }}
        >
          {statusCode}
        </span>
      </div>

      {/* Body Section */}
      <div style={{ display: "grid", gridTemplateColumns: isPost && requestBody ? "1fr 1fr" : "1fr", gap: "20px", padding: "24px 32px" }}>
        {/* Request Body (If POST) */}
        {isPost && requestBody && (
          <div>
            <div style={{ color: "#94a3b8", fontSize: "14px", marginBottom: "8px", fontWeight: 600 }}>
              REQUEST BODY (JSON)
            </div>
            <pre
              style={{
                background: "#090d16",
                padding: "20px",
                borderRadius: "12px",
                color: "#f59e0b",
                fontSize: "18px",
                margin: 0,
                border: "1px solid rgba(245, 158, 11, 0.2)",
              }}
            >
              {requestBody}
            </pre>
          </div>
        )}

        {/* Response Body */}
        <div>
          <div style={{ color: "#94a3b8", fontSize: "14px", marginBottom: "8px", fontWeight: 600 }}>
            RESPONSE BODY (JSON)
          </div>
          <pre
            style={{
              background: "#090d16",
              padding: "20px",
              borderRadius: "12px",
              color: "#4ade80",
              fontSize: "18px",
              margin: 0,
              border: "1px solid rgba(74, 222, 128, 0.2)",
            }}
          >
            {responseBody}
          </pre>
        </div>
      </div>
    </div>
  );
};
