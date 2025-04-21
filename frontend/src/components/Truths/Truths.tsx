import { useQuery } from "@tanstack/react-query";
import DOMPurify from "dompurify";
import { useState } from "react";

type Truth = {
  id: number;
  content: string;
  external_id: number;
  timestamp: string;
  url: string;
  media_attachments: any[];
};

const fetchTruths = async (): Promise<Truth[]> => {
  const res = await fetch("http://localhost:8000/truths");
  if (!res.ok) throw new Error("Failed to fetch truths");
  return res.json();
};

const formatTime = (isoString: string) => {
  const date = new Date(isoString);
  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
};

const formatDate = (isoString: string) => {
  const date = new Date(isoString);
  return date.toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};

export const TruthsComponent = () => {
  const { data, error, isLoading } = useQuery({
    queryKey: ["truths"],
    queryFn: fetchTruths,
  });

  const [expanded, setExpanded] = useState<{ [id: number]: boolean }>({});

  const toggleExpand = (id: number) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  if (isLoading) return <div>Loading...</div>;
  if (error instanceof Error) return <div>Error: {error.message}</div>;

  let lastDate: string | null = null;

  return (
    <ul style={{ listStyle: "none", padding: 0 }}>
      {data?.map((truth) => {
        const isExpanded = expanded[truth.id];
        const cleanHTML = DOMPurify.sanitize(truth.content);
        const textOnly = cleanHTML.replace(/<[^>]+>/g, "").trim();
        const needsTruncate = textOnly.length > 128;
        const truncatedText = textOnly.slice(0, 128);
        const hasNoContent = textOnly.length === 0;
        const currentDate = formatDate(truth.timestamp);

        const showDateHeader = currentDate !== lastDate;
        lastDate = currentDate;

        return (
          <div key={truth.id}>
            {showDateHeader && (
              <li style={{ fontWeight: "bold", marginTop: 30 }}>
                {currentDate}
              </li>
            )}
            <li
              style={{
                border: "1px solid gray",
                marginBottom: 20,
                padding: 10,
                borderRadius: 8,
                display: "flex",
                justifyContent: "space-between",
              }}
            >
              <div style={{ display: "flex", alignItems: "start" }}>
                <div style={{ marginRight: 20, whiteSpace: "nowrap" }}>
                  {formatTime(truth.timestamp)}
                </div>
                <div>
                  {hasNoContent ? (
                    <div style={{ fontStyle: "italic", color: "#777" }}>
                      No content provided
                    </div>
                  ) : isExpanded || !needsTruncate ? (
                    <div
                      dangerouslySetInnerHTML={{
                        __html: cleanHTML,
                      }}
                    />
                  ) : (
                    <div
                      dangerouslySetInnerHTML={{
                        __html: DOMPurify.sanitize(truncatedText + "..."),
                      }}
                    />
                  )}
                </div>
              </div>
              {!hasNoContent && needsTruncate && (
                <button
                  onClick={() => toggleExpand(truth.id)}
                  style={{
                    marginTop: 4,
                    cursor: "pointer",
                    background: "none",
                    border: "none",
                    color: "blue",
                    padding: 0,
                  }}
                >
                  {isExpanded ? "▲" : "▼"}
                </button>
              )}
            </li>
          </div>
        );
      })}
    </ul>
  );
};
