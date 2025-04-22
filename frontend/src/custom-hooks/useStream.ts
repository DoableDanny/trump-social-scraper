import { useEffect } from "react";

export const useStream = <T>(url: string, onEvent: (data: T) => void) => {
  useEffect(() => {
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      try {
        const parsed: T = JSON.parse(event.data);
        onEvent(parsed);
      } catch (err) {
        console.error("Invalid SSE data", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE error", err);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [url, onEvent]);
};
