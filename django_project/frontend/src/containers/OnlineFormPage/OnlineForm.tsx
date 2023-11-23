import React, { useState, useEffect } from 'react';
import axios from "axios";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Skeleton from "@mui/material/Skeleton";
import FormWizard, { FormMetadata } from './Forms/FormWizard';
import './index.scss';
import PropertyInterface from '../../models/Property';
import PropertySummaryTable from '../../components/PropertySummaryTable';
import MapPreview from '../../components/MapPreview';
import ConfirmationAlertDialog from '../../components/ConfirmationAlertDialog';
import { UploadSpeciesDetailInterface } from '../../models/Upload';

const FETCH_PROPERTY_DETAIL_URL = '/api/property/detail/'
const FETCH_FORM_METADATA_LIST_URL = '/api/population/metadata/list/'
const FETCH_FORM_DRAFT_LIST = '/api/upload/population/draft/'
const FETCH_EXISTING_POPULATION_DATA = '/api/upload/population/fetch/'


function OnlineForm() {
    const [loading, setLoading] = useState<boolean>(true)
    const [property, setProperty] = useState<PropertyInterface>(null)
    const [formMetadata, setFormMetadata] = useState<FormMetadata>(null)
    const [draftUUID, setDraftUUID] = useState<string>('')
    const [draftUUIDToConfirm, setDraftUUIDToConfirm] = useState<string>('')
    const [confirmationOpen, setConfirmationOpen] = useState(false)
    const [initialData, setInitialData] = useState<UploadSpeciesDetailInterface>(null)

    useEffect(() => {
        let fetch_apis = []
        let propertyId = (window as any).property_id
        let uploadId = parseInt((window as any).upload_id)
        setLoading(true)
        fetch_apis.push(
            axios.get(`${FETCH_PROPERTY_DETAIL_URL}${propertyId}/`)
        )
        fetch_apis.push(
            axios.get(`${FETCH_FORM_METADATA_LIST_URL}`)
        )
        if (uploadId > 0) {
            fetch_apis.push(
                axios.get(`${FETCH_EXISTING_POPULATION_DATA}${uploadId}/`)
            )
        } else {
            fetch_apis.push(
                axios.get(`${FETCH_FORM_DRAFT_LIST}${propertyId}/`)
            )
        }
        Promise.all(fetch_apis).then((responses) => {
            setLoading(false)
            setProperty(responses[0].data as PropertyInterface)
            setFormMetadata(responses[1].data as FormMetadata)
            if (uploadId) {
                console.log('data ', responses[2].data)
                setInitialData(responses[2].data as UploadSpeciesDetailInterface)
            } else {
                let _draftList = responses[2].data as string[]
                if (_draftList && _draftList.length) {
                    setDraftUUIDToConfirm(_draftList[0])
                    setConfirmationOpen(true)
                }
            }
          }).catch(error => {
            setLoading(false)
            console.log(error)
            alert('Unexpected error while loading property data!')
          })
    }, [])

    /* draft upload confirmation */
    const handleDraftConfirmationOk = () => {
        setConfirmationOpen(false)
        setDraftUUID(draftUUIDToConfirm)
        setDraftUUIDToConfirm('')
    }

    const handleDraftConfirmationClose = () => {
        // delete draft
        axios.delete(
            `${FETCH_FORM_DRAFT_LIST}${draftUUIDToConfirm}/`, {}
        ).then(
            response => {
                setConfirmationOpen(false)
                setDraftUUIDToConfirm('')
            }
        ).catch(error => {
            // ignore error
            setConfirmationOpen(false)
            setDraftUUIDToConfirm('')
        })
    }
    /* end of draft upload confirmation */

    return (
        <div className="App">
            <div className="OnlineFormPage">
                <Grid container flexDirection={'row'}>
                    <Grid item>
                        <Box className='LeftSideBar'>
                            <Box className='EmptyHeader'>
                                DATA UPLOAD
                            </Box>
                            <Box className='LeftSideBarContent'>
                                {loading ? <Skeleton sx={{height: '100%'}} /> : <MapPreview propertyItem={property} /> }
                            </Box>
                            <Box className='LeftSideBarContent'>
                                {loading ? <Skeleton sx={{height: '100%'}} /> : <PropertySummaryTable propertyItem={property} /> }
                            </Box>
                        </Box>
                    </Grid>
                    <Grid item flex={1}>
                        <Grid container className="Content" flexDirection={'column'}>
                            <Grid item className='FlexContainerFillHeight'>
                                {loading ? <Skeleton sx={{height: '100%'}} /> : <FormWizard propertyItem={property} metadata={formMetadata} draftUUID={draftUUID} initialData={initialData} /> }
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item>
                        <ConfirmationAlertDialog open={confirmationOpen} alertClosed={handleDraftConfirmationClose}
                            alertConfirmed={handleDraftConfirmationOk}
                            alertDialogTitle={'Draft Upload'}
                            alertDialogDescription={'You have a draft upload. Do you want to continue to edit the draft?'}
                            confirmButtonText='OK'
                            confirmButtonProps={{color: 'success', autoFocus: true}}
                        />
                    </Grid>
                </Grid>
            </div>
        </div>
    )
}

export default OnlineForm;