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

const FETCH_PROPERTY_DETAIL_URL = '/api/property/detail/'
const FETCH_FORM_METADATA_LIST_URL = '/api/population/metadata/list/'


function OnlineForm() {
    const [loading, setLoading] = useState<boolean>(true)
    const [uploadSession, setUploadSession] = useState<string>('')
    const [property, setProperty] = useState<PropertyInterface>(null)
    const [formMetadata, setFormMetadata] = useState<FormMetadata>(null)

    useEffect(() => {
        let fetch_apis = []
        let propertyId = (window as any).property_id
        setLoading(true)
        fetch_apis.push(
            axios.get(`${FETCH_PROPERTY_DETAIL_URL}${propertyId}/`)
        )
        fetch_apis.push(
            axios.get(`${FETCH_FORM_METADATA_LIST_URL}`)
        )
        Promise.all(fetch_apis).then((responses) => {
            setLoading(false)
            setProperty(responses[0].data as PropertyInterface)
            setFormMetadata(responses[1].data as FormMetadata)
          }).catch(error => {
            setLoading(false)
            console.log(error)
            alert('Unexpected error while loading property data!')
          })
    }, [])

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
                                {loading ? <Skeleton sx={{height: '100%'}} /> : <FormWizard propertyItem={property} metadata={formMetadata} /> }
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </div>
        </div>
    )
}

export default OnlineForm;