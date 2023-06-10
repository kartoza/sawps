import React, { useState } from 'react';
import Grid from "@mui/material/Grid";
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import InputAdornment from "@mui/material/InputAdornment";
import SearchIcon from '@mui/icons-material/Search';
import CircularProgress from "@mui/material/CircularProgress";
import {RootState} from '../../../app/store';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { toggleParcelSelectionMode } from '../../../reducers/MapState';
import { createNewProperty } from '../../../models/Property';
import { PropertyInfo } from '../Property';
import PropertyInterface, {PropertyValidation} from '../../../models/Property';
import {postData} from "../../../utils/Requests";
import AlertMessage from '../../../components/AlertMessage';

import './index.scss';

const CREATE_NEW_PROPERTY_URL = '/api/property/create/'

function Upload() {
    const dispatch = useAppDispatch()
    const mapSelectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)
    const selectedParcels = useAppSelector((state: RootState) => state.mapState.selectedParcels)
    const [property, setProperty] = useState(createNewProperty())
    const [isEnablePropertyForm, setIsEnablePropertyForm] = useState(true)
    const [savingProperty, setSavingProperty] = useState(false)
    const [alertMessage, setAlertMessage] = useState<string>('')
    const [propertyValidation, setPropertyValidation] = useState<PropertyValidation>({})

    const saveProperty = () => {
        let _error_messages = []
        let _error_validation = {}
        if (selectedParcels.length === 0) {
            _error_messages.push('Error! Please select at least 1 parcel!')
        }
        if (property.name.trim() === '') {
            _error_messages.push('Error! Property name is mandatory!')
            _error_validation = { ..._error_validation, name: true }
        }
        if (property.property_type.trim() === '') {
            _error_messages.push('Error! Property type is mandatory!')
            _error_validation = { ..._error_validation, property_type: true }
        }
        if (property.province.trim() === '') {
            _error_messages.push('Error! Province is mandatory!')
            _error_validation = { ..._error_validation, province: true }
        }
        if (property.organisation.trim() === '') {
            _error_messages.push('Error! Organisation is mandatory!')
            _error_validation = { ..._error_validation, organisation: true }
        }
        if (_error_messages.length && !_error_validation) {
            setAlertMessage(_error_messages[0])
            return
        } else if (_error_messages.length === 1 && _error_validation) {
            setAlertMessage(_error_messages[0])
            setPropertyValidation(_error_validation)
            return
        } else if (_error_messages.length > 1 && _error_validation) {
            setAlertMessage('Error! Please fill in mandatory input!')
            setPropertyValidation(_error_validation)
            return
        }
        setSavingProperty(true)
        let _data:PropertyInterface = {
            ...property,
            name: property.name.trim(),
            owner_email: property.owner_email ? property.owner_email.trim() : '',
            parcels: selectedParcels
        }
        postData(`${CREATE_NEW_PROPERTY_URL}`, _data).then(
            response => {
                setSavingProperty(false)
                setAlertMessage('Successfully adding new property!')
                // reset parcel selection mode
                dispatch(toggleParcelSelectionMode())
            }
          ).catch(error => {
            setSavingProperty(false)
            console.log('error ', error)
            alert('Error saving new property...')
          })
    }

    return (
        <Grid container flexDirection={'column'} className='Upload'>
            <AlertMessage message={alertMessage} onClose={() => setAlertMessage('')} />
            <Grid item className='Header'>
                DATA UPLOAD
            </Grid>
            <Grid item>
                <Grid container className='UploadContainer'>
                    <Grid item>
                        <FormControl className='SearchArea' variant="outlined">
                            <InputLabel htmlFor="search-area">Search area</InputLabel>
                            <OutlinedInput
                                id="search-area"
                                type={'text'}
                                endAdornment={
                                    <InputAdornment position="end">
                                        <IconButton
                                        aria-label="search"
                                        edge="end"
                                        >
                                        <SearchIcon />
                                        </IconButton>
                                    </InputAdornment>
                                }
                                label="Password"
                            />
                        </FormControl>
                    </Grid>
                    <Grid item>
                        <Grid container className='UploadContent'>
                            <Grid item>
                                Select Property
                            </Grid>
                            <Grid item>
                                <Grid container className='UploadSection'>
                                    <Grid item className='UploadSectionHeader'>
                                        <span className='UploadSectionHeaderIcon Boundary'></span>
                                        <span>Create Property Boundary/Update</span>
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
                                                <Grid container flexDirection={'row'} flexWrap={'wrap'} spacing={1} rowGap={1} justifyContent={'space-evenly'}>
                                                    { mapSelectionMode === 'parcel' ? 
                                                        <Button variant='contained' onClick={() => dispatch(toggleParcelSelectionMode()) }>CANCEL</Button> :
                                                        <Button variant='contained' onClick={() => dispatch(toggleParcelSelectionMode()) }>SELECT</Button>
                                                    } 
                                                    <Button variant='contained'>DIGITISE</Button>
                                                    <Button variant='contained'>UPLOAD</Button>
                                                    { savingProperty ? (
                                                        <Button variant='contained' disabled={savingProperty}><CircularProgress size={16} sx={{marginRight: '5px' }}/> SAVING PROPERTY...</Button>
                                                    ) : (
                                                        <Button variant='contained' disabled={savingProperty} onClick={saveProperty}>SAVE PROPERTY</Button>
                                                    )}
                                                </Grid>
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item>
                                <Grid container className='UploadSection'>
                                    <Grid item className='UploadSectionHeader'>
                                        <span className='UploadSectionHeaderIcon Property'></span>
                                        <span>Property Information</span>
                                    </Grid>
                                    <Grid item className='UploadSectionContent Property'>
                                        <Grid container flexDirection={'column'}>
                                            <Grid item>
                                                <p>
                                                    Please add the properties name all associated information is auto-generated by the system
                                                </p>
                                            </Grid>
                                            <Grid item>
                                                <PropertyInfo property={property} enableForm={isEnablePropertyForm && !savingProperty} onUpdated={(data, validation) => { setProperty(data); setPropertyValidation({...propertyValidation, ...validation}); }} validationError={propertyValidation} />
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item>
                                <Grid container className='UploadSection'>
                                    <Grid item className='UploadSectionHeader'>
                                        <span className='UploadSectionHeaderIcon Population'></span>
                                        <span>Population Data</span>
                                    </Grid>
                                    <Grid item className='UploadSectionContent'>
                                        
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item>
                                Save Button
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}


export default Upload;
