import React, { useState, useEffect } from 'react';
import axios from "axios";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Skeleton from "@mui/material/Skeleton";
import FormWizard from './Forms/FormWizard';
import './index.scss';
import PropertyInterface from '../../models/Property';
import PropertySummaryTable from '../../components/PropertySummaryTable';
import MapPreview from '../../components/MapPreview';

const FETCH_PROPERTY_DETAIL_URL = '/api/property/detail/'


function OnlineForm() {
    const [loading, setLoading] = useState<boolean>(true)
    const [uploadSession, setUploadSession] = useState<string>('')
    const [property, setProperty] = useState<PropertyInterface>(null)

    const fetchPropertyDetail = () => {
        setLoading(true)
        let propertyId = (window as any).property_id
        axios.get(`${FETCH_PROPERTY_DETAIL_URL}${propertyId}/`).then((response) => {
            setLoading(false)
            if (response.data) {
                // set selected property
                setProperty(response.data as PropertyInterface)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchPropertyDetail()
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
                                {loading ? <Skeleton sx={{height: '100%'}} /> : <FormWizard propertyItem={property}/> }
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </div>
        </div>
    )
}

export default OnlineForm;