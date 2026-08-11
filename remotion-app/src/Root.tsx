import "./index.css";
import { Composition, getInputProps } from "remotion";
import { DynamicVideo } from "./ApiExpressCourse/DynamicVideo";
import scriptData from "./data/current_script.json";

export const RemotionRoot: React.FC = () => {
  const inputProps: any = getInputProps();

  return (
    <>
      {/* 16:9 Landscape Composition (YouTube / Desktop) */}
      <Composition
        id="ExpressApiVideo"
        component={DynamicVideo}
        durationInFrames={1200}
        fps={30}
        width={1920}
        height={1080}
        calculateMetadata={({ props }) => {
          const script = props.script || inputProps.script || scriptData;
          const totalFrames = (script.scenes || []).reduce(
            (acc: number, scene: any) => acc + (scene.durationInFrames || 240),
            0
          );
          return {
            durationInFrames: totalFrames || 1200,
            props: { script }
          };
        }}
        defaultProps={{ script: scriptData }}
      />

      {/* 9:16 Vertical Composition (Shorts / TikTok / Reels) */}
      <Composition
        id="ExpressApiVideoShorts"
        component={DynamicVideo}
        durationInFrames={1200}
        fps={30}
        width={1080}
        height={1920}
        calculateMetadata={({ props }) => {
          const script = props.script || inputProps.script || scriptData;
          const totalFrames = (script.scenes || []).reduce(
            (acc: number, scene: any) => acc + (scene.durationInFrames || 240),
            0
          );
          return {
            durationInFrames: totalFrames || 1200,
            props: { script }
          };
        }}
        defaultProps={{ script: scriptData }}
      />
    </>
  );
};
