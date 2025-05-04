import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [selectedText, setSelectedText] = useState("");

  useEffect(() => {
    console.log("running use Effect")
    chrome.runtime.onMessage.addListener((message) => {
      console.log("message received")
      if (message.type === "TEXT_SELECTED") {
        console.log(message.text)
        setSelectedText(message.text);
      }
    });
  }, []);

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
    </>
  )
}

export default App
