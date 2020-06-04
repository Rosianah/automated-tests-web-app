import React from 'react'
import { makeStyles } from '@material-ui/core/styles'
import Stepper from '@material-ui/core/Stepper'
import Step from '@material-ui/core/Step'
import StepLabel from '@material-ui/core/StepLabel'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'
import Upload from './smsupload'
import Run from './smsrun'
import Creds from './smscreds'

const useStyles = makeStyles((theme) => ({
  root: {
    marginTop: theme.spacing(10),
    width: '100%'
  },
  backButton: {
    marginRight: theme.spacing(1),
    marginLeft: theme.spacing(24)
  },
  instructions: {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(6),
    marginLeft: theme.spacing(26)
  }
}))

function getSteps () {
  return ['Upload json file', 'Enter your details', 'Run Test', 'Complete test']
}

function getStepContent (stepIndex) {
  switch (stepIndex) {
    case 0:
      return <Upload/>
    case 1:
      return <Creds/>
    case 2:
      return <Run/>
    case 3:
      return 'Complete the test'
    default:
      return 'Unknown stepIndex'
  }
}

export default function HorizontalLabelPositionBelowStepper () {
  const classes = useStyles()
  const [activeStep, setActiveStep] = React.useState(0)
  const steps = getSteps()

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1)
  }

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1)
  }

  const handleReset = () => {
    setActiveStep(0)
  }

  return (
    <div className={classes.root}>
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <div>
        {activeStep === steps.length ? (
          <div>
            <Typography className={classes.instructions}>You have completed running the tests</Typography>
            <Button onClick={handleReset}>Reset</Button>
          </div>
        ) : (
          <div>
            <Typography className={classes.instructions}>{getStepContent(activeStep)}</Typography>
            <div>
              <Button
                disabled={activeStep === 0}
                onClick={handleBack}
                className={classes.backButton}
              >
                Back
              </Button>
              <Button variant="contained" color="primary" onClick={handleNext}>
                {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
