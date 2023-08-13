import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import {
    DataGrid,
    GridColDef,
    GridValueGetterParams,
    GridActionsCellItem,
    GridRowId 
} from '@mui/x-data-grid';
import {
    UploadSpeciesDetailInterface,
    getDefaultUploadSpeciesDetail,
    AnnualPopulationPerActivityInterface,
    CommonUploadMetadata,
    AnnualPopulationPerActivityValidation
} from '../../../models/Upload';
import EventDetailForm, {EventType} from './EventDetailForm';

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
    const IntakeColumns: GridColDef[] = [
        {
            field: 'activity_type_name',
            headerName: 'Activity',
            flex: 1,
        },
        {
            field: 'total',
            headerName: 'Total',
            flex: 1,
        },
        {
            field: 'reintroduction_source',
            headerName: 'Source',
            flex: 1,
        },
        {
            field: 'actions',
            type: 'actions',
            getActions: ({ id }) => [
                <GridActionsCellItem
                    icon={<EditIcon />}
                    label="Edit"
                    onClick={() => handleEditRow(id, EventType.intake)}
                />,
                <GridActionsCellItem
                    icon={<DeleteIcon />}
                    label="Delete"
                    onClick={() => handleDeleteRow(id, EventType.intake)}
                />,
            ]
        }
    ]
    const OfftakeColumns: GridColDef[] = [
        {
            field: 'activity_type_name',
            headerName: 'Activity',
            flex: 1,
        },
        {
            field: 'total',
            headerName: 'Total',
            flex: 1,
        },
        {
            field: 'translocation_destination',
            headerName: 'Destination',
            flex: 1,
        },
        {
            field: 'actions',
            type: 'actions',
            getActions: ({ id }) => [
                <GridActionsCellItem
                    icon={<EditIcon />}
                    label="Edit"
                    onClick={() => handleEditRow(id, EventType.offtake)}
                />,
                <GridActionsCellItem
                    icon={<DeleteIcon />}
                    label="Delete"
                    onClick={() => handleDeleteRow(id, EventType.offtake)}
                />,
            ]
        }
    ]

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
        if (activity.activity_type_id === 0) {
            _error_validation = {
                ..._error_validation,
                activity_type_id: true
            }
        }
        if (!activity.reintroduction_source || activity.reintroduction_source.trim() === '') {
            _error_validation = {
                ..._error_validation,
                reintroduction_source: true
            }
        }
        return _error_validation
    }

    const validateOfftakeActivity = (activity: AnnualPopulationPerActivityInterface) => {
        let _error_validation:AnnualPopulationPerActivityValidation = {}
        if (activity.activity_type_id === 0) {
            _error_validation = {
                ..._error_validation,
                activity_type_id: true
            }
        }
        if (!activity.translocation_destination || activity.translocation_destination.trim() === '') {
            _error_validation = {
                ..._error_validation,
                translocation_destination: true
            }
        }
        return _error_validation
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
                            <Grid item className={'ActivityTable' + (data.intake_populations.length === 0 ? ' EmptyRows' : '')}>
                                <DataGrid columns={IntakeColumns} rows={data.intake_populations} autoHeight
                                    />
                            </Grid>
                            <Grid item>
                                <EventDetailForm initialData={selectedIntakeActivity} eventMetadataList={intakeEventMetadataList} eventType={EventType.intake}
                                   setIsDirty={setIsDirty} validate={validateIntakeActivity} onSave={(isCreate: boolean, activity: AnnualPopulationPerActivityInterface, isCancel?: boolean) =>{
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
                            <Grid item className={'ActivityTable' + (data.offtake_populations.length === 0 ? ' EmptyRows' : '')}>
                                <DataGrid columns={OfftakeColumns} rows={data.offtake_populations} autoHeight />
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