import React, { useEffect, useState } from 'react';
import axios from "axios";
import Box from "@mui/material/Box";
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';
import { RootState } from '../../../app/store';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { Typography } from '@mui/material';
import Slider from '@mui/material/Slider';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import Loading from '../../../components/Loading';
import SpeciesLayer from '../../../models/SpeciesLayer';
import { setSpeciesFilter, toggleSpecies } from '../../../reducers/SpeciesFilter';
import './index.scss';

export interface FILTEERSPECIES {
    id: number
}
const FETCH_AVAILABLE_SPECIES = '/species/'
const yearRangeStart = 2010;
const yearRangeEnd = 2023;
const marks = [
    {
        value: yearRangeStart,
        label: `${yearRangeStart}`,
    },
    {
        value: yearRangeEnd,
        label: `${yearRangeEnd}`,
    },
];

function Filter() {
    const dispatch = useAppDispatch()
    const SpeciesFilterList = useAppSelector((state: RootState) => state.SpeciesFilter.SpeciesFilterList)
    const [loading, setLoading] = useState(false)
    const [value, setValue] = useState<number[]>([yearRangeStart, yearRangeEnd]);
    const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
    const [filterlList, setFilterList] = useState([
        {
            "id": 1,
            "name": "Population Category",
            "isSelected": false,
            "filterData": ['0-10', '11-20', '21-50', '50-100', '101-200', '>200']
        },
        {
            "id": 2,
            "name": "Protected Area",
            "isSelected": false,
            "filterData": ['National Park', 'Heritage sight', 'Nature Reserve']
        },
        {
            "id": 3,
            "name": "Activity",
            "isSelected": false,
            "filterData": ['Hunting', 'Poaching', 'Import', 'Export', 'Translocation', 'Contraseption']
        },
        {
            "id": 4,
            "name": "Critical biodiversity areas",
            "isSelected": false,
            "filterData": ['Critical biodiversity area ', 'Critical biodiversity area 1', 'Critical biodiversity area 2', 'Ecological support area', 'Ecological support area 1']
        },
        {
            "id": 5,
            "name": "Ecosystem type",
            "isSelected": false
        }
    ])

    const handleSpectialFilterOption = (each:string,event:any) => {
        event.stopPropagation();
        if (selectedOptions.includes(each)) {
            setSelectedOptions(selectedOptions.filter((selected) => selected !== each));
          } else {
            setSelectedOptions([...selectedOptions, each]);
          }
    };

    const handleArrowClick = (id: number,index:number) => {
        const _updatedData = filterlList.map((item: any) => {
            if (id === item.id) {
                item.isSelected = !item.isSelected
            }
            return item;
        });
        setFilterList(_updatedData)
    }


    const handleChange = (newValue: number | number[]) => {
        setValue(newValue as number[]);
    };
    const months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
    ];
    const [monthList, setMonthList] = useState(Array(months.length).fill(false));

    const handleisMonthCheck = (index: number) => {
        const updatedIsMonth = [...monthList];
        updatedIsMonth[index] = !updatedIsMonth[index];
        setMonthList(updatedIsMonth);
        if (updatedIsMonth[index]) {
            const selectedMonth = months[index];
        }
    };

    const fetchSpeciesList = () => {
        setLoading(true)
        axios.get(FETCH_AVAILABLE_SPECIES).then((response) => {
            setLoading(false)
            if (response.data) {
                let _species = response.data as SpeciesLayer[]
                _species = _species.map((species) => {
                    species.isSelected = false
                    return species
                })
                dispatch(setSpeciesFilter(_species))
            }
        })
    }

    useEffect(() => {
        fetchSpeciesList()
    }, [])

    return (
        <Box>
            <Box className='searchBar'>
                <TextField
                    variant="outlined"
                    placeholder="Keyword"
                    InputProps={{
                        endAdornment: (
                            <InputAdornment position="end">
                                <SearchIcon />
                            </InputAdornment>
                        ),
                    }}
                />
            </Box>
            <Box className='sidebarBox'>
                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/species/elephant.png" alt='species image' />
                    <Typography color='#75B37A' fontSize='medium'>Species</Typography>
                </Box>
                <List className='ListItem' component="nav" aria-label="">
                    {loading ? <Loading /> :
                        SpeciesFilterList.map((species, index) => {
                            const speciesId = `checkbox-list-label-${species.id}`;
                            return (
                                <ListItemButton
                                    key={species.id}
                                    disabled={loading}
                                    onClick={(event) => dispatch(toggleSpecies(species.id))}
                                    className='ListItemButton'
                                >
                                    <ListItemIcon>
                                        <Checkbox
                                            edge="start"
                                            checked={species?.isSelected}
                                            tabIndex={-1}
                                            disableRipple
                                            inputProps={{ 'aria-labelledby': speciesId }}
                                        />
                                    </ListItemIcon>
                                    <ListItemText id={speciesId} primary={species.common_name_varbatim} />
                                </ListItemButton>
                            )
                        })
                    }
                </List>
                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/watchIcon.png" alt='watch image' />
                    <Typography color='#75B37A' fontSize='medium'>Year</Typography>
                </Box>
                <Box className='sliderYear'>
                    <Slider
                        value={value}
                        onChange={(e: any) => handleChange(e)}
                        valueLabelDisplay="auto"
                        min={yearRangeStart}
                        max={yearRangeEnd}
                        marks={marks}
                    />
                </Box>
                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/Calender-logo.png" alt='calender image' />
                    <Typography color='#75B37A' fontSize='medium'>Year</Typography>
                </Box>
                <List className='ListItem' component="nav" aria-label="">
                    {loading ? <Loading /> :
                        months.map((month, index) => {
                            const monthId: string = `checkbox-list-label-${index}`;
                            return (
                                <ListItemButton
                                    key={index}
                                    disabled={loading}
                                    onClick={(event) => handleisMonthCheck(index)}
                                    className='ListItemButton'
                                >
                                    <ListItemIcon>
                                        <Checkbox
                                            edge="start"
                                            checked={monthList[index]}
                                            tabIndex={-1}
                                            disableRipple
                                            inputProps={{ 'aria-labelledby': monthId }}
                                        />
                                    </ListItemIcon>
                                    <ListItemText id={monthId} primary={month} />
                                </ListItemButton>
                            )
                        })
                    }
                </List>
                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/FilterIcon.png" alt='Filter image' />
                    <Typography color='#75B37A' fontSize='medium'>Spatial filters</Typography>
                </Box>
                <Box>
                    <div className='sidebarArrowsBox'>
                        <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
                            {filterlList.map((item: any,index:number) => (
                                <li key={item.id} onClick={() => handleArrowClick(item.id,index)}>
                                    <div style={{ display: 'flex', alignItems: 'center' }}>
                                        {item.isSelected ? <ArrowDropDownIcon /> : <ArrowRightIcon />}
                                        <span>{item.name}</span>
                                    </div>
                                    {item.isSelected && (
                                        <List component="nav" aria-label="">
                                            {loading ? (
                                                <Loading />
                                            ) : (
                                                item?.filterData?.map((each: string, index: number) => {
                                                    const filterId: string = `checkbox-list-label-${index}`;
                                                    return (
                                                        <ListItemButton
                                                            key={index}
                                                            disabled={loading}
                                                            className='ListItemButton'
                                                        >
                                                            <ListItemIcon>
                                                                <Checkbox
                                                                    edge="start"
                                                                    checked={selectedOptions.includes(each)}
                                                                    tabIndex={-1}
                                                                    disableRipple
                                                                    inputProps={{ 'aria-labelledby': filterId }}
                                                                    onClick={(event) => handleSpectialFilterOption(each,event)}
                                                                />
                                                            </ListItemIcon>
                                                            <ListItemText id={filterId} primary={each} />
                                                        </ListItemButton>
                                                    );
                                                })
                                            )}
                                        </List>
                                    )}
                                </li>
                            ))}
                        </ul>
                    </div>
                </Box>

            </Box>
        </Box>
    )

}


export default Filter;
