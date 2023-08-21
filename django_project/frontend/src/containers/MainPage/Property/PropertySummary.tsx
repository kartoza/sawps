import React from 'react';
import Grid from "@mui/material/Grid";
import {RootState} from '../../../app/store';
import { useAppSelector } from '../../../app/hooks';
import PropertySummaryTable from '../../../components/PropertySummaryTable';
import SpeciesSideBarLineChart from '../Metrics/SpeciesSideBarLineChart';
import ActivityBarChart from '../Metrics/ActivityBarChart';
import { UserRole } from '../../../models/Stakeholder';


export default function PropertySummary() {
    const propertyItem = useAppSelector((state: RootState) => state.mapState.selectedProperty)
    const userRole = (window as any).userRole

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
                            { userRole !== UserRole.DECISION_MAKER &&
                                <Grid item>
                                    <Grid item className='Header'>
                                        <Grid container flexDirection={'row'} justifyContent={'space-between'}>
                                            <Grid item className='SiteDetailTitle'>
                                                <span className='LineChartIcon'></span>
                                                <span>Species Populations</span>
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                    <SpeciesSideBarLineChart property={propertyItem.id}/>
                                </Grid>
                            }
                            { userRole !== UserRole.DECISION_MAKER &&
                                <Grid item>
                                    <Grid item className='Header'>
                                        <Grid container flexDirection={'row'} justifyContent={'space-between'}>
                                            <Grid item className='SiteDetailTitle'>
                                                <span className='SiteDetailIcon'></span>
                                                <span>Activity Metrics</span>
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                    <ActivityBarChart property={propertyItem.id}/>
                                </Grid>
                            }
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}
