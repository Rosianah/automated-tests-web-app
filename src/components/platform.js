import React from 'react'
import { Link } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'
import Card from '@material-ui/core/Card'
import CardActionArea from '@material-ui/core/CardActionArea'
import CardActions from '@material-ui/core/CardActions'
import CardContent from '@material-ui/core/CardContent'
import CardMedia from '@material-ui/core/CardMedia'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'
import { Grid } from '@material-ui/core'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginTop: theme.spacing(3),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1)

  },
  control: {
    padding: theme.spacing(3)
  }
}))

export default function SpacingGrid () {
  const [spacing] = React.useState(2)
  const classes = useStyles()

  return (

    <Grid container className={classes.root} spacing={4}>
      <Grid item xs={12}>
        <Grid container justify="center" spacing={spacing}>

          <Grid item md={4}>
            <Card className={classes.root}>
              <CardActionArea>
                <CardMedia
                  component="img"
                  alt="Telegram logo"
                  height="350"
                  image="https://www.userlogos.org/files/logos/fernandosantucci/telegram.png"
                  title="Telegram logo"
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="h2">
                      Telegram
                  </Typography>
                  <Typography variant="body2" color="textSecondary" component="p">
                    Run automated tests on Telegram
                  </Typography>
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

          <Grid item md={4}>
            <Card className={classes.root}>
              <CardActionArea>
                <CardMedia
                  component="img"
                  alt="SMS"
                  height="350"
                  image="https://www.dcs2way.co.uk/SiteAssets/Images/News/speech-bubble-icon.png"
                  title="SMS"
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="h2">
                      SMS
                  </Typography>
                  <Typography variant="body2" color="textSecondary" component="p">
                    Run automated tests on SMS
                  </Typography>
                </CardContent>
              </CardActionArea>
              <CardActions>
                <Link to= {'/smsStepper'}>
                  <Button size="small" color="primary">
                    Run Test
                  </Button>
                </Link>
              </CardActions>
            </Card>
          </Grid>

          <Grid item md={4}>
            <Card className={classes.root}>
              <CardActionArea>
                <CardMedia
                  component="img"
                  alt="WhatsApp"
                  height="350"
                  image="http://img.talkandroid.com/uploads/2014/03/whatsapp_app_icon.png"
                  title="WhatsApp"
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="h2">
                      WhatsApp
                  </Typography>
                  <Typography variant="body2" color="textSecondary" component="p">
                    Run automated tests on WhatsApp
                  </Typography>
                </CardContent>
              </CardActionArea>
              <CardActions>
                <Link to= {'/'}>
                  <Button disabled size="small" color="primary">
                    Run Test
                  </Button>
                </Link>
              </CardActions>
            </Card>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  )
}
