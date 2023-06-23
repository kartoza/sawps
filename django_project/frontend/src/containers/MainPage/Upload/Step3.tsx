import React, { useState } from 'react';
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import PropertyInterface from '../../../models/Property';
import { PropertyInfo } from '../Property';

interface Step3Interface {
    property: PropertyInterface;
    onUpdateBoundary: () => void;
}

export default function Step3(props: Step3Interface) {
    
    return (
        <Grid container className='UploadSection Step3' rowGap={2}>
            <Grid item className='UploadSectionHeader'>
                <span className='UploadSectionHeaderIcon Population'></span>
                <span>Upload Species Population Data</span>
            </Grid>
            <Grid item className='UploadSectionContent'>
                <Grid container flexDirection={'row'} flexWrap={'nowrap'} justifyContent={'space-between'} rowGap={2} className='ButtonContainer'>
                    <Button variant='contained' className='ManualForm'>ONLINE FORM</Button>
                    <Button variant='contained' className='Download'>DOWNLOAD TEMPLATE</Button>
                    <Button variant='contained' className='Upload'>UPLOAD TEMPLATE</Button>
                </Grid>
            </Grid>
            <Grid item className='UploadSectionHeader'>
                <span className='UploadSectionHeaderIcon SiteDetail'></span>
                <span>Selected Property Information</span>
            </Grid>
            <Grid item className='UploadSectionContent'>
                <Grid container flexDirection={'column'} flexWrap={'nowrap'} rowGap={2} className='ButtonContainer'>
                    <Button variant='contained' className='UpdateBoundary' onClick={props.onUpdateBoundary}>UPDATE PROPERTY BOUNDARY</Button>
                </Grid>
            </Grid>
            <Grid item className='UploadSectionContent'>
                <PropertyInfo property={props.property} enableForm={false} />
            </Grid>
        </Grid>
    )
}
