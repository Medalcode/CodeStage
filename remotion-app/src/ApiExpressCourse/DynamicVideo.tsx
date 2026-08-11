import React from "react";
import { AbsoluteFill, Series, Audio, staticFile } from "remotion";

import { Scene1Intro } from "./components/Scene1Intro";
import { TerminalWindow } from "./components/TerminalWindow";
import { EditorWindow } from "./components/EditorWindow";
import { HttpClientWindow } from "./components/HttpClientWindow";
import { DiagramWindow } from "./components/DiagramWindow";
import { FeaturesWindow } from "./components/FeaturesWindow";
import { Scene6Outro } from "./components/Scene6Outro";
import { SubtitleBar } from "./components/SubtitleBar";

import scriptData from "../data/current_script.json";

export const DynamicVideo: React.FC<{
  script?: any;
}> = ({ script }) => {
  const activeScript = script || scriptData;
  const scenes = activeScript.scenes || [];

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

      <Series>
        {scenes.map((scene: any) => {
          const duration = scene.durationInFrames || 240;

          let sceneContent = null;
          if (scene.type === "intro") {
            sceneContent = (
              <Scene1Intro
                title={scene.title}
                subtitle={scene.subtitle}
                requirements={scene.requirements}
              />
            );
          } else if (scene.type === "terminal") {
            sceneContent = (
              <TerminalWindow
                title={scene.title}
                commands={scene.commands || []}
              />
            );
          } else if (scene.type === "editor") {
            sceneContent = (
              <EditorWindow
                filename={scene.filename}
                codeLines={scene.codeLines || []}
              />
            );
          } else if (scene.type === "http-client") {
            sceneContent = (
              <HttpClientWindow
                method={scene.method || "GET"}
                url={scene.url}
                statusCode={scene.statusCode}
                requestBody={scene.requestBody}
                responseBody={scene.responseBody}
              />
            );
          } else if (scene.type === "diagram") {
            sceneContent = (
              <DiagramWindow
                title={scene.title}
                nodes={scene.nodes || []}
              />
            );
          } else if (scene.type === "features") {
            sceneContent = (
              <FeaturesWindow
                title={scene.title}
                features={scene.features || []}
              />
            );
          } else if (scene.type === "outro") {
            sceneContent = (
              <Scene6Outro
                title={scene.title}
                subtitle={scene.subtitle}
                githubRepo={scene.githubRepo}
              />
            );
          }

          return (
            <Series.Sequence key={scene.id} durationInFrames={duration}>
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {/* Dynamic TTS Audio Track for this scene */}
                {scene.audioFile && (
                  <Audio src={staticFile(`audio/${scene.audioFile}`)} />
                )}

                {sceneContent}
                {scene.speechText && <SubtitleBar speechText={scene.speechText} />}
              </div>
            </Series.Sequence>
          );
        })}
      </Series>
    </AbsoluteFill>
  );
};
