import React, { Component } from 'react'
import axios from 'axios'
import Button from '@material-ui/core/Button'

class Run extends Component {
        onRunTest = event => {
          const axiosConfig = {
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*'
            }
          }
          axios.post('http://localhost:5001/', axiosConfig)
        };

        render () {
          return (
            <div><Button variant="contained" color="primary" onClick={this.onRunTest}>Run Test</Button> </div>
          )
        }
}

export default Run
