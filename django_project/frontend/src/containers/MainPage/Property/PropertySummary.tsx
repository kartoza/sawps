import React from 'react';
import Grid from "@mui/material/Grid";
import {RootState} from '../../../app/store';
import { useAppSelector } from '../../../app/hooks';
import PropertySummaryTable from '../../../components/PropertySummaryTable';
import SpeciesSideBarLineChart from '../Metrics/SpeciesSideBarLineChart';
import ActivityBarChart from '../Metrics/ActivityBarChart';


export default function PropertySummary() {
    const propertyItem = useAppSelector((state: RootState) => state.mapState.selectedProperty)
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)

    return (
        <Grid container flexDirection={'column'} className='PropertySummary'>
            <Grid item className='EmptyHeader'></Grid>
            <Grid item className='FlexContainerFill'>
                <Grid container className='ContentContainer'>
                    <Grid item className='Header'>
                        <Grid container flexDirection={'row'} justifyContent={'space-between'}>
                            <Grid item className='SiteDetailTitle'>
                                <span className='SiteDetailIcon'></span>
                                <span>Property Information</span>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item className='FlexContainerFillHeight'>
                        <Grid container className='SummaryContent'>
                            <Grid item>
                                <PropertySummaryTable propertyItem={propertyItem} />
                            </Grid>
                            <Grid item>
                                <Grid item className='Header'>
                                    <Grid container flexDirection={'row'} justifyContent={'space-between'}>
                                        <Grid item className='SiteDetailTitle'>
                                            <span className='LineChartIcon'></span>
                                            <span>Species Populations</span>
                                        </Grid>
                                    </Grid>
                                </Grid>
                                <SpeciesSideBarLineChart
                                    property={propertyItem.id}            
                                    selectedSpecies={selectedSpecies}
                                    from={startYear}
                                    to={endYear}
                                />
                            </Grid>
                            <Grid item>
                                <Grid item className='Header'>
                                        <Grid container flexDirection={'row'} justifyContent={'space-between'}>
                                            <Grid item className='SiteDetailTitle'>
                                                <span className='SiteDetailIcon'></span>
                                                <span>Activity Metrics</span>
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                    <ActivityBarChart
                                        property={propertyItem.id}            
                                        selectedSpecies={selectedSpecies}
                                        from={startYear}
                                        to={endYear}
                                    />
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}
