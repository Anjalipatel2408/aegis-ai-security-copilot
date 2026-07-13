import { useState } from "react";
import { uploadLog, parseLog, detectAnomalies, classifyAttacks, getAttackSummary, getRemediation } from "./api";

function App() {
  const [file, setFile] = useState(null);
  const [logId, setLogId] = useState(null);
  const [status, setStatus] = useState("");
  const [attacks, setAttacks] = useState([]);
  const [remediation, setRemediation] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    setStatus("Uploading...");
    const res = await uploadLog(file);
    setLogId(res.data.log_id);
    setStatus(`Uploaded! Log ID: ${res.data.log_id}`);
  };

  const runFullAnalysis = async () => {
    if (!logId) return;
    setStatus("Parsing...");
    await parseLog(logId);
    setStatus("Detecting anomalies...");
    await detectAnomalies(logId);
    setStatus("Classifying attacks...");
    await classifyAttacks(logId);
    setStatus("Fetching results...");
    const res = await getAttackSummary(logId);
    setAttacks(res.data);
    setStatus("Analysis complete!");
  };

  const fetchRemediation = async (entryId) => {
    const res = await getRemediation(entryId);
    setRemediation(res.data.remediation_advice);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "900px", margin: "0 auto" }}>
      <h1>🛡️ AEGIS AI – Security Copilot</h1>

      <div style={{ marginBottom: "20px" }}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} style={{ marginLeft: "10px" }}>Upload Log</button>
        <button onClick={runFullAnalysis} style={{ marginLeft: "10px" }} disabled={!logId}>
          Run Full Analysis
        </button>
      </div>

      <p><strong>Status:</strong> {status}</p>

      <h2>Detected Attacks: {attacks.length}</h2>
      <table border="1" cellPadding="8" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>IP</th>
            <th>Endpoint</th>
            <th>Attack Type</th>
            <th>MITRE Technique</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {attacks.map((a) => (
            <tr key={a.id}>
              <td>{a.ip_address}</td>
              <td>{a.endpoint}</td>
              <td>{a.attack_type}</td>
              <td>{a.mitre_technique_id} - {a.mitre_technique_name}</td>
              <td><button onClick={() => fetchRemediation(a.id)}>Get Fix</button></td>
            </tr>
          ))}
        </tbody>
      </table>

      {remediation && (
        <div style={{ marginTop: "20px", padding: "15px", background: "#f0f0f0", borderRadius: "8px" }}>
          <h3>🤖 Remediation Advice</h3>
          <p style={{ whiteSpace: "pre-wrap" }}>{remediation}</p>
        </div>
      )}
    </div>
  );
}

export default App;