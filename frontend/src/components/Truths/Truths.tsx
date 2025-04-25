import { useTruths } from "../../custom-hooks/useTruths";
import { formatDate } from "./utils";
import { Truth } from "./Truth";
import styles from "./Truths.module.css";

export const Truths = () => {
  const { data, loading, error } = useTruths();
  let lastDate: string | null = null;

  console.log("Truths", data);

  if (loading) return <div>Loading...</div>;
  if (error instanceof Error) return <div>Error: {error.message}</div>;

  return (
    <div className={styles.truthsContainer}>
      <ul className={styles.truthsList}>
        {data?.map((truth) => {
          const currentDate = formatDate(truth.timestamp);
          const showDateHeader = currentDate !== lastDate;
          lastDate = currentDate;

          return (
            <div key={truth.external_id}>
              {showDateHeader && (
                <div className={styles.dateHeader}>{currentDate}</div>
              )}
              <div
                className={`${styles.truthItemWrapper} ${
                  showDateHeader ? styles.withTopBorder : ""
                }`}
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
