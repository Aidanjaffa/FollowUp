import React, { useState, useEffect } from 'react';
import './style.css'

function App() {
  const [data, setData] = useState(null);

  // recieving api data from flask
  function post(event) {
    event.preventDefault(); // stops page reload

    const input = document.getElementById("command"); // collects data from react form

    // fetches api data by going into the post method and giving the content type headers so flask knows to get the json that i sent with the body
    fetch("/api", {
      method: "POST",
      headers : {'Content-Type' : 'application/json'}, // must have so flask knows it be json
      body: JSON.stringify(input.value)
    })
    .then((response) => response.json())
    .then(data => setData(data))
    .catch(error => console.error("Error:", error));
  }

  useEffect(() =>{
    const terminal = document.querySelector(".terminal");
    if (terminal.scrollHeight > 500)
      terminal.scroll(0, terminal.scrollHeight);
    
  })

  return (
    // html stuff
    <div>
      <div className='container'>
        <div className='header'>
            <i className='fa fa-terminal' style={{fontSize: "25px"}}></i>
            <h1 style={{fontSize: "20px", marginLeft: "auto", marginTop: "2px", marginRight: "5px", fontWeight: "400"}}>Terminal 1</h1>
        </div>
        <div className='terminal'>
          {data ? (
            data.message.map((message, index) =>
              <p key={index}>{message}</p>
            )
          ):(
            <p></p>
          )}
          <form style={{marginTop: "auto", marginBottom: "5px"}} method='post' type='submit' onSubmit={post}>
            <input name='command' id='command'></input>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
