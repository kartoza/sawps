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
import { DEFAULT_START_YEAR_FILTER, DEFAULT_END_YEAR_FILTER } from '../../../reducers/SpeciesFilter';


interface NationalTrendSectionInterface {
    species: string;
}

const SPECIES_POPULATION_TREND_URL = '/api/species/population_trend/'

interface CategoryLabelInterface {
    [key: string]: string;
}

const getGrowthChartTitle = (species: string, cat_label: string, labels: CategoryLabelInterface) => {
    let _title = `${cat_label} ${species} Populations`
    if (cat_label in labels) {
        _title = _title + ` (${labels[cat_label]} individuals)`
    }
    return capitalizeSentence(_title)
}

const NationalTrendSection = (props: NationalTrendSectionInterface) => {
    const [populationTrendData, setPopulationTrendData] = useState<PopulationTrendItem[]>([])
    const [largePopulationGrowthData, setLargePopulationGrowthData] = useState<GrowthDataItem[]>([])
    const [mediumPopulationGrowthData, setMediumPopulationGrowthData] = useState<GrowthDataItem[]>([])
    const [smallPopulationGrowthData, setSmallPopulationGrowthData] = useState<GrowthDataItem[]>([])
    const [loadingTrendData, setLoadingTrendData] = useState(false)
    const [loadingGrowthData, setLoadingGrowthData] = useState(false)
    const [categoryLabels, setCategoryLabels] = useState<CategoryLabelInterface>({})
    const [growthPeriodCategories, setGrowthPeriodCategories] = useState<string[]>(null)
    const [growthPopChangeCategories, setGrowthPopChangeCategories] = useState<string[]>(null)

    const fetchNationalTrendData = (species: string) => {
        setLoadingTrendData(true)
        axios.get(`${SPECIES_POPULATION_TREND_URL}?species=${species}&level=national&data_type=trend`)
            .then((response) => {
            setLoadingTrendData(false)
            if (response.data['results']) {
                setPopulationTrendData(response.data['results'] as PopulationTrendItem[])
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
            let _data = response.data['results']
            if (_data) {
                let _large: GrowthDataItem[] = []
                let _medium: GrowthDataItem[] = []
                let _small: GrowthDataItem[] = []
                let _labels: CategoryLabelInterface = {}
                for (let i = 0; i < _data.length; i++) {
                    let _item = _data[i] as GrowthDataItem
                    if (_item.pop_size_cat === 'large') {
                        _large.push(_item)
                    } else if (_item.pop_size_cat === 'medium') {
                        _medium.push(_item)
                    } else if (_item.pop_size_cat === 'small') {
                        _small.push(_item)
                    }
                    if (_item.pop_size_cat_label) {
                        _labels[_item.pop_size_cat] = _item.pop_size_cat_label
                    }
                }
                setLargePopulationGrowthData(_large)
                setMediumPopulationGrowthData(_medium)
                setSmallPopulationGrowthData(_small)
                let _metadata = response.data['metadata']
                let _periodCategories = 'period' in _metadata ? _metadata['period'] : null
                let _popChangeCategories = 'pop_change_cat' in _metadata ? _metadata['pop_change_cat'] : null
                setGrowthPeriodCategories(_periodCategories)
                setGrowthPopChangeCategories(_popChangeCategories)
                setCategoryLabels(_labels)
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
                                    <AreaAvailableLineChart />
                                </Grid>
                            </Grid>
                        </Grid>
                        <Grid item sm={12} md={12} lg={7}>
                            {!loadingGrowthData ?
                                <Grid container flexDirection={'column'} spacing={1}>
                                    <Grid item>
                                        <GroupedGrowthChart chartId='large-national-growth-chart' title={getGrowthChartTitle(props.species, 'large', categoryLabels)} data={largePopulationGrowthData} periodCategories={growthPeriodCategories} popChangeCategories={growthPopChangeCategories} />
                                    </Grid>
                                    <Grid item>
                                        <GroupedGrowthChart chartId='medium-national-growth-chart' title={getGrowthChartTitle(props.species, 'medium', categoryLabels)} data={mediumPopulationGrowthData} periodCategories={growthPeriodCategories} popChangeCategories={growthPopChangeCategories} />
                                    </Grid>
                                    <Grid item>
                                        <GroupedGrowthChart chartId='small-national-growth-chart' title={getGrowthChartTitle(props.species, 'small', categoryLabels)} data={smallPopulationGrowthData} periodCategories={growthPeriodCategories} popChangeCategories={growthPopChangeCategories} />
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
