import React from 'react';
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import {RootState} from '../../../app/store';
import {useAppSelector } from '../../../app/hooks';
import PropertySummaryTable from './PropertySummaryTable';


export default function PropertySummary() {
    const propertyItem = useAppSelector((state: RootState) => state.mapState.selectedProperty)


    return (
        <Grid container flexDirection={'column'} className='PropertySummary'>
            <Grid item className='EmptyHeader'>
                
            </Grid>
            <Grid item className='FlexContainerFill'>
                <Grid container className='ContentContainer'>
                    <Grid item className='Header'>
                        <Grid container flexDirection={'row'} justifyContent={'space-between'}>
                            <Grid item className='SiteDetailTitle'>
                                <span className='SiteDetailIcon'></span>
                                <span>{ `Property: ID${propertyItem.id}` }</span>
                            </Grid>
                            <Grid item>
                                <Button variant='contained'>UPLOAD SPECIES DATA</Button>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item className='FlexContainerFillHeight'>
                        <Grid container className='SummaryContent'>
                            <Grid item>
                                <PropertySummaryTable propertyItem={propertyItem} />
                            </Grid>
                            <Grid item>
                                {/* Species data chart */}
                            </Grid>
                            <Grid item>
                                {/* Total species table */}
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}
