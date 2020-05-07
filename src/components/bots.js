import React, { Component } from 'react'
import axios from 'axios'
import Button from '@material-ui/core/Button'
import ButtonGroup from '@material-ui/core/ButtonGroup'

class bots extends Component {
    onAmiranStaging = async event => {
    // axios configs
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
      var id = 920286769
      axios.post('http://localhost:5001/id', id, axiosConfig)

      console.log(id)
    }

    onAmiranProduction = event => {
      // axios configs
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
      var id = 920286769
      axios.post('http://localhost:5001/id', id, axiosConfig)

      console.log(id)
    }

    render () {
      return (
        <div>
          <h5>Select a bot to test</h5>
          <ButtonGroup variant="text" color="primary" aria-label="text primary button group">
            <Button onClick={this.onAmiranStaging }> Amiran Staging </Button>)
            <Button onClick={this.onAmiranProduction}> Amiran Production </Button>
          </ButtonGroup>
        </div>
      )
    }
}

export default bots
