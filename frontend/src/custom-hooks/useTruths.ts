import { useCallback } from "react";
import { useFetch } from "./useFetch";
import { useStream } from "./useStream";
import { Truth } from "../components/Truths/Truths";

export const useTruths = () => {
  const { data, setData, error, loading } = useFetch<Truth>(
    "http://localhost:8000/truths"
  );

  const handleNewTruth = useCallback(
    (newTruth: Truth) => {
      setData((prev) => {
        const exists = prev.some((t) => t.external_id === newTruth.external_id);
        return exists ? prev : [newTruth, ...prev];
      });
    },
    [setData]
  );

  useStream<Truth>("http://localhost:8000/stream", handleNewTruth);

  return { data, error, loading };
};
