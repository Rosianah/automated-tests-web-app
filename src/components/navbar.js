import React, { Component } from 'react'
import List from '@material-ui/core/List'
import { BrowserRouter as Router, Route, Link } from 'react-router-dom'
import ListItem from '@material-ui/core/ListItem'
import ListItemText from '@material-ui/core/ListItemText'
import TypoGraphy from '@material-ui/core/Typography'
import { Home } from '@material-ui/icons'

class NavBar extends Component {
  render () {
    return (
      <List component="nav">
        <ListItem component="div">
          <ListItemText inset>
            <TypoGraphy color="inherit" variant="title">
              <Router>
                <Link to="/">Home </Link>
                <Home/>
                <div>
                  <Route exact path = "/" />
                </div>
              </Router>
            </TypoGraphy>
          </ListItemText>
        </ListItem >
      </List>
    )
  }
}

export default NavBar
