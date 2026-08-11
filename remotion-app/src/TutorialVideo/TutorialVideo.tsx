import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { TitleCard } from "./TitleCard";
import { CodeCard } from "./CodeCard";
import { SubtitleBanner } from "./SubtitleBanner";

export interface TutorialVideoProps {
  title: string;
  subtitle: string;
  category: string;
  filename: string;
  codeSnippet: string[];
  scriptText: string;
}

export const TutorialVideo: React.FC<TutorialVideoProps> = ({
  title,
  subtitle,
  category,
  filename,
  codeSnippet,
  scriptText,
}) => {
  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(circle at 50% 30%, #1e1b4b 0%, #090d16 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* Background Decorative Blur Orbs */}
      <div
        style={{
          position: "absolute",
          top: "10%",
          left: "15%",
          width: "400px",
          height: "400px",
          borderRadius: "50%",
          background: "rgba(99, 102, 241, 0.15)",
          filter: "blur(100px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "10%",
          right: "15%",
          width: "450px",
          height: "450px",
          borderRadius: "50%",
          background: "rgba(168, 85, 247, 0.15)",
          filter: "blur(120px)",
        }}
      />

      {/* Sequence 1: Intro Title Card (0s - 3s / 0 - 90 frames) */}
      <Sequence from={0} durationInFrames={90}>
        <TitleCard title={title} subtitle={subtitle} category={category} />
      </Sequence>

      {/* Sequence 2: Code Animation Card (3s - 10s / 90 - 210 frames) */}
      <Sequence from={90} durationInFrames={210}>
        <CodeCard filename={filename} codeSnippet={codeSnippet} />
      </Sequence>

      {/* Subtitle Banner across the bottom */}
      <Sequence from={0} durationInFrames={300}>
        <SubtitleBanner text={scriptText} />
      </Sequence>
    </AbsoluteFill>
  );
};
