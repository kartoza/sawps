import React, { useState, useEffect, useCallback } from 'react';
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepButton from '@mui/material/StepButton';
import TabPanel from '../../../components/TabPanel';
import {UploadSpeciesDetailInterface, getDefaultUploadSpeciesDetail} from '../../../models/Upload'
import './index.scss';
import PropertyInterface from '../../../models/Property';
import SpeciesDetail from './SpeciesDetail';
import ActivityDetail from './ActivityDetail';
import ReviewAndConfirm from './ReviewAndConfirm';
import ConfirmationAlertDialog from '../../../components/ConfirmationAlertDialog';
import FeedbackAlertDialog, {AlertType} from '../../../components/FeedbackAlertDialog';

interface FormWizardInterface {
    propertyItem: PropertyInterface;
}

const steps = ['SPECIES DETAIL', 'ACTIVITY DETAIL', 'REVIEW & SUBMIT']

function FormWizard(props: FormWizardInterface) {
    const [loading, setLoading] = useState<boolean>(false)
    const [uploadSession, setUploadSession] = useState<string>('')
    const [isDirty, setIsDirty] = useState(false)
    const [data, setData] = useState<UploadSpeciesDetailInterface>(getDefaultUploadSpeciesDetail(props.propertyItem.id))
    const [activeStep, setActiveStep] = React.useState(0);
    const [completed, setCompleted] = React.useState<{
        [k: number]: boolean
    }>({})
    const [confirmationOpen, setConfirmationOpen] = useState(false)
    const [navigateTo, setNavigateTo] = useState<number>(-1)
    const [feedbackAlertDialog, setFeedbackAlertDialog] = useState<AlertType>(AlertType.none)
    const [feedbackAlertDesc, setFeedbackAlertDesc] = useState<string>('')

    const totalSteps = () => {
        return steps.length
    }

    const completedSteps = () => {
        return Object.keys(completed).length
    }

    const isLastStep = () => {
        return activeStep === totalSteps() - 1
    }

    const allStepsCompleted = () => {
        return completedSteps() === totalSteps()
    }

    const handleNext = () => {
        const newActiveStep =
        isLastStep() && !allStepsCompleted()
            ? // It's the last step, but not all steps have been completed,
            // find the first step that has been completed
            steps.findIndex((step, i) => !(i in completed))
            : activeStep + 1
        setActiveStep(newActiveStep)
    }

    const handleBack = () => {
        if (isDirty) {
            setNavigateTo(activeStep - 1)
            setConfirmationOpen(true)
        } else {
            setActiveStep((prevActiveStep) => prevActiveStep - 1)
        }
    }

    const handleStep = (step: number) => {
        if (isDirty) {
            setNavigateTo(step)
            setConfirmationOpen(true)
        } else {
            setActiveStep(step)
        }
    }

    const onFormSave = (index: number, formData: UploadSpeciesDetailInterface) => {
        setCompleted({
            ...completed,
            [index]: true
        })
        setData({
            ...formData,
            annual_population: {...formData.annual_population},
            intake_population: {...formData.intake_population},
            offtake_population: {...formData.offtake_population}
        })
        handleNext()
    }

    const onFormBack = (index: number, formData: UploadSpeciesDetailInterface) => {
        handleBack()
    }

    useEffect(() => {
        setIsDirty(false)
    }, [activeStep])

    /* Check Unsaved Changes */
    useEffect(() => {
        window.addEventListener("beforeunload", alertUserUnsavedChanges)
        return () => {
          window.removeEventListener("beforeunload", alertUserUnsavedChanges)
        }
    }, [isDirty])

    const alertUserUnsavedChanges = useCallback((e:any) => {
        if (isDirty) {
            e.preventDefault()
            e.returnValue = ""
        }
    }, [isDirty])

    const handleUnsavedChangesConfirmationClose = () => {
        setConfirmationOpen(false)
        setNavigateTo(-1)
    }

    const handleUnsavedChangesConfirmationOk = () => {
        setActiveStep(navigateTo)
        handleUnsavedChangesConfirmationClose()
    }
    /* End of Check Unsaved Changes */

    const handleSubmit = () => {
        setLoading(true)
        setTimeout(() => {
            setLoading(false)
            setFeedbackAlertDialog(AlertType.success)
            setFeedbackAlertDesc('Your data has been successfully saved!')
        }, 2000)
    }

    return (
        <Grid container className='OnlineFormWizard' flexDirection={'column'}>
            <Box className='TabHeaders'>
                <Stepper nonLinear activeStep={activeStep}>
                    {steps.map((label, index) => (
                    <Step key={label} disabled={loading || (index > activeStep && !completed[index])} completed={completed[index]}>
                        <StepButton color="inherit" onClick={() => handleStep(index)} className={activeStep === index && isDirty ? 'form-dirty' : ''}>
                            {label}
                        </StepButton>
                    </Step>
                    ))}
                </Stepper>
            </Box>
            <Box className='TabPanels FlexContainerFill'>
                <Box className='OnlineFormWizardContent'>
                    <TabPanel key={0} value={activeStep} index={0} noPadding>
                        <SpeciesDetail initialData={data} setIsDirty={setIsDirty} handleNext={(formData)=>onFormSave(0, formData)} />
                    </TabPanel>
                    <TabPanel key={1} value={activeStep} index={1} noPadding>
                        <ActivityDetail initialData={data} setIsDirty={setIsDirty} handleNext={(formData)=>onFormSave(1, formData)}
                            handleBack={(formData) => onFormBack(1, formData)} />
                    </TabPanel>
                    <TabPanel key={2} value={activeStep} index={2} noPadding>
                        <ReviewAndConfirm initialData={data} handleStepChange={(newStep: number) => handleStep(newStep)}
                            handleBack={(formData) => onFormBack(2, formData)}
                            handleSubmit={handleSubmit} loading={loading} />
                    </TabPanel>
                </Box>
            </Box>
            <Grid item>
                <ConfirmationAlertDialog open={confirmationOpen} alertClosed={handleUnsavedChangesConfirmationClose}
                    alertConfirmed={handleUnsavedChangesConfirmationOk}
                    alertDialogTitle={'Unsaved changes'}
                    alertDialogDescription={'You have unsaved changes. Are you sure to leave this page?'}
                    confirmButtonText='Leave'
                    confirmButtonProps={{color: 'error', autoFocus: true}}
                />
            </Grid>
            <Grid item>
                <FeedbackAlertDialog type={feedbackAlertDialog} alertDialogTitle='Upload Species Data'
                    alertDialogDescription={feedbackAlertDesc} alertClosed={() => {
                        setFeedbackAlertDialog(AlertType.none)
                        window.location.replace(window.location.origin + '/map/?tab=1')
                    }} />
            </Grid>
        </Grid>
    )
}

export default FormWizard;