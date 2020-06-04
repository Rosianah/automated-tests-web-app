import axios from 'axios'
import Button from '@material-ui/core/Button'
import React, { Component } from 'react'

class upload extends Component {
state = {
  // Initially, no file is selected
  selectedFile: null,
  fileJson: null
};

// On file select (from the pop up)
onFileChange = async event => {
  // Update the state
  this.setState({ selectedFile: event.target.files[0] })
  const fileReader = new FileReader()
  fileReader.onloadend = () => {
    try {
      this.setState({ fileJson: JSON.parse(fileReader.result) })
    } catch (ex) {
      console.log(ex)
      throw ex
    }
  }
  fileReader.readAsText(event.target.files[0])
}

// On file upload (click the upload button)
onFileUpload = () => {
// Details of the uploaded file
  console.log('fileJSON ==> ', this.state.fileJson)
  // Request made to the backend api

  // axios configs
  const axiosConfig = {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  }
  axios.post('http://localhost:5000/send', this.state.fileJson, axiosConfig)
};

// File content to be displayed after
// file upload is complete
fileData = () => {
  if (this.state.selectedFile) {
    return (
      <div>
        <h4>File Details:</h4>
        <p>File Name: {this.state.selectedFile.name}</p>
        <p>File Type: {this.state.selectedFile.type}</p>
        <p> Last Modified:{' '}
          {this.state.selectedFile.lastModifiedDate.toDateString()}
        </p>
      </div>
    )
  } else {
    return (
      <div>
        <br />
        <h5>Choose file before pressing the upload button</h5>
      </div>
    )
  }
}

render () {
  return (
    <div>
      <div>
        <input variant="contained" color="primary" type="file" onChange={this.onFileChange} accept=".json"/>
        <Button variant="contained" color="primary" onClick={this.onFileUpload}>
          Upload
        </Button>
      </div>
      {this.fileData()}
    </div>
  )
}
}

export default upload
