import React, { useState } from 'react';
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { toggleParcelSelectionMode } from '../../../reducers/MapState';
import {RootState} from '../../../app/store';
import {postData} from "../../../utils/Requests";
import AlertMessage from '../../../components/AlertMessage';
import PropertyInterface from '../../../models/Property';

const CREATE_NEW_PROPERTY_URL = '/api/property/create/'

interface Step2Interface {
    property: PropertyInterface;
    onSave: (data: PropertyInterface) => void;
}

export default function Step2(props: Step2Interface) {
    const dispatch = useAppDispatch()
    const mapSelectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)
    const selectedParcels = useAppSelector((state: RootState) => state.mapState.selectedParcels)
    const [savingProperty, setSavingProperty] = useState(false)
    const [alertMessage, setAlertMessage] = useState<string>('')

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
        postData(`${CREATE_NEW_PROPERTY_URL}`, _data).then(
            response => {
                setSavingProperty(false)
                // reset parcel selection mode
                dispatch(toggleParcelSelectionMode())
                // trigger to next step
                props.onSave({...props.property, id:response.data['id']})
            }
          ).catch(error => {
            setSavingProperty(false)
            console.log('error ', error)
            alert('Error saving property...')
          })
    }

    return (
        <Grid container className='UploadSection Step2'>
            <Grid item>
                <AlertMessage message={alertMessage} onClose={() => setAlertMessage('')} />
            </Grid>
            <Grid item className='UploadSectionHeader'>
                <span className='UploadSectionHeaderIcon Boundary'></span>
                <span>Create Property Boundary</span>
            </Grid>
            <Grid item className='UploadSectionContent CreateBoundary'>
                <Grid container flexDirection={'column'}>
                    <Grid item>
                        <p>
                            Create your property boundary by either selecting the cadastral parcels that make up the property or
                            manually digitising your property boundary using the tools below
                        </p>
                    </Grid>
                    <Grid item>
                        <Grid container flexDirection={'column'} flexWrap={'nowrap'} spacing={2} rowGap={2} className='ButtonContainer'>
                            { mapSelectionMode === 'parcel' ? 
                                <Button variant='contained' onClick={() => dispatch(toggleParcelSelectionMode()) } sx={{ background: '#FAA755' }} >CANCEL</Button> :
                                <Button variant='contained' onClick={() => dispatch(toggleParcelSelectionMode()) } sx={{ background: '#FAA755' }}>SELECT</Button>
                            } 
                            <Button variant='contained' sx={{ background: '#9D85BE' }}>DIGITISE</Button>
                            <Button variant='contained' sx={{ background: 'rgba(40, 40, 41, 0.8)' }}>UPLOAD</Button>
                            { savingProperty ? (
                                <Button variant='contained' disabled={savingProperty}><CircularProgress size={16} sx={{marginRight: '5px' }}/> SAVING BOUNDARY...</Button>
                            ) : (
                                <Button variant='contained' disabled={savingProperty} onClick={saveProperty}>SAVE BOUNDARY</Button>
                            )}
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}
