import React, { Component } from 'react'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import TypoGraphy from '@material-ui/core/Typography'
import NavBar from './components/navbar'
import Posts from './components/platform'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import './App.css'
import stepper from './components/stepper'
import smsStepper from './components/sms/smsStepper'

class App extends Component {
  render () {
    return (
      <Router>
        <div>
          <AppBar color="primary" position="static">
            <Toolbar>
              <TypoGraphy variant="title" color="inherit" >
                <h2>Kuza Bot Test Platform </h2>
              </TypoGraphy>
              <NavBar/>
            </Toolbar>
          </AppBar>

          <Switch>
            <Route exact path="/" component={Posts}/> 
            <Route path="/stepper" component={stepper}/>
            <Route path="/smsStepper" component={smsStepper}/>
          </Switch>       
        </div>
      </Router> 
    )
  }
}

export default App
