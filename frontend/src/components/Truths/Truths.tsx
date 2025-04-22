import { useTruths } from "../../custom-hooks/useTruths";
import { formatDate } from "./utils";
import { Truth } from "./Truth";

export const Truths = () => {
  const { data, loading, error } = useTruths();
  let lastDate: string | null = null;

  if (loading) return <div>Loading...</div>;
  if (error instanceof Error) return <div>Error: {error.message}</div>;

  return (
    <div
      style={{
        backgroundColor: "rgb(8,11,17)",
        display: "flex",
        justifyContent: "center",
        padding: 10,
      }}
    >
      <ul
        style={{
          listStyle: "none",
          padding: 0,
          maxWidth: 1000,
        }}
      >
        {data?.map((truth) => {
          const currentDate = formatDate(truth.timestamp);
          const showDateHeader = currentDate !== lastDate;
          lastDate = currentDate;

          return (
            <div key={truth.external_id}>
              {showDateHeader && (
                <div
                  style={{
                    fontWeight: "bold",
                    marginTop: 30,
                    color: "rgb(115, 134, 170)",
                    marginBottom: 10,
                  }}
                >
                  {currentDate}
                </div>
              )}
              <div
                style={{
                  borderTop: showDateHeader ? "1px solid gray" : "none",
                  borderLeft: "1px solid gray",
                  borderRight: "1px solid gray",
                  borderBottom: "1px solid gray",
                }}
              >
                <Truth truth={truth} />
              </div>
            </div>
          );
        })}
      </ul>
    </div>
  );
};
