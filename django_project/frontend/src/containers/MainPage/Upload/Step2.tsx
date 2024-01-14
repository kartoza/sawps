import React, { useState } from 'react';
import {v4 as uuidv4} from 'uuid';
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import HelpOutlineOutlinedIcon from '@mui/icons-material/HelpOutlineOutlined';
import LightTooltip from '../../../components/LightTooltip';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { 
    toggleParcelSelectionMode,
    toggleParcelSelectedState,
    triggerMapEvent,
    toggleDigitiseSelectionMode
} from '../../../reducers/MapState';
import {RootState} from '../../../app/store';
import {postData} from "../../../utils/Requests";
import AlertMessage from '../../../components/AlertMessage';
import PropertyInterface from '../../../models/Property';
import { MapSelectionMode, MapEvents } from "../../../models/Map";
import SelectedParcelTable from './SelectedParcelTable';
import ParcelInterface from '../../../models/Parcel';
import Uploader from './Uploader';

const CREATE_NEW_PROPERTY_URL = '/api/property/create/'
const PROPERTY_UPDATE_BOUNDARIES_URL = '/api/property/boundaries/update/'

interface Step2Interface {
    property: PropertyInterface;
    onSave: (data: PropertyInterface) => void;
}

export default function Step2(props: Step2Interface) {
    const dispatch = useAppDispatch()
    const mapSelectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)
    const selectedParcels = useAppSelector((state: RootState) => state.mapState.selectedParcels)
    const uploadMode = useAppSelector((state: RootState) => state.uploadState.uploadMode)
    const [savingProperty, setSavingProperty] = useState(false)
    const [alertMessage, setAlertMessage] = useState<string>('')
    const [openUploader, setOpenUploader] = useState(false)
    const [boundarySearchSession, setBoundarySearchSession] = useState<string>('')

    const saveProperty = () => {
        if (selectedParcels.length === 0) {
            setAlertMessage('Error! Please select at least 1 parcel!')
            return
        }
        setSavingProperty(true)
        let _data:PropertyInterface = {
            ...props.property,
            parcels: selectedParcels
        }
        if (boundarySearchSession) {
            _data['boundary_search_session'] = boundarySearchSession
        }
        let _url = CREATE_NEW_PROPERTY_URL
        if (props.property.id) {
            _url = PROPERTY_UPDATE_BOUNDARIES_URL
        }
        postData(`${_url}`, _data).then(
            response => {
                setSavingProperty(false)
                // reset parcel selection mode
                dispatch(toggleParcelSelectionMode(uploadMode))
                // trigger event to refresh properties layer
                dispatch(triggerMapEvent({
                    'id': uuidv4(),
                    'name': MapEvents.REFRESH_PROPERTIES_LAYER,
                    'date': Date.now()
                }))
                // trigger to next step
                props.onSave({...props.property, ...response.data})
            }
        ).catch(error => {
            setSavingProperty(false)
            console.log('error ', error)
            if (error.response) {
                alert(`Error saving property: ${error.response.data}!`)
            } else {
                alert(`Error saving property!`)
            }
        })    
    }

    return (
        <Grid container className='UploadSection Step2' rowGap={2}>
            <Grid item className='UploadSectionHeader'>
                <span className='UploadSectionHeaderIcon Boundary'></span>
                <span>Create Property Boundary</span>
                <LightTooltip title='Create your property boundary by either selecting the cadastral parcels that make up the property or manually digitising your property boundary using the tools below'>
                    <HelpOutlineOutlinedIcon fontSize='small' className='UploadSectionHelpIcon' />
                </LightTooltip>
            </Grid>
            <Grid item className='UploadSectionContent' sx={{flex: 1}}>
                <Grid container flexDirection={'column'} className='SelectedParcelContainerParent'>
                    <Grid item className='SelectedParcelContainer'>
                        <SelectedParcelTable parcels={selectedParcels}
                            onRemoveParcel={(parcel: ParcelInterface) => {
                                dispatch(toggleParcelSelectedState(parcel))
                                dispatch(triggerMapEvent({
                                    'id': uuidv4(),
                                    'name': MapEvents.HIGHLIGHT_SELECTED_PARCEL,
                                    'date': Date.now(),
                                    'payload': []
                                }))
                            }}
                            onParcelHovered={(parcel: ParcelInterface) => {
                                if (parcel) {
                                    dispatch(triggerMapEvent({
                                        'id': uuidv4(),
                                        'name': MapEvents.HIGHLIGHT_SELECTED_PARCEL,
                                        'date': Date.now(),
                                        'payload': [parcel.id, parcel.layer]
                                    }))
                                } else {
                                    dispatch(triggerMapEvent({
                                        'id': uuidv4(),
                                        'name': MapEvents.HIGHLIGHT_SELECTED_PARCEL,
                                        'date': Date.now(),
                                        'payload': []
                                    }))
                                }
                            }}
                        />
                    </Grid>
                </Grid>
            </Grid>
            <Grid item className='UploadSectionContent'>
                <Grid container flexDirection={'column'}>
                    <Grid item>
                        <Grid container flexDirection={'column'} flexWrap={'nowrap'} rowGap={2} className='ButtonContainer'>
                            <Grid item>
                                <Grid container flexDirection={'row'} flexWrap={'wrap'} justifyContent={'space-between'}>
                                    { mapSelectionMode === MapSelectionMode.Parcel ? 
                                        <Button variant='contained' className='Select' onClick={() => dispatch(toggleParcelSelectionMode(uploadMode)) }>CANCEL</Button> :
                                        <Button variant='contained' className='Select' disabled={mapSelectionMode === MapSelectionMode.Digitise} onClick={() => dispatch(toggleParcelSelectionMode(uploadMode)) }>SELECT</Button>
                                    } 
                                    <Button variant='contained' className='Digitise' disabled={mapSelectionMode === MapSelectionMode.Parcel} onClick={() => dispatch(toggleDigitiseSelectionMode()) }>DIGITISE</Button>
                                    <Button variant='contained' className='Upload' disabled={mapSelectionMode === MapSelectionMode.Digitise || mapSelectionMode === MapSelectionMode.Parcel} onClick={() => setOpenUploader(true)}>UPLOAD</Button>
                                </Grid>
                            </Grid>
                            <Grid item>
                                { savingProperty ? (
                                    <Button variant='contained' className='Save' disabled={savingProperty}><CircularProgress size={16} sx={{marginRight: '5px' }}/> SAVING BOUNDARY...</Button>
                                ) : (
                                    <Button variant='contained' className='Save' disabled={savingProperty} onClick={saveProperty}>SAVE BOUNDARY</Button>
                                )}
                            </Grid>
                        </Grid>
                    </Grid>        
                    <Grid item>
                        <AlertMessage message={alertMessage} onClose={() => setAlertMessage('')} />
                        <Uploader open={openUploader} onClose={() => setOpenUploader(false)} onErrorMessage={(error: string) => setAlertMessage(error)}
                         onSuccessBoundarySearch={(session: string) => setBoundarySearchSession(session)} />
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}
