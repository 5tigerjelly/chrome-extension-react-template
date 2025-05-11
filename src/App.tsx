import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [selectedText, setSelectedText] = useState("");

  const [relation, setRelation] = useState("");
  const [extractedQuote, setExtractedQuote] = useState("");
  const [scores, setScores] = useState<{ supports: number; contradicts: number; unclear: number } | null>(null);

  useEffect(() => {
    chrome.storage.local.get("selectedText", (result) => {
      if (result.selectedText) {
        setSelectedText(result.selectedText);
        getConclusion(result.selectedText); // call notebook
      }
    });
  }, []);


  const getConclusion = async (text: string) => {
    try {
      const response = await fetch("http://localhost:8888/get_conclusion", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ quote: text })
      });

      const data = await response.json();

      setRelation(data.relation || "unknown");
      setExtractedQuote(data.extractedQuote || "");
      setScores(data.scores || null);
    } catch (error) {
      console.error("Error fetching conclusion:", error);
      setRelation("error");
    }
  };


  return (
    <>
      {/*<div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div> */}
      <h1>Fact-Checking</h1>
      <button onClick={() => { }}>
        Start Read
      </button>
      {selectedText && <p>{selectedText}</p>}
      {/* <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}

      {relation && <p><strong>Conclusion:</strong> {relation}</p>}
      {extractedQuote && <p><strong>Extracted Sentence:</strong> “{extractedQuote}”</p>}
      {scores && (
        <div>
          <strong>Probabilities:</strong>
          <ul>
            <li>Supports: {scores.supports}</li>
            <li>Contradicts: {scores.contradicts}</li>
            <li>Unclear: {scores.unclear}</li>
          </ul>
        </div> )}

    </>
  )
}

export default App
