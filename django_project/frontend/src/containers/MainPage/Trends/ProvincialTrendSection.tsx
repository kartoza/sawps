import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {Box, Typography, Grid, Divider} from "@mui/material";
import PopulationTrendChart, {PopulationTrendItem} from './PopulationTrendChart';
import './index.scss';

interface ProvincialTrendSectionInterface {
    species: string;
}

interface ProvincialPopulationTrendDict {
    [key: string]: PopulationTrendItem[];
}

const SPECIES_POPULATION_TREND_URL = '/api/species/population_trend/'


const ProvincialTrendSection = (props: ProvincialTrendSectionInterface) => {
    const [populationTrendData, setPopulationTrendData] = useState<ProvincialPopulationTrendDict>({})

    const fetchProvincialTrendData = (species: string) => {
        axios.get(`${SPECIES_POPULATION_TREND_URL}?species=${species}&level=provincial`)
            .then((response) => {
            if (response.data) {
                let _trendData: ProvincialPopulationTrendDict = {}
                for (let i=0; i < response.data.length; ++i) {
                    let _trend = response.data[i]
                    let _province = _trend['province']
                    let _item: PopulationTrendItem = {
                        'year': _trend['year'],
                        'sum_fitted': _trend['sum_fitted'],
                        'lower_ci': _trend['lower_ci'],
                        'upper_ci': _trend['upper_ci']
                    }
                    if (_province in _trendData) {
                        _trendData[_province].push(_item)
                    } else {
                        _trendData[_province] = [_item]
                    }
                }
                setPopulationTrendData({..._trendData})
            }
        }).catch((error) => {
            console.log(error)
        })
    }
    
    useEffect(() => {
        fetchProvincialTrendData(props.species)
    }, [props.species])

    return (
        <Box className={'SectionContainer'}>
            <Grid container flexDirection={'column'}>
                <Grid item className='SectionTitle'>
                    <Typography>Provincial</Typography>
                    <Divider />
                </Grid>
                <Grid item>
                    <Grid container flexDirection={'column'}>
                        <Grid item>
                            <Grid container flexDirection={'row'} spacing={{ xs: 1 }} columns={{ xs: 4, sm: 8, md: 12, xl: 12 }}>
                                {Object.keys(populationTrendData).map((province, index) => {
                                    return (
                                        <Grid item xs={4} key={index}>
                                            <PopulationTrendChart chartId={`province-population-trend-${province}`} chartTitle={`${province}`} data={populationTrendData[province]} />
                                        </Grid>
                                    )
                                })}
                            </Grid>
                        </Grid>
                        <Grid item>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Box>
    )

}

export default ProvincialTrendSection
