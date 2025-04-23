import { useCallback } from "react";
import { useFetch } from "./useFetch";
import { useStream } from "./useStream";
import { Truth } from "../components/Truths/Truth";

const API_URL = import.meta.env.VITE_API_URL;

export const useTruths = () => {
  const { data, setData, error, loading } = useFetch<Truth>(
    `${API_URL}/truths`
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

  useStream<Truth>(`${API_URL}/stream`, handleNewTruth);

  return { data, error, loading };
};
