import React, { useState } from "react";
import axios from "axios";

function App() {
  const [phone, setPhone] = useState("");
  const [language, setLanguage] = useState("english");
  const [result, setResult] = useState(null);

  const startCall = async () => {
    try {
      const response = await axios.post("https://your-backend-url.onrender.com/start-call", {
        phone_number: phone,
        language: language,
      });
      setResult(response.data);
    } catch (error) {
      setResult({ error: error.message });
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto space-y-4">
      <h1 className="text-xl font-semibold">📞 Trigger Voice Agent</h1>
      
      <input
        type="text"
        placeholder="Enter phone number"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        className="w-full p-2 border rounded"
      />

      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="w-full p-2 border rounded"
      >
        <option value="english">English</option>
        <option value="hindi">Hindi</option>
      </select>

      <button
        onClick={startCall}
        className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
      >
        Start Call
      </button>

      {result && (
        <pre className="bg-gray-100 p-4 rounded mt-4 text-sm overflow-x-auto">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;
