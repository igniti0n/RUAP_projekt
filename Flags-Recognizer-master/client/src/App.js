import React, { useState } from 'react'
import axios from 'axios'
import './App.css'
const App = () => {
  const [image, setImage] = useState();
  const [path, setPath] = useState();
  const [result, setResult] = useState();


  const onChange = (e) => {
    let files = e.target.files;
    if (files[0] !== undefined) {
      setPath(files[0].name)
      let reader = new FileReader();
      reader.readAsDataURL(files[0]);

      reader.onload = (e) => {
        setImage(e.target.result)
      }
    }
  }


  const handleRequest = async () => {
    try {
      const url = 'http://127.0.0.1:5000/'
      const response = await axios({
        method: 'POST',
        url: url,
        data: {
          name: path.toString()
        }
      })
      setResult(response.data)
    } catch (error) {
      console.log(error)
    }
  }
  return (
    <div className="mainContainer">
      <div className="titleContainer">
        <h1>FLAG RECOGNIZER</h1>
      </div>
      <div className="predictionContainer">
        <img src={image} className="image" />
        <input
          type="file"
          name="file"
          onChange={(e) => onChange(e)}
        />
        <button onClick={handleRequest} style={{ marginTop: 30 }}>
          Predict
        </button>
        <div className="prediction">
          <p className="prediction">Prediction =</p>
          <h3 className="result">{result}</h3>
        </div>

      </div>


    </div>
  )
}

export default App;