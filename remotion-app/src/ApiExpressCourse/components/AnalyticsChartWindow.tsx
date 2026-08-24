import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const AnalyticsChartWindow: React.FC<{
  title?: string;
  metrics?: Array<{ label: string; value: string; change: string }>;
  chartTitle?: string;
}> = ({
  title = "Power BI / Dashboard Analytics — Métricas en Vivo",
  metrics = [
    { label: "Usuarios Activos", value: "18,420", change: "+ 34%" },
    { label: "Tiempo de Respuesta", value: "42 ms", change: "- 18%" },
    { label: "Tasa de Conversión", value: "8.4 %", change: "+ 5.2%" },
    { label: "Uso de CPU Server", value: "22 %", change: "ÓPTIMO" },
  ],
  chartTitle = "Rendimiento Operativo y Ventas Mensuales",
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
        width: "92%",
        maxWidth: "1250px",
        height: "680px",
        borderRadius: "16px",
        overflow: "hidden",
        boxShadow: "0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 35px rgba(245, 158, 11, 0.2)",
        background: "#0f172a",
        border: "1px solid rgba(245, 158, 11, 0.3)",
        display: "flex",
        flexDirection: "column",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* Power BI Header */}
      <div
        style={{
          background: "#1e293b",
          padding: "12px 22px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <span style={{ fontSize: "22px" }}>📈</span>
          <span style={{ color: "#fbbf24", fontWeight: "bold", fontSize: "16px" }}>{title}</span>
        </div>
        <div style={{ background: "#d97706", color: "#ffffff", padding: "4px 12px", borderRadius: "6px", fontSize: "13px", fontWeight: "bold" }}>
          POWER BI DESKTOP
        </div>
      </div>

      {/* Main Content Area */}
      <div
        style={{
          flex: 1,
          background: "#090d16",
          padding: "24px",
          display: "flex",
          flexDirection: "column",
          gap: "24px",
        }}
      >
        {/* KPI Cards Row */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px" }}>
          {metrics.map((m, idx) => (
            <div
              key={idx}
              style={{
                background: "#1e293b",
                padding: "18px",
                borderRadius: "12px",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                display: "flex",
                flexDirection: "column",
              }}
            >
              <span style={{ color: "#94a3b8", fontSize: "13px", fontWeight: 600 }}>{m.label}</span>
              <span style={{ fontSize: "28px", fontWeight: "bold", color: "#f8fafc", margin: "6px 0" }}>{m.value}</span>
              <span style={{ color: "#10b981", fontSize: "13px", fontWeight: "bold" }}>{m.change}</span>
            </div>
          ))}
        </div>

        {/* Animated Bar Chart Viewport */}
        <div
          style={{
            flex: 1,
            background: "#1e293b",
            borderRadius: "12px",
            padding: "20px",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div style={{ color: "#fbbf24", fontWeight: "bold", fontSize: "15px", marginBottom: "20px" }}>
            {chartTitle}
          </div>

          <div
            style={{
              flex: 1,
              display: "flex",
              alignItems: "flex-end",
              justifyContent: "space-around",
              gap: "16px",
              paddingBottom: "10px",
              borderBottom: "2px solid rgba(255, 255, 255, 0.1)",
            }}
          >
            {[
              { month: "Ene", height: "45%", color: "#38bdf8" },
              { month: "Feb", height: "60%", color: "#38bdf8" },
              { month: "Mar", height: "75%", color: "#38bdf8" },
              { month: "Abr", height: "55%", color: "#38bdf8" },
              { month: "May", height: "90%", color: "#fbbf24" },
              { month: "Jun", height: "100%", color: "#10b981" },
            ].map((bar, bIdx) => (
              <div key={bIdx} style={{ display: "flex", flexDirection: "column", alignItems: "center", flex: 1, height: "100%", justifyContent: "flex-end" }}>
                <div
                  style={{
                    width: "60%",
                    maxHeight: bar.height,
                    height: bar.height,
                    background: bar.color,
                    borderRadius: "6px 6px 0 0",
                    boxShadow: `0 0 15px ${bar.color}66`,
                    transition: "height 0.5s ease",
                  }}
                />
                <span style={{ color: "#94a3b8", fontSize: "13px", marginTop: "8px" }}>{bar.month}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
