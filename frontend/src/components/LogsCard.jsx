import Card from "./Card";
import TerminalLogs from "./TerminalLogs";

export default function LogsCard({ logs }) {
  return (
    <Card className="overflow-hidden">
      <TerminalLogs logs={logs} />
    </Card>
  );
}
