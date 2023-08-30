import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import {
    GridRowId 
} from '@mui/x-data-grid';
import {
    UploadSpeciesDetailInterface,
    getDefaultUploadSpeciesDetail,
    AnnualPopulationPerActivityInterface,
    CommonUploadMetadata,
    AnnualPopulationPerActivityValidation,
    AnnualPopulationPerActivityErrorMessage
} from '../../../models/Upload';
import EventDetailForm, {EventType} from './EventDetailForm';
import ActivityDataTable from './ActivityDataTable';

interface ActivityDetailInterface {
    initialData: UploadSpeciesDetailInterface;
    intakeEventMetadataList: CommonUploadMetadata[];
    offtakeEventMetadataList: CommonUploadMetadata[];
    setIsDirty: (isDirty: boolean) => void;
    handleBack: (data: UploadSpeciesDetailInterface) => void;
    handleNext: (data: UploadSpeciesDetailInterface) => void;
    handleSaveDraft: (data: UploadSpeciesDetailInterface) => void;    
}

export default function ActivityDetail(props: ActivityDetailInterface) {
    const {
        initialData, intakeEventMetadataList, offtakeEventMetadataList,
        setIsDirty, handleBack, handleNext, handleSaveDraft
    } = props
    const [data, setData] = useState<UploadSpeciesDetailInterface>(getDefaultUploadSpeciesDetail(0))
    const [selectedIntakeActivity, setSelectedIntakeActivity] = useState<AnnualPopulationPerActivityInterface>(null)
    const [selectedOfftakeActivity, setSelectedOfftakeActivity] = useState<AnnualPopulationPerActivityInterface>(null)

    const handleEditRow = (id: GridRowId, eventType: EventType) => {
        if (eventType === EventType.intake) {
            if (selectedIntakeActivity && selectedIntakeActivity.id === id) {
                // toggle edit
                setSelectedIntakeActivity(null)
            } else {
                let _row = data.intake_populations.find((row) => row.id === id)
                if (_row) {
                    setSelectedIntakeActivity(_row)
                } else {
                    setSelectedIntakeActivity(null)
                }
            }
        } else {
            if (selectedOfftakeActivity && selectedOfftakeActivity.id === id) {
                // toggle edit
                setSelectedOfftakeActivity(null)
            } else {
                let _row = data.offtake_populations.find((row) => row.id === id)
                if (_row) {
                    setSelectedOfftakeActivity(_row)
                } else {
                    setSelectedOfftakeActivity(null)
                }
            }
        }
    }

    const handleDeleteRow = (id: GridRowId, eventType: EventType) => {
        if (eventType === EventType.intake) {
            if (selectedIntakeActivity && selectedIntakeActivity.id === id) {
                setSelectedIntakeActivity(null)
            }
            setData({
                ...data,
                intake_populations: data.intake_populations.filter((row) => row.id !== id)
            })
        } else {
            if (selectedOfftakeActivity && selectedOfftakeActivity.id === id) {
                setSelectedOfftakeActivity(null)
            }
            setData({
                ...data,
                offtake_populations: data.offtake_populations.filter((row) => row.id !== id)
            })
        }
    }

    const validateIntakeActivity = (activity: AnnualPopulationPerActivityInterface) => {
        let _error_validation:AnnualPopulationPerActivityValidation = {}
        let _error_messages:AnnualPopulationPerActivityErrorMessage = {}
        if (activity.activity_type_id === 0) {
            _error_validation = {
                ..._error_validation,
                activity_type_id: true
            }
        } else {
            // validate if selected activity has not been added yet
            let _exist = data.intake_populations.find((element) => element.activity_type_id === activity.activity_type_id && element.id !== activity.id)
            if (_exist) {
                _error_validation = {
                    ..._error_validation,
                    activity_type_id: true
                }
                _error_messages = {
                    ..._error_messages,
                    activity_type_id: `Event ${activity.activity_type_name} has been selected!`
                }
            }
        }
        if (!activity.reintroduction_source || activity.reintroduction_source.trim() === '') {
            _error_validation = {
                ..._error_validation,
                reintroduction_source: true
            }
        }
        return [_error_validation, _error_messages] as [AnnualPopulationPerActivityValidation, AnnualPopulationPerActivityErrorMessage]
    }

    const validateOfftakeActivity = (activity: AnnualPopulationPerActivityInterface) => {
        let _error_validation:AnnualPopulationPerActivityValidation = {}
        let _error_messages:AnnualPopulationPerActivityErrorMessage = {}
        if (activity.activity_type_id === 0) {
            _error_validation = {
                ..._error_validation,
                activity_type_id: true
            }
        } else {
            // validate if selected activity has not been added yet
            let _exist = data.offtake_populations.find((element) => element.activity_type_id === activity.activity_type_id && element.id !== activity.id)
            if (_exist) {
                _error_validation = {
                    ..._error_validation,
                    activity_type_id: true
                }
                _error_messages = {
                    ..._error_messages,
                    activity_type_id: `Event ${activity.activity_type_name} has been selected! Please select other event!`
                }
            }
        }
        return [_error_validation, _error_messages] as [AnnualPopulationPerActivityValidation, AnnualPopulationPerActivityErrorMessage]
    }

    useEffect(() => {
        setData({
            ...initialData,
            annual_population: {...initialData.annual_population},
            intake_populations: initialData.intake_populations.map((element, idx) => {
                element.id = idx
                return element
            }),
            offtake_populations: initialData.offtake_populations.map((element, idx) => {
                element.id = idx
                return element
            })
        })
    }, [initialData])

    return (
        <Grid container flexDirection={'column'} rowSpacing={2}>
            <Grid item>
                <Grid container flexDirection={'row'} spacing={4}>
                    <Grid item xs={12} md={6}>
                        <Grid container flexDirection={'column'} rowSpacing={1}>
                            <Grid item>
                                <Typography variant='h6'>Introduction/Reintroduction</Typography>
                            </Grid>
                            <Grid item>
                                <ActivityDataTable data={data.intake_populations} eventType={EventType.intake} isReadOnly={false}
                                handleDeleteRow={handleDeleteRow} handleEditRow={handleEditRow} />
                            </Grid>
                            <Grid item>
                                <EventDetailForm initialData={selectedIntakeActivity} eventMetadataList={intakeEventMetadataList} eventType={EventType.intake}
                                   setIsDirty={setIsDirty} validate={validateIntakeActivity} onSave={(isCreate: boolean, activity: AnnualPopulationPerActivityInterface, isCancel?: boolean) => {
                                    if (isCancel) {
                                        setSelectedIntakeActivity(null)
                                        return;
                                    }
                                    if (isCreate) {
                                        activity.id = data.intake_populations.length ? data.intake_populations[data.intake_populations.length - 1].id + 1 : 0
                                        setData({
                                            ...data,
                                            intake_populations: [...data.intake_populations, activity]
                                        })
                                    } else {
                                        setData({
                                            ...data,
                                            intake_populations: data.intake_populations.map((element) => {
                                                return element.id === activity.id ? activity : element
                                            })
                                        })
                                        setSelectedIntakeActivity(null)
                                    }
                                   }} />
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <Grid container flexDirection={'column'} rowSpacing={1}>
                            <Grid item>
                                <Typography variant='h6'>Off-take</Typography>
                            </Grid>
                            <Grid item>
                                <ActivityDataTable data={data.offtake_populations} eventType={EventType.offtake} isReadOnly={false}
                                    handleDeleteRow={handleDeleteRow} handleEditRow={handleEditRow} />
                            </Grid>
                            <Grid item>
                                <EventDetailForm initialData={selectedOfftakeActivity} eventMetadataList={offtakeEventMetadataList} eventType={EventType.offtake}
                                   setIsDirty={setIsDirty} validate={validateOfftakeActivity} onSave={(isCreate: boolean, activity: AnnualPopulationPerActivityInterface, isCancel?: boolean) =>{
                                    if (isCancel) {
                                        setSelectedOfftakeActivity(null)
                                        return;
                                    }
                                    if (isCreate) {
                                        activity.id = data.offtake_populations.length ? data.offtake_populations[data.offtake_populations.length - 1].id + 1 : 0
                                        setData({
                                            ...data,
                                            offtake_populations: [...data.offtake_populations, activity]
                                        })
                                    } else {
                                        setData({
                                            ...data,
                                            offtake_populations: data.offtake_populations.map((element) => {
                                                return element.id === activity.id ? activity : element
                                            })
                                        })
                                        setSelectedOfftakeActivity(null)
                                    }
                                   }} />
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            <Grid item container flexDirection={'row'} justifyContent={'space-between'}>
                <Grid item>
                    <Button variant='outlined' onClick={() => {
                        handleSaveDraft(data)
                    }}>SAVE DRAFT</Button>
                </Grid>
                <Grid item>
                    <Grid container flexDirection={'row'} justifyContent={'flex-end'} columnSpacing={2}>
                        <Grid item>
                            <Button variant='outlined' onClick={() => handleBack(data)}>BACK</Button>
                        </Grid>
                        <Grid item>
                            <Button variant='contained' onClick={() => {
                                handleNext(data)
                            }}>NEXT</Button>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}