import React from "react";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";
import Button from '@material-ui/core/Button'
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
  const [hash, setHash] = React.useState("")
  const handleHashChange = event => {
    setHash(event.target.value)
  }

  const [id, setId] = React.useState("")
  const handleIdChange = event => {
    setId(event.target.value)
  }

  const handleSubmit = event => {
    console.log(hash, id)

    const axiosConfig = {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    }
  
    axios.post('http://localhost:5002/telegram', {hash, id}, axiosConfig)
  }

  return (
    <div>
      <form className={classes.root} noValidate autoComplete="off">
        <div>
        <TextField
          id="outlined-uncontrolled"
          label="API HASH"
          defaultValue=" "
          variant="outlined"
          onChange = {handleHashChange}
        />
        <TextField
          id="outlined-uncontrolled"
          label="API ID"
          defaultValue=" "
          variant="outlined"
          onChange = {handleIdChange}
        />        
        </div>
        <Button variant="contained" color="primary" onClick = {handleSubmit}>
          Upload
        </Button>
      </form>      
    </div>
  );
}
