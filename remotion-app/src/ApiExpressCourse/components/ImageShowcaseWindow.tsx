import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const ImageShowcaseWindow: React.FC<{
  title?: string;
  subtitle?: string;
  imageSrc?: string;
  caption?: string;
}> = ({
  title = "Diagrama y Recursos Visuales del Proyecto",
  subtitle = "Ilustración paso a paso de los conceptos clave",
  imageSrc,
  caption = "Esquema conceptual de la arquitectura y componentes del sistema.",
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
        width: "88%",
        maxWidth: "1150px",
        height: "650px",
        borderRadius: "16px",
        overflow: "hidden",
        boxShadow: "0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 35px rgba(236, 72, 153, 0.2)",
        background: "#0f172a",
        border: "1px solid rgba(236, 72, 153, 0.3)",
        display: "flex",
        flexDirection: "column",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* Window Header */}
      <div
        style={{
          background: "#1e293b",
          padding: "12px 20px",
          display: "flex",
          alignItems: "center",
          gap: "12px",
          borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
        }}
      >
        <div style={{ display: "flex", gap: "8px" }}>
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#ef4444" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#f59e0b" }} />
          <div style={{ width: "12px", height: "12px", borderRadius: "50%", background: "#10b981" }} />
        </div>
        <span style={{ color: "#f472b6", fontWeight: "bold", fontSize: "15px" }}>
          🖼️ {title}
        </span>
      </div>

      {/* Main Viewport */}
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
        <h2 style={{ fontSize: "28px", color: "#f472b6", marginBottom: "8px" }}>
          {title}
        </h2>
        <p style={{ color: "#94a3b8", fontSize: "16px", marginBottom: "24px" }}>
          {subtitle}
        </p>

        {imageSrc ? (
          <img
            src={imageSrc}
            alt="Asset"
            style={{
              maxWidth: "85%",
              maxHeight: "360px",
              borderRadius: "12px",
              boxShadow: "0 15px 40px rgba(0,0,0,0.6)",
              border: "1px solid rgba(255,255,255,0.1)",
            }}
          />
        ) : (
          <div
            style={{
              width: "75%",
              height: "280px",
              background: "linear-gradient(135deg, #1e1b4b 0%, #311042 100%)",
              borderRadius: "16px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              border: "2px dashed rgba(236, 72, 153, 0.4)",
              boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
            }}
          >
            <span style={{ fontSize: "54px", marginBottom: "12px" }}>📸</span>
            <span style={{ fontSize: "20px", fontWeight: "bold", color: "#f472b6" }}>
              Visual Asset / Diagrama Ilustrativo
            </span>
          </div>
        )}

        <div
          style={{
            marginTop: "20px",
            color: "#e2e8f0",
            fontSize: "14px",
            background: "rgba(255,255,255,0.05)",
            padding: "8px 20px",
            borderRadius: "20px",
            border: "1px solid rgba(255,255,255,0.1)",
          }}
        >
          {caption}
        </div>
      </div>
    </div>
  );
};
