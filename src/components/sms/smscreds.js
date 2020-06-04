import React, { Component } from "react";
import TextField from "@material-ui/core/TextField";
import Button from '@material-ui/core/Button'
import { makeStyles } from "@material-ui/core/styles";
import axios from 'axios'

const useStyles = makeStyles(theme => ({
  root: {
    "& .MuiTextField-root": {
      margin: theme.spacing(1),
      width: "25ch"
    }
  }
}));

export default function StateTextFields() {
    const classes = useStyles();
    const [code, setCode] = React.useState("")
    const handleCodeChange = event => {
      setCode(event.target.value)
    }

    const [phone, setPhone] = React.useState("")
    const handlePhoneChange = event => {
      setPhone(event.target.value)
    }

    const handleSubmit = event => {
      console.log(code, phone)

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    
      axios.post('http://localhost:5002/sms', {code, phone}, axiosConfig)
    }
    
    
    return (
      <div>
        <form className={classes.root} noValidate autoComplete="off">
          <div>
          <TextField
            id="outlined-uncontrolled"
            label="Short code"
            defaultValue=" "
            variant="outlined"
            onChange = {handleCodeChange}
          />
          <TextField
            id="outlined-uncontrolled"
            label="Phone Number"
            defaultValue=" "
            variant="outlined"
            onChange = {handlePhoneChange}
          />        
          </div>
          <Button  variant="contained" color="primary" onClick={handleSubmit}>
            Upload
          </Button>
        </form>      
      </div>
    )
}
  