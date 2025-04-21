import "./App.css";
import { TruthsComponent } from "./components/Truths/Truths";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <h1>HELLO WORLD</h1>

      <br />
      <br />

      <TruthsComponent />
    </QueryClientProvider>
  );
}

export default App;
