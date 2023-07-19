import React, { useState } from 'react';
import {v4 as uuidv4} from 'uuid';
import axios from "axios";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import {RootState} from '../../../app/store';
import {useAppDispatch, useAppSelector } from '../../../app/hooks';
import {
    setSelectedProperty,
    setSelectedParcels,
    triggerMapEvent
} from '../../../reducers/MapState';
import {
    setUploadState
} from '../../../reducers/UploadState';
import PropertySummaryTable from '../../../components/PropertySummaryTable';
import { UploadMode } from '../../../models/Upload';
import PropertyInterface from '../../../models/Property';


const FETCH_PROPERTY_DETAIL_URL = '/api/property/detail/'

export default function PropertySummary() {
    const dispatch = useAppDispatch()
    const [loading, setLoading] = useState(false)
    const propertyItem = useAppSelector((state: RootState) => state.mapState.selectedProperty)

    const onUploadSpeciesClicked = () => {
        if (propertyItem.id) {
            // fetch property detail
            setLoading(true)
            axios.get(`${FETCH_PROPERTY_DETAIL_URL}${propertyItem.id}/`).then((response) => {
                setLoading(false)
                if (response.data) {
                    // set selected parcels+property
                    let _property = response.data as PropertyInterface
                    dispatch(setSelectedProperty(_property))
                    dispatch(setSelectedParcels(_property.parcels))
                    dispatch(setUploadState(UploadMode.PropertySelected))
                    // trigger map zoom to bbox
                    if (_property.bbox && _property.bbox.length === 4) {
                        let _bbox = _property.bbox.map(String)
                        dispatch(triggerMapEvent({
                            'id': uuidv4(),
                            'name': 'PROPERTY_SELECTED',
                            'date': Date.now(),
                            'payload': _bbox
                        }))
                    }
                }
            }).catch((error) => {
                setLoading(false)
                console.log(error)
            })
        }
    }

    return (
        <Grid container flexDirection={'column'} className='PropertySummary'>
            <Grid item className='EmptyHeader'></Grid>
            <Grid item className='FlexContainerFill'>
                <Grid container className='ContentContainer'>
                    <Grid item className='Header'>
                        <Grid container flexDirection={'row'} justifyContent={'space-between'}>
                            <Grid item className='SiteDetailTitle'>
                                <span className='SiteDetailIcon'></span>
                                <span>{ `Property: ID${propertyItem.id}` }</span>
                            </Grid>
                            <Grid item>
                                <Button variant='contained' disabled={propertyItem.id===0} onClick={onUploadSpeciesClicked}>UPLOAD SPECIES DATA</Button>
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
