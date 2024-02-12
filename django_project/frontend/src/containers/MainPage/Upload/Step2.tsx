import React, { useState } from 'react';
import {v4 as uuidv4} from 'uuid';
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import HelpOutlineOutlinedIcon from '@mui/icons-material/HelpOutlineOutlined';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import LightTooltip from '../../../components/LightTooltip';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { 
    toggleParcelSelectionMode,
    toggleParcelSelectedState,
    triggerMapEvent,
    toggleDigitiseSelectionMode,
    setSelectedParcels
} from '../../../reducers/MapState';
import {RootState} from '../../../app/store';
import {postData} from "../../../utils/Requests";
import AlertMessage from '../../../components/AlertMessage';
import PropertyInterface, {BoundarySearchResultInterface, BOUNDARY_FILE_SOURCE_TYPE} from '../../../models/Property';
import { MapSelectionMode, MapEvents } from "../../../models/Map";
import SelectedParcelTable from './SelectedParcelTable';
import ParcelInterface from '../../../models/Parcel';
import Uploader from './Uploader';

const CREATE_NEW_PROPERTY_URL = '/api/property/create/'
const PROPERTY_UPDATE_BOUNDARIES_URL = '/api/property/boundaries/update/'

interface Step2Interface {
    property: PropertyInterface;
    onSave: (data: PropertyInterface) => void;
    onBoundaryPropertyUpdated: (source: string) => void;
}

interface UploadedBoundarySummaryInterface {
    upload_file_names?: string[],
    property_size_ha: number,
    province: string
}


function UploadedBoundarySummary(props: UploadedBoundarySummaryInterface) {
    return (
        <TableContainer component={Paper}>
            <Table className='UploadedBoundaryTable' aria-label="uploaded boundary summary" size='small'>
                <colgroup>
                    <col width="50%" />
                    <col width="50%" />
                </colgroup>
                <TableHead>
                    <TableRow>
                        <TableCell>Boundary Information</TableCell>
                        <TableCell>Data</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    { props.upload_file_names &&
                        <TableRow key='upload_file_names'>
                            <TableCell component="th" scope="row">
                                Files
                            </TableCell>
                            <TableCell className='TableCellText'>
                                <span>{props.upload_file_names.join(',')}</span>
                            </TableCell>
                        </TableRow>
                    }
                    <TableRow key='size'>
                        <TableCell component="th" scope="row">
                            Boundary Size
                        </TableCell>
                        <TableCell className='TableCellText'>
                            <span>{props.property_size_ha.toFixed(2)} ha</span>                                
                        </TableCell>
                    </TableRow>
                    <TableRow key='province'>
                        <TableCell component="th" scope="row">
                            Province
                        </TableCell>
                        <TableCell className='TableCellText'>
                            <span>{props.province}</span>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
    )
}


export default function Step2(props: Step2Interface) {
    const dispatch = useAppDispatch()
    const mapSelectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)
    const selectedParcels = useAppSelector((state: RootState) => state.mapState.selectedParcels)
    const uploadMode = useAppSelector((state: RootState) => state.uploadState.uploadMode)
    const [savingProperty, setSavingProperty] = useState(false)
    const [alertMessage, setAlertMessage] = useState<string>('')
    const [openUploader, setOpenUploader] = useState(false)
    const [boundarySearchData, setBoundarySearchData] = useState<BoundarySearchResultInterface>(null)

    const saveProperty = () => {
        if (selectedParcels.length === 0 && boundarySearchData === null) {
            setAlertMessage('Error! Please upload boundary file or select at least 1 parcel!')
            return
        }
        setSavingProperty(true)
        let _data:PropertyInterface = {
            ...props.property,
            parcels: selectedParcels
        }
        if (boundarySearchData) {
            _data['boundary_search_session'] = boundarySearchData.session
        }
        let _url = CREATE_NEW_PROPERTY_URL
        if (props.property.id) {
            _url = PROPERTY_UPDATE_BOUNDARIES_URL
        }
        postData(`${_url}`, _data).then(
            response => {
                setSavingProperty(false)
                // reset parcel selection mode
                if (mapSelectionMode === MapSelectionMode.Parcel) {
                    dispatch(toggleParcelSelectionMode(uploadMode))
                }
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

    const clearBoundary = () => {
        if (mapSelectionMode === MapSelectionMode.Parcel) {
            dispatch(toggleParcelSelectionMode(uploadMode))
        }
        setBoundarySearchData(null)
        dispatch(setSelectedParcels([]))
        props.onBoundaryPropertyUpdated('')
        dispatch(triggerMapEvent({
            'id': uuidv4(),
            'name': MapEvents.BOUNDARY_FILES_REMOVED,
            'date': Date.now(),
            'payload': []
        }))
    }

    const getSelectButton = () => {
        return (
            <Grid item flex={1}>
                {mapSelectionMode === MapSelectionMode.Parcel ?
                    <Button variant='contained' className='Select' onClick={() => dispatch(toggleParcelSelectionMode(uploadMode)) }>CANCEL</Button> :
                    <Button variant='contained' className='Select' disabled={mapSelectionMode === MapSelectionMode.Digitise} onClick={() => dispatch(toggleParcelSelectionMode(uploadMode)) }>SELECT</Button>
                }
            </Grid>
        )
    }

    const tooltipText = 'Create your property boundary by either selecting the cadastral parcels that make up the property or manually digitising your property boundary using the tools below. You may also upload a boundary file from your property.'

    return (
        <Grid container className='UploadSection Step2' rowGap={2}>
            <Grid item className='UploadSectionHeader'>
                <span className='UploadSectionHeaderIcon Boundary'></span>
                <span>Create Property Boundary</span>
                <LightTooltip title={tooltipText}>
                    <HelpOutlineOutlinedIcon fontSize='small' className='UploadSectionHelpIcon' />
                </LightTooltip>
            </Grid>
            <Grid item className='UploadSectionContent' sx={{flex: 1}}>
                <Grid container flexDirection={'column'} className='SelectedParcelContainerParent'>
                    <Grid item className='SelectedParcelContainer'>
                        {boundarySearchData !== null && (
                            <UploadedBoundarySummary property_size_ha={boundarySearchData.property_size_ha} province={boundarySearchData.province}
                                upload_file_names={boundarySearchData.upload_file_names} />
                        )}
                        { boundarySearchData == null && props.property.id > 0 && props.property.boundary_source === BOUNDARY_FILE_SOURCE_TYPE && (
                            <UploadedBoundarySummary property_size_ha={props.property.size} province={props.property.province} />
                        )}
                        {(boundarySearchData === null && selectedParcels.length > 0) && (
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
                        )}
                        { !((boundarySearchData === null && selectedParcels.length > 0) || boundarySearchData !== null || (props.property.id > 0 && props.property.boundary_source === BOUNDARY_FILE_SOURCE_TYPE)) && (
                            <span className='hintText'>
                                {tooltipText}
                            </span>
                        )}
                    </Grid>
                </Grid>
            </Grid>
            <Grid item className='UploadSectionContent'>
                <Grid container flexDirection={'column'}>
                    <Grid item>
                        <Grid container flexDirection={'column'} flexWrap={'nowrap'} rowGap={2} className='ButtonContainer'>
                            { ((props.property.id === 0 && boundarySearchData === null) || (props.property.id > 0 && props.property.boundary_source !== BOUNDARY_FILE_SOURCE_TYPE)) && (
                                <Grid item>
                                    <Grid container flexDirection={'row'} flexWrap={'wrap'} justifyContent={'space-between'} spacing={1}>
                                        { getSelectButton() }
                                        <Grid item flex={1}>
                                            <Button variant='contained' className='Digitise' disabled={mapSelectionMode === MapSelectionMode.Parcel} onClick={() => dispatch(toggleDigitiseSelectionMode()) }>DIGITISE</Button>
                                        </Grid>
                                    </Grid>
                                </Grid>
                            )}
                            {(boundarySearchData !== null || props.property.id > 0) && (selectedParcels.length === 0) && (
                                <Grid item>
                                    <Button variant='contained' className='Upload' disabled={openUploader || boundarySearchData !== null || (props.property.id > 0 && props.property.boundary_source === BOUNDARY_FILE_SOURCE_TYPE)} onClick={() => setOpenUploader(true)}>UPLOAD</Button>
                                </Grid>
                            )}
                            {(boundarySearchData !== null || (props.property.id > 0 && props.property.boundary_source === BOUNDARY_FILE_SOURCE_TYPE) || selectedParcels.length > 0) && (
                                <Grid item>
                                    <Button variant='contained' className='Clear' disabled={openUploader} onClick={clearBoundary}>CLEAR BOUNDARY</Button>
                                </Grid>
                            )}
                            <Grid item>
                                { savingProperty ? (
                                    <Button variant='contained' className='Save' disabled={savingProperty}><CircularProgress size={16} sx={{marginRight: '5px' }}/> SAVING BOUNDARY...</Button>
                                ) : (
                                    <Button variant='contained' className='Save' disabled={savingProperty || (selectedParcels.length === 0 && boundarySearchData === null)} onClick={saveProperty}>SAVE BOUNDARY</Button>
                                )}
                            </Grid>
                        </Grid>
                    </Grid>        
                    <Grid item>
                        <AlertMessage message={alertMessage} onClose={() => setAlertMessage('')} />
                        <Uploader open={openUploader} onClose={() => setOpenUploader(false)}
                            onSuccessBoundarySearch={(boundarySearchData: BoundarySearchResultInterface) => {
                                setBoundarySearchData(boundarySearchData)
                                props.onBoundaryPropertyUpdated(BOUNDARY_FILE_SOURCE_TYPE)
                            }} />
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}
