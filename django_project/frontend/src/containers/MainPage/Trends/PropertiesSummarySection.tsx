import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {Box, Typography, Grid, Divider} from "@mui/material";
import './index.scss';
import Loading from '../../../components/Loading';
import PopulationHistogramChart, { PopulationHistogramItem } from './PopulationHistogramChart';


interface PropertiesSummarySectionInterface {
    species: string;
}

const SPECIES_POPULATION_TREND_URL = '/api/species/population_trend/'
const NUM_PROPERTIES_PER_POP_SIZE_CAT = 'num_properties_per_pop_size_cat'
const NUM_PROPERTIES_PER_DENSITY_CAT = 'num_properties_per_density_cat'


const PropertiesSummarySection = (props: PropertiesSummarySectionInterface) => {
    const [loadingPerPopSizeData, setLoadingPerPopSizeData] = useState(true)
    const [loadingPerDensityData, setLoadingPerDensityData] = useState(true)
    const [populationHistogramPerPopSizeData, setPopulationHistogramPerPopSizeData] = useState<PopulationHistogramItem[]>([])
    const [populationHistogramPerDensityData, setPopulationHistogramPerDensityData] = useState<PopulationHistogramItem[]>([])

    const toggleLoading = (loading: boolean, type: string) => {
        if (type === NUM_PROPERTIES_PER_POP_SIZE_CAT) {
            setLoadingPerPopSizeData(loading)
        } else {
            setLoadingPerDensityData(loading)
        }
    }

    const fetchPopulationHistogram = (species: string, type: string) => {
        toggleLoading(true, type)
        axios.get(`${SPECIES_POPULATION_TREND_URL}?species=${species}&level=national&data_type=${type}`)
        .then((response) => {
            toggleLoading(false, type)
            if (response.data['results']) {
                if (type === NUM_PROPERTIES_PER_POP_SIZE_CAT) {
                    setPopulationHistogramPerPopSizeData(response.data['results'] as PopulationHistogramItem[])
                } else {
                    setPopulationHistogramPerDensityData(response.data['results'] as PopulationHistogramItem[])
                }
            }
        }).catch((error) => {
            toggleLoading(false, type)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchPopulationHistogram(props.species, NUM_PROPERTIES_PER_POP_SIZE_CAT)
        fetchPopulationHistogram(props.species, NUM_PROPERTIES_PER_DENSITY_CAT)
    }, [props.species])    

    return (
        <Box className={'SectionContainer'}>
            <Grid container flexDirection={'column'}>
                <Grid item className='SectionTitle'>
                    <Typography>Properties Summary</Typography>
                    <Divider />
                </Grid>
                <Grid item>
                    {(loadingPerPopSizeData || loadingPerDensityData  || populationHistogramPerPopSizeData.length > 0 || populationHistogramPerDensityData.length > 0) ?
                    <Grid container flexDirection={'row'} spacing={1}>
                        <Grid item sm={12} md={12} lg={6}>
                            {!loadingPerPopSizeData ?
                                <PopulationHistogramChart
                                    data={populationHistogramPerPopSizeData}
                                    chartId='properties-per-population-size-cat'
                                    chartTitle='The number of properties per population size category'
                                    chartXLabel='Population Size Category (total size of population)'
                                    chartYLabels={['Percentage (%) of', 'properties of each size']}
                                    color='#00B1E9'
                                />
                            : <Loading containerStyle={{minHeight: 160}}/>}
                        </Grid>
                        <Grid item sm={12} md={12} lg={6}>
                            {!loadingPerDensityData ?
                                <PopulationHistogramChart
                                    data={populationHistogramPerDensityData}
                                    chartId='properties-per-density-cat'
                                    chartTitle='The number of properties per density category'
                                    chartXLabel='Population Size Category (total size of population)'
                                    chartYLabels={['Percentage (%) of', 'properties of each density']}
                                    color='#00AB76'
                                />
                            : <Loading containerStyle={{minHeight: 160}}/>}
                        </Grid>
                    </Grid>
                    : null}
                    {(!loadingPerPopSizeData && !loadingPerDensityData && populationHistogramPerPopSizeData.length === 0 && populationHistogramPerDensityData.length === 0) ? <Box className='SectionEmpty'>
                        {'Insufficient amount of data for this species to generate trend charts.'}
                    </Box>
                    :null}
                </Grid>
            </Grid>
        </Box>
    )

}

export default PropertiesSummarySection;