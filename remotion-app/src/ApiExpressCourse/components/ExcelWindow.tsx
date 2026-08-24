import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const ExcelWindow: React.FC<{
  title?: string;
  sheetName?: string;
  formula?: string;
  headers?: string[];
  rows?: Array<Array<string | number>>;
  summaryText?: string;
}> = ({
  title = "Ventas_y_Analisis_2026.xlsx — Excel",
  sheetName = "Reporte_General",
  formula = "=SUMA(C2:C6)",
  headers = ["ID", "Producto / Categoría", "Ventas (USD)", "Crecimiento", "Estado"],
  rows = [
    ["101", "Licencias SaaS Enterprise", "$ 14,500", "+ 24%", "Completado"],
    ["102", "Suscripciones Mensuales", "$ 8,900", "+ 18%", "Completado"],
    ["103", "Servicios de Consultoría", "$ 12,300", "+ 35%", "Completado"],
    ["104", "Capacitación Corporativa", "$ 6,400", "+ 12%", "Completado"],
    ["TOTAL", "Métricas Consolidadas", "$ 42,100", "+ 22%", "ACTIVO"],
  ],
  summaryText = "Total de ingresos calculados automáticamente en la hoja de cálculo.",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 90 },
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
        boxShadow: "0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 35px rgba(16, 185, 129, 0.2)",
        background: "#064e3b",
        border: "1px solid rgba(16, 185, 129, 0.3)",
        display: "flex",
        flexDirection: "column",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* Excel Title Bar & Ribbon */}
      <div
        style={{
          background: "#047857",
          padding: "10px 20px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          color: "#ffffff",
          fontWeight: "bold",
          fontSize: "15px",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <span style={{ fontSize: "20px" }}>📊</span>
          <span>{title}</span>
        </div>
        <div style={{ background: "#065f46", padding: "4px 12px", borderRadius: "6px", fontSize: "13px" }}>
          Hoja: {sheetName}
        </div>
      </div>

      {/* Excel Formula Bar */}
      <div
        style={{
          background: "#022c22",
          padding: "8px 20px",
          display: "flex",
          alignItems: "center",
          gap: "14px",
          borderBottom: "1px solid rgba(16, 185, 129, 0.2)",
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "14px",
          color: "#34d399",
        }}
      >
        <span style={{ color: "#a7f3d0", fontWeight: "bold" }}>fx</span>
        <div
          style={{
            flex: 1,
            background: "#064e3b",
            padding: "4px 12px",
            borderRadius: "4px",
            color: "#ffffff",
          }}
        >
          {formula}
        </div>
      </div>

      {/* Excel Sheet Grid Container */}
      <div
        style={{
          flex: 1,
          background: "#091e17",
          padding: "20px",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            color: "#ecfdf5",
            fontSize: "15px",
            textAlign: "left",
          }}
        >
          <thead>
            <tr style={{ background: "#047857", color: "#ffffff" }}>
              {headers.map((h, i) => (
                <th
                  key={i}
                  style={{
                    padding: "12px 16px",
                    border: "1px solid #065f46",
                    fontWeight: 700,
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, rIdx) => {
              const isTotal = rIdx === rows.length - 1;
              const rowBg = isTotal ? "rgba(16, 185, 129, 0.25)" : (rIdx % 2 === 0 ? "#04382c" : "#064e3b");
              const rowWeight = isTotal ? "bold" : "normal";
              const rowColor = isTotal ? "#34d399" : "#ecfdf5";

              return (
                <tr
                  key={rIdx}
                  style={{
                    background: rowBg,
                    fontWeight: rowWeight,
                    color: rowColor,
                  }}
                >
                  {row.map((cell, cIdx) => (
                    <td
                      key={cIdx}
                      style={{
                        padding: "12px 16px",
                        border: "1px solid rgba(16, 185, 129, 0.2)",
                      }}
                    >
                      {cell}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>

        {/* Footer Summary Banner */}
        <div
          style={{
            marginTop: "auto",
            background: "rgba(16, 185, 129, 0.15)",
            borderRadius: "10px",
            padding: "14px 20px",
            color: "#6ee7b7",
            fontSize: "14px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            border: "1px solid rgba(16, 185, 129, 0.3)",
          }}
        >
          <span>💡 <strong>Nota del Reporte:</strong> {summaryText}</span>
          <span style={{ background: "#059669", color: "#ffffff", padding: "4px 12px", borderRadius: "6px", fontWeight: "bold" }}>
            EXCEL DATA OK
          </span>
        </div>
      </div>
    </div>
  );
};
