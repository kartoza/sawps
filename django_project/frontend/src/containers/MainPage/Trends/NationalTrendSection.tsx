import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {Box, Typography, Grid, Divider} from "@mui/material";
import PopulationTrendChart, {PopulationTrendItem} from './PopulationTrendChart';
import {GrowthDataItem} from './GrowthChart';
import GroupedGrowthChart from './GroupedGrowthChart';
import './index.scss';
import Loading from '../../../components/Loading';
import AreaAvailableLineChart from "../Metrics/AreaAvailableLineChart";
import { capitalizeSentence } from '../../../utils/Helpers';


interface NationalTrendSectionInterface {
    species: string;
}

const SPECIES_POPULATION_TREND_URL = '/api/species/population_trend/'


const NationalTrendSection = (props: NationalTrendSectionInterface) => {
    const [populationTrendData, setPopulationTrendData] = useState<PopulationTrendItem[]>([])
    const [largePopulationGrowthData, setLargePopulationGrowthData] = useState<GrowthDataItem[]>([])
    const [mediumPopulationGrowthData, setMediumPopulationGrowthData] = useState<GrowthDataItem[]>([])
    const [smallPopulationGrowthData, setSmallPopulationGrowthData] = useState<GrowthDataItem[]>([])
    const [loadingTrendData, setLoadingTrendData] = useState(false)
    const [loadingGrowthData, setLoadingGrowthData] = useState(false)

    const fetchNationalTrendData = (species: string) => {
        setLoadingTrendData(true)
        axios.get(`${SPECIES_POPULATION_TREND_URL}?species=${species}&level=national&data_type=trend`)
            .then((response) => {
            setLoadingTrendData(false)
            if (response.data) {
                setPopulationTrendData(response.data as PopulationTrendItem[])
            }
        }).catch((error) => {
            setLoadingTrendData(false)
            console.log(error)
        })
    }

    const fetchNationalGrowthData = (species: string) => {
        setLoadingGrowthData(true)
        axios.get(`${SPECIES_POPULATION_TREND_URL}?species=${species}&level=national&data_type=growth`)
            .then((response) => {
            setLoadingGrowthData(false)
            if (response.data) {
                let _large: GrowthDataItem[] = []
                let _medium: GrowthDataItem[] = []
                let _small: GrowthDataItem[] = []
                for (let i = 0; i < response.data.length; i++) {
                    let _item = response.data[i] as GrowthDataItem
                    if (_item.pop_size_cat === 'large') {
                        _large.push(_item)
                    } else if (_item.pop_size_cat === 'medium') {
                        _medium.push(_item)
                    } else if (_item.pop_size_cat === 'small') {
                        _small.push(_item)
                    }
                }
                setLargePopulationGrowthData(_large)
                setMediumPopulationGrowthData(_medium)
                setSmallPopulationGrowthData(_small)
            }
        }).catch((error) => {
            setLoadingGrowthData(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchNationalTrendData(props.species)
        fetchNationalGrowthData(props.species)
    }, [props.species])

    return (
        <Box className={'SectionContainer'}>
            <Grid container flexDirection={'column'}>
                <Grid item className='SectionTitle'>
                    <Typography>National</Typography>
                    <Divider />
                </Grid>
                <Grid item>
                    {(loadingTrendData || loadingGrowthData || populationTrendData.length > 0) ? <Grid container flexDirection={'row'} spacing={1}>
                        <Grid item sm={12} md={12} lg={5}>
                            <Grid container flexDirection={'column'} className='national-trend-left-side'>
                                <Grid item>
                                    {!loadingTrendData ?
                                        <PopulationTrendChart chartId='national-population-trend' chartTitle={capitalizeSentence(`${props.species} National Population Trend`)} data={populationTrendData} />
                                    : <Loading containerStyle={{minHeight: 160}}/>}
                                </Grid>
                                <Grid item></Grid>
                                <Grid item style={{ marginTop: 15 }}>
                                    <AreaAvailableLineChart
                                        propertyId={''}
                                        startYear={1960}
                                        endYear={new Date().getFullYear()}
                                        national={true}
                                    />
                                </Grid>
                            </Grid>
                        </Grid>
                        <Grid item sm={12} md={12} lg={7}>
                            {!loadingGrowthData ?
                                <Grid container flexDirection={'column'} spacing={1}>
                                    <Grid item>
                                        <GroupedGrowthChart chartId='large-national-growth-chart' title={capitalizeSentence(`Large ${props.species} Populations`)} data={largePopulationGrowthData} />
                                    </Grid>
                                    <Grid item>
                                        <GroupedGrowthChart chartId='medium-national-growth-chart' title={capitalizeSentence(`Medium ${props.species} Populations`)} data={mediumPopulationGrowthData} />
                                    </Grid>
                                    <Grid item>
                                        <GroupedGrowthChart chartId='small-national-growth-chart' title={capitalizeSentence(`Small ${props.species} Populations`)} data={smallPopulationGrowthData} />                                    
                                    </Grid>
                                </Grid>
                            : <Loading containerStyle={{minHeight: 160}}/>}
                        </Grid>
                    </Grid>
                    : null}
                    {(!loadingTrendData && !loadingGrowthData && populationTrendData.length === 0) ? <Box className='SectionEmpty'>
                        {'Insufficient amount of data for this species to generate trend charts.'}
                    </Box>
                    :null}
                </Grid>
            </Grid>
        </Box>
    )
}

export default NationalTrendSection
