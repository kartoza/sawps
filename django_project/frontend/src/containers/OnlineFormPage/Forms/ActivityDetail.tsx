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



interface ActivityDetailInterface {
    initialData: UploadSpeciesDetailInterface;
    setIsDirty: (isDirty: boolean) => void;
    handleBack: (data: UploadSpeciesDetailInterface) => void;
    handleNext: (data: UploadSpeciesDetailInterface) => void;
}

export default function ActivityDetail(props: ActivityDetailInterface) {
    const [data, setData] = useState<UploadSpeciesDetailInterface>(getDefaultUploadSpeciesDetail(0))

    useEffect(() => {
        setData({
            ...props.initialData,
            annual_population: {...props.initialData.annual_population},
            intake_population: {...props.initialData.intake_population},
            offtake_population: {...props.initialData.offtake_population}
        })
    }, [props.initialData])

    return (
        <Grid container flexDirection={'column'} rowSpacing={2}>
            <Grid item>

            </Grid>
            <Grid item container flexDirection={'row'} justifyContent={'flex-end'} columnSpacing={2}>
                <Grid item>
                    <Button variant='outlined' onClick={() => props.handleBack(data)}>BACK</Button>
                </Grid>
                <Grid item>
                    <Button variant='contained' onClick={() => props.handleNext(data)}>NEXT</Button>
                </Grid>
            </Grid>
        </Grid>
    )
}