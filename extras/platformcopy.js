import React from 'react'
import { Link } from 'react-router-dom'
import { Grid, Typography } from '@material-ui/core'
import Card from '@material-ui/core/Card'
import CardActionArea from '@material-ui/core/CardActionArea'
import CardActions from '@material-ui/core/CardActions'
import CardContent from '@material-ui/core/CardContent'
import CardMedia from '@material-ui/core/CardMedia'
import Button from '@material-ui/core/Button'
import { posts } from './platform-content'

function Posts (props) {
  return (
    <div style={{ marginTop: 20, padding: 30 }}>
      <Grid container spacing={40} justify="center">
        {posts.map(post => (
          <Grid item key={post.title} md={3}>
            <Card>
              <CardActionArea>
                <CardMedia
                  component="img"
                  alt="Platform-logo"
                  height="400"
                  image={post.image}
                  title="Platform-logo"
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="h2">
                    {post.title}
                  </Typography>
                  <Typography component="p">{post.excerpt}</Typography>
                </CardContent>
              </CardActionArea>
              <CardActions>               
                <Link to= {'/stepper'}>
                  <Button size="small" color="primary">
                    Run Test
                  </Button>
                </Link>
              </CardActions>              
            </Card>
          </Grid>
        ))}
      </Grid>  
    </div>
  )
}

export default Posts
