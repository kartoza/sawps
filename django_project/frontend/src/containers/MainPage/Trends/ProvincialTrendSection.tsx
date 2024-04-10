import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {Box, Typography, Grid, Divider} from "@mui/material";
import PopulationTrendChart, {PopulationTrendItem} from './PopulationTrendChart';
import {GrowthDataItem} from './GrowthChart';
import GroupedGrowthChart from './GroupedGrowthChart';
import './index.scss';
import Loading from '../../../components/Loading';
import {setSelectedProvinceCount} from "../../../reducers/SpeciesFilter";

interface ProvincialTrendSectionInterface {
    species: string;
    province: string[]
}

interface ProvincialPopulationTrendDict {
    [key: string]: PopulationTrendItem[];
}
interface ProvincialPopulationGrowthDict {
    [key: string]: GrowthDataItem[];
}

const SPECIES_POPULATION_TREND_URL = '/api/species/population_trend/'


const ProvincialTrendSection = (props: ProvincialTrendSectionInterface) => {
    const [allPopulationTrendData, setAllPopulationTrendData] = useState<ProvincialPopulationTrendDict>({})
    const [allPopulationGrowthData, setAllPopulationGrowthData] = useState<ProvincialPopulationGrowthDict>({})
    const [populationTrendData, setPopulationTrendData] = useState<ProvincialPopulationTrendDict>({})
    const [populationGrowthData, setPopulatioGrowthData] = useState<ProvincialPopulationGrowthDict>({})
    const [loadingTrendData, setLoadingTrendData] = useState(false)
    const [loadingGrowthData, setLoadingGrowthData] = useState(false)

    const fetchProvincialTrendData = (species: string) => {
        setLoadingTrendData(true)
        axios.get(`${SPECIES_POPULATION_TREND_URL}?species=${species}&level=provincial`)
            .then((response) => {
            setLoadingTrendData(false)
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
                setAllPopulationTrendData({..._trendData})
                setPopulationTrendData({..._trendData})
            }
        }).catch((error) => {
            setLoadingTrendData(false)
            console.log(error)
        })
    }

    const fetchProvincialGrowthData = (species: string) => {
        setLoadingGrowthData(true)
        axios.get(`${SPECIES_POPULATION_TREND_URL}?species=${species}&level=provincial&data_type=growth`)
            .then((response) => {
            setLoadingGrowthData(false)
            if (response.data) {
                // check if has data
                if (response.data.length === 1) {
                    let _item = response.data[0]
                    if ('data.limitation' in _item) {
                        setPopulatioGrowthData({})
                        return;
                    }
                }
                let _data: ProvincialPopulationGrowthDict = {}
                for (let i = 0; i < response.data.length; i++) {
                    let _item = response.data[i] as GrowthDataItem
                    let _province = _item.province
                    if (_province in _data) {
                        _data[_province].push(_item)
                    } else {
                        _data[_province] = [_item]
                    }
                }
                setAllPopulationGrowthData({..._data})
                setPopulatioGrowthData({..._data})
            }
        }).catch((error) => {
            setLoadingGrowthData(false)
            console.log(error)
        })
    }
    
    useEffect(() => {
        fetchProvincialTrendData(props.species)
        fetchProvincialGrowthData(props.species)
    }, [props.species])

    useEffect(() => {
        setPopulatioGrowthData(
          Object.fromEntries(Object.entries(allPopulationGrowthData).filter(([key]) => props.province.includes(key)))
        )
        setPopulationTrendData(
          Object.fromEntries(Object.entries(allPopulationTrendData).filter(([key]) => props.province.includes(key)))
        )
    }, [props.province])

    return (
        <Box className={'SectionContainer'}>
            <Grid container flexDirection={'column'}>
                <Grid item className='SectionTitle'>
                    <Typography>Provincial</Typography>
                    <Divider />
                </Grid>
                <Grid item>
                    {(loadingTrendData || loadingGrowthData || Object.keys(populationTrendData).length > 0) ? <Grid container flexDirection={'column'} spacing={1}>
                        <Grid item>
                            {!loadingTrendData ? 
                            <Grid container flexDirection={'row'} spacing={{ xs: 1 }} columns={{ xs: 4, sm: 8, md: 8, xl: 12 }}>
                                {Object.keys(populationTrendData).map((province, index) => {
                                    return (
                                        <Grid item xs={4} key={index}>
                                            <PopulationTrendChart chartId={`province-population-trend-${province}`} chartTitle={`${province}`} data={populationTrendData[province]} />
                                        </Grid>
                                    )
                                })}
                            </Grid>
                            : <Loading containerStyle={{minHeight: 160}}/>}
                        </Grid>
                        <Grid item>
                            {!loadingGrowthData ? 
                            <Grid container flexDirection={'row'} spacing={{ xs: 1 }} columns={{ xs: 4, sm: 4, md: 12, xl: 12 }}>
                                {Object.keys(populationGrowthData).map((province, index) => {
                                    return (
                                        <Grid item xs={4} md={6} key={index}>
                                            <GroupedGrowthChart chartId={`province-growth-chart-${province}`} title={`${province}`} data={populationGrowthData[province]} />
                                        </Grid>
                                    )
                                })}
                            </Grid>
                            : <Loading containerStyle={{minHeight: 160}}/>}
                        </Grid>
                    </Grid>
                    : null}
                    {(!loadingTrendData && !loadingGrowthData && Object.keys(populationTrendData).length === 0) ? <Box className='SectionEmpty'>
                        {'Insufficient amount of data for this species to generate trend charts.'}
                    </Box>
                    :null}
                </Grid>
            </Grid>
        </Box>
    )

}

export default ProvincialTrendSection
