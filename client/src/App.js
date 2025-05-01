import logo from './logo.svg';
import './App.css';

import React, {useState} from 'react';
import {StyleSheet, Button, View, Text} from 'react-native';

function App() {
  const [bottomtext, setbottomtext] = useState("how was the race?");


  const handleClick = () => {

    // Simple GET request using fetch
    console.log("bungus");
    var fetch_message = fetch("http://127.0.0.1:8000/rating", {
      method: "GET"
    }
    ).then(response => response.json())
    .then(message => setbottomtext(message["evaluation"]));
  }


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Suh dude
        </p>
        <a style={{"paddingBottom": 5}}>
          {bottomtext}
        </a>
        <Button
          title="how was the race?"
          onPress={handleClick}
        />
      </header>
    </div>
  );
}

export default App;
