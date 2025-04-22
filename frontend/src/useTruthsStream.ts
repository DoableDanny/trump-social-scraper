import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Truth } from "./components/Truths/Truths";

export const useTruthsStream = () => {
  const queryClient = useQueryClient();

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/stream");

    eventSource.onmessage = (event) => {
      try {
        const newTruth = JSON.parse(event.data);

        const current = queryClient.getQueryData<Truth[]>(["truths"]) || [];

        if (current.find((t) => t.id === newTruth.id)) return;

        queryClient.setQueryData<Truth[]>(["truths"], [newTruth, ...current]);
      } catch (err) {
        console.error("Invalid SSE data", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE error:", err);
      eventSource.close();
    };

    return () => eventSource.close();
  }, [queryClient]);
};
