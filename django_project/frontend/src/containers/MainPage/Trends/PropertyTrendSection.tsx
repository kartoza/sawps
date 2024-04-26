import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {Box, Typography, Grid, Divider} from "@mui/material";
import PopulationTrendChart, {PopulationTrendItem} from './PopulationTrendChart';
import Loading from '../../../components/Loading';

interface PropertyTrendSectionInterface {
    species: string;
    property: string;
}

const SPECIES_POPULATION_TREND_URL = '/api/species/population_trend/'

interface PropertyTrendDict {
    [key: string]: PopulationTrendItem[];
}

const PropertyTrendSection = (props: PropertyTrendSectionInterface) => {
    const [populationTrendData, setPopulationTrendData] = useState<PropertyTrendDict>({})
    const [loadingTrendData, setLoadingTrendData] = useState(false)

    const fetchPropertyTrendData = (species: string, property: string) => {
        setLoadingTrendData(true)
        let _data = {
            'species': species,
            'property': property
        }
        axios.post(`${SPECIES_POPULATION_TREND_URL}`, _data)
            .then((response) => {
                setLoadingTrendData(false)
                let _results_data = response.data['results']
                if (_results_data) {
                    let _trendData: PropertyTrendDict = {}
                    for (let i=0; i < _results_data.length; ++i) {
                        let _trend = _results_data[i]
                        let _property = _trend['property']
                        let _item: PopulationTrendItem = {
                            'year': _trend['year'],
                            'sum_fitted': _trend['fitted_pop_est'],
                            'lower_ci': _trend['lower_ci'],
                            'upper_ci': _trend['upper_ci'],
                            'raw_pop_est': _trend['raw_pop_est']
                        }
                        if (_property in _trendData) {
                            _trendData[_property].push(_item)
                        } else {
                            _trendData[_property] = [_item]
                        }
                    }
                    setPopulationTrendData({..._trendData})
                }
        }).catch((error) => {
            setLoadingTrendData(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchPropertyTrendData(props.species, props.property)
    }, [props.species, props.property])


    return (
        <Box className={'SectionContainer'}>
            <Grid container flexDirection={'column'}>
                <Grid item className='SectionTitle'>
                    <Typography>{Object.keys(populationTrendData).length > 1 ? 'Properties' : 'Property'}</Typography>
                    <Divider />
                </Grid>
                <Grid item>
                    <Grid container flexDirection={'column'}>
                        <Grid item>
                            {loadingTrendData && <Loading containerStyle={{minHeight: 160}}/>}
                            {!loadingTrendData && Object.keys(populationTrendData).length > 0 ? 
                            <Grid container flexDirection={'row'} spacing={{ xs: 1 }} columns={{ xs: 4, sm: 8, md: 8, xl: 12 }}>
                                {Object.keys(populationTrendData).map((property, index) => {
                                    return (
                                        <Grid item xs={4} key={index}>
                                            <PopulationTrendChart chartId={`property-population-trend-${property}`} chartTitle={`${property}`} data={populationTrendData[property]} showRawPopEst={true} />
                                        </Grid>
                                    )
                                })}
                            </Grid>
                            : null}
                            {!loadingTrendData && props.property && props.property.length > 0 && Object.keys(populationTrendData).length == 0 ?
                            <Box className='SectionEmpty'>
                                {'Insufficient data for selected ' + (props.property && props.property.length === 1 ? 'property': 'properties')}
                            </Box>
                            : null}
                            {!loadingTrendData && !props.property ?
                            <Box className='SectionEmpty'>
                                {'Choose one or more property to view the property trend data.'}
                            </Box>
                            : null}
                        </Grid>
                        <Grid item>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Box>
    )
}

export default PropertyTrendSection
