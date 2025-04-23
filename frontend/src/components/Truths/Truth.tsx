import DOMPurify from "dompurify";
import { useState } from "react";
import { formatTime } from "./utils";
import styles from "./Truths.module.css";

export type MediaAttachment = {
  id: string;
  url: string;
  meta: {
    small?: {
      size: string;
      width: number;
      height: number;
      aspect: number;
    };
    original?: {
      size?: string;
      width: number;
      height: number;
      bitrate?: number;
      duration?: number;
      frame_rate?: string;
      aspect?: number;
    };
    colors?: {
      accent: string;
      background: string;
      foreground: string;
    };
  };
  type: "image" | "video";
  blurhash: string | null;
  text_url: string | null;
  processing: string;
  remote_url: string | null;
  description: string | null;
  preview_url: string | null;
  external_video_id: string | null;
  preview_remote_url: string | null;
};

export type Truth = {
  id: number;
  content: string;
  external_id: number;
  timestamp: string;
  url: string;
  media_attachments: MediaAttachment[];
  ai_summary: string;
};

interface Props {
  truth: Truth;
}

export const Truth = ({ truth }: Props) => {
  const [expanded, setExpanded] = useState(false);
  const cleanHTML = DOMPurify.sanitize(truth.content);
  const textOnly = cleanHTML.replace(/<[^>]+>/g, "").trim();
  const needsTruncate = textOnly.length > 128;
  const truncatedText = textOnly.slice(0, 128);
  const hasNoContent = textOnly.length === 0;

  return (
    <li
      style={{
        padding: 20,
        display: "flex",
        justifyContent: "space-between",
      }}
    >
      <div style={{ display: "flex", alignItems: "start" }}>
        <div
          style={{
            marginRight: 20,
            whiteSpace: "nowrap",
            color: "rgb(196,199,205)",
          }}
        >
          {formatTime(truth.timestamp)}
        </div>
        <div>
          <div className={styles.content}>
            {hasNoContent ? (
              <div>No content provided</div>
            ) : expanded || !needsTruncate ? (
              <div dangerouslySetInnerHTML={{ __html: cleanHTML }} />
            ) : (
              <div
                dangerouslySetInnerHTML={{
                  __html: DOMPurify.sanitize(truncatedText + "..."),
                }}
              />
            )}
          </div>
          {truth.ai_summary !== "" && (
            <div style={{ marginTop: 10, color: "gray" }}>
              AI summary: {DOMPurify.sanitize(truth.ai_summary)}
            </div>
          )}
        </div>
      </div>
      {!hasNoContent && needsTruncate && (
        <button
          onClick={() => setExpanded((prev) => !prev)}
          style={{
            marginLeft: 20,
            cursor: "pointer",
            background: "none",
            border: "none",
            color: "rgb(196,199,205)",
            padding: 0,
          }}
        >
          {expanded ? "▲" : "▼"}
        </button>
      )}
    </li>
  );
};
