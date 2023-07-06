import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import Button from '@mui/material/Button';
import {
    UploadSpeciesDetailInterface,
    getDefaultUploadSpeciesDetail,
    AnnualPopulationInterface,
    TaxonMetadata,
    CommonUploadMetadata
} from '../../../models/Upload';



interface ReviewAndConfirmInterface {
    initialData: UploadSpeciesDetailInterface;
    handleBack: (data: UploadSpeciesDetailInterface) => void;
}

export default function ReviewAndConfirm(props: ReviewAndConfirmInterface) {
    return (
        <Grid container flexDirection={'column'} rowSpacing={2}>
            <Grid item>

            </Grid>
            <Grid item container flexDirection={'row'} justifyContent={'flex-end'} columnSpacing={2}>
                <Grid item>
                    <Button variant='outlined' onClick={() => props.handleBack(props.initialData)}>BACK</Button>
                </Grid>
                <Grid item>
                    <Button variant='contained' onClick={() => {}}>SUBMIT</Button>
                </Grid>
            </Grid>
        </Grid>
    )
}