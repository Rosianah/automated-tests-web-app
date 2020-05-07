import React, { Component } from "react";
import axios from 'axios'; 
import Button from '@material-ui/core/Button'

class Run extends Component {
        onRunTest = event => {
        axios.post("http://localhost:5000/")  
    };

    render() {
        return ( 
            <div><Button variant="contained" color="primary" onClick={this.onRunTest}>Run Test</Button> </div>
        )
        }
    
}

export default Run