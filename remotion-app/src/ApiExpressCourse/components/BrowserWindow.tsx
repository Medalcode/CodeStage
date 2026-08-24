import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const BrowserWindow: React.FC<{
  url?: string;
  title?: string;
  contentType?: "webpage" | "api_json" | "dashboard";
  mainContent?: string;
  previewImage?: string;
}> = ({
  url = "https://localhost:3000/api/dashboard",
  title = "Navegador Web — Aplicación en Ejecución",
  contentType = "webpage",
  mainContent = "Aplicación Web Activa y Respondiendo Peticiones HTTP",
  previewImage,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  return (
    <div
      style={{
        transform: `scale(${scale})`,
        width: "90%",
        maxWidth: "1200px",
        height: "680px",
        borderRadius: "16px",
        overflow: "hidden",
        boxShadow: "0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 35px rgba(56, 189, 248, 0.2)",
        background: "#0f172a",
        border: "1px solid rgba(255, 255, 255, 0.15)",
        display: "flex",
        flexDirection: "column",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* Browser Header / Tab Bar */}
      <div
        style={{
          background: "#1e293b",
          padding: "12px 18px",
          display: "flex",
          alignItems: "center",
          gap: "14px",
          borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
        }}
      >
        {/* Window Control Buttons */}
        <div style={{ display: "flex", gap: "8px" }}>
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#ef4444" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#f59e0b" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#10b981" }} />
        </div>

        {/* Browser Nav Buttons */}
        <div style={{ display: "flex", gap: "10px", color: "#64748b", fontSize: "14px", fontWeight: "bold" }}>
          <span>‹</span>
          <span>›</span>
          <span>↻</span>
        </div>

        {/* Address Bar */}
        <div
          style={{
            flex: 1,
            background: "#0f172a",
            borderRadius: "8px",
            padding: "6px 14px",
            color: "#38bdf8",
            fontSize: "14px",
            fontFamily: "'JetBrains Mono', monospace",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            border: "1px solid rgba(56, 189, 248, 0.3)",
          }}
        >
          <span style={{ color: "#10b981" }}>🔒</span>
          <span>{url}</span>
        </div>
      </div>

      {/* Browser Viewport Area */}
      <div
        style={{
          flex: 1,
          background: "#090d16",
          padding: "32px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          color: "#ffffff",
          textAlign: "center",
        }}
      >
        <div
          style={{
            padding: "8px 16px",
            borderRadius: "20px",
            background: "rgba(56, 189, 248, 0.15)",
            color: "#38bdf8",
            fontSize: "14px",
            fontWeight: 600,
            marginBottom: "16px",
            letterSpacing: "1px",
          }}
        >
          {title.toUpperCase()}
        </div>

        {previewImage ? (
          <img
            src={previewImage}
            alt="Preview"
            style={{
              maxWidth: "85%",
              maxHeight: "380px",
              borderRadius: "12px",
              boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
            }}
          />
        ) : (
          <div
            style={{
              width: "85%",
              background: "#1e293b",
              borderRadius: "12px",
              padding: "28px",
              border: "1px solid rgba(255, 255, 255, 0.1)",
            }}
          >
            <h2 style={{ fontSize: "28px", color: "#f8fafc", marginBottom: "12px" }}>
              {mainContent}
            </h2>
            <p style={{ color: "#94a3b8", fontSize: "16px", lineHeight: "1.6" }}>
              Estado HTTP 200 OK — Servidor desplegado correctamente y listo para recibir usuarios.
            </p>
            
            <div
              style={{
                marginTop: "24px",
                display: "inline-flex",
                gap: "16px",
              }}
            >
              <div
                style={{
                  background: "#38bdf8",
                  color: "#0f172a",
                  padding: "10px 24px",
                  borderRadius: "8px",
                  fontWeight: "bold",
                  fontSize: "15px",
                }}
              >
                ⚡ Ver API Docs
              </div>
              <div
                style={{
                  background: "rgba(255,255,255,0.1)",
                  color: "#ffffff",
                  padding: "10px 24px",
                  borderRadius: "8px",
                  fontWeight: 600,
                  fontSize: "15px",
                }}
              >
                🔍 Inspeccionar Red
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
