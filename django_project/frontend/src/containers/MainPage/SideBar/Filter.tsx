import React, { useEffect, useState } from 'react';
import axios from "axios";
import {
    Box,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Checkbox,
    Accordion,
    AccordionSummary,
    Typography,
    AccordionDetails,
    Chip,
    IconButton,
    SelectChangeEvent,
    FormControlLabel,
} from '@mui/material';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';
import { RootState } from '../../../app/store';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import Slider from '@mui/material/Slider';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import CloseIcon from '@mui/icons-material/Close';
import Loading from '../../../components/Loading';
import SpeciesLayer from '../../../models/SpeciesLayer';
import { selectedPropertyId, setEndYear, setSpeciesFilter, setStartYear, toggleSpecies } from '../../../reducers/SpeciesFilter';
import './index.scss';
import PropertyInterface from '../../../models/Property';

const yearRangeStart = 1960;
const yearRangeEnd = 2023;
const FETCH_AVAILABLE_SPECIES = '/species/'
const FETCH_PROPERTY_LIST_URL = '/api/property/list/'


function Filter() {
    const dispatch = useAppDispatch()
    const SpeciesFilterList = useAppSelector((state: RootState) => state.SpeciesFilter.SpeciesFilterList)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [loading, setLoading] = useState(false)
    const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
    const [selectedSpecies, setSelectedSpecies] = useState<string[]>([]);
    const [propertyList, setPropertyList] = useState<PropertyInterface[]>([])
    const [selectedProperty, setSelectedProperty] = useState([]);
    const [localStartYear, setLocalStartYear] = useState(startYear);
    const [localEndYear, setLocalEndYear] = useState(endYear);

    const marks = [
        {
            value: startYear,
            label: `${startYear}`,
        },
        {
            value: endYear,
            label: `${endYear}`,
        },
    ];

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

    const handleSpectialFilterOption = (each: string, event: any) => {
        event.stopPropagation();
        if (selectedOptions.includes(each)) {
            setSelectedOptions(selectedOptions.filter((selected) => selected !== each));
        } else {
            setSelectedOptions([...selectedOptions, each]);
        }
    };

    const handleArrowClick = (id: number) => {
        const _updatedData = filterlList.map((item: any) => {
            if (id === item.id) {
                item.isSelected = !item.isSelected
            }
            return item;
        });
        setFilterList(_updatedData)
    }

    const handleChange = (event: any, newValue: number | number[]) => {
        if (Array.isArray(newValue)) {
            dispatch(setStartYear(newValue[0]));
            dispatch(setEndYear(newValue[1]));
        }
    };

    const fetchSpeciesList = () => {
        setLoading(true)
        axios.get(FETCH_AVAILABLE_SPECIES).then((response) => {
            setLoading(false)
            if (response.data) {
                let _species = response.data as SpeciesLayer[]
                _species = _species.map((species) => {
                    return species
                })
                dispatch(setSpeciesFilter(_species))
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    const fetchPropertyList = () => {
        setLoading(true)
        axios.get(FETCH_PROPERTY_LIST_URL).then((response) => {
            setLoading(false)
            if (response.data) {
                setPropertyList(response.data as PropertyInterface[])
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchSpeciesList();
        fetchPropertyList();
    }, [])

    const handleDeleteSpecies = (valueToDelete: string) => {
        const updatedSelectedSpecies = selectedSpecies.filter((item) => item !== valueToDelete);
        setSelectedSpecies(updatedSelectedSpecies);
    }
    const handleSelectedSpecies = (value: string) => () => {
        const updatedSelectedSpecies = selectedSpecies.includes(value)
            ? selectedSpecies.filter((item) => item !== value)
            : [...selectedSpecies, value];
        setSelectedSpecies(updatedSelectedSpecies);
    };

    useEffect(() => {
        dispatch(toggleSpecies(selectedSpecies.length > 0 ? selectedSpecies.join(',') : ''));
    }, [selectedSpecies])

    const handleDeleteProperty = (idToDelete: number) => () => {
        const updatedSelectedProperty = selectedProperty.filter((id) => id !== idToDelete);
        setSelectedProperty(updatedSelectedProperty);
    };

    const handleSelectedProperty = (id: number) => () => {
        const propertyExists = selectedProperty.includes(id);
        if (propertyExists) {
            const updatedSelectedProperty = selectedProperty.filter((item) => item !== id);
            setSelectedProperty(updatedSelectedProperty);
        } else {
            const updatedSelectedProperty = [...selectedProperty, id];
            setSelectedProperty(updatedSelectedProperty);
        }
    };

    useEffect(() => {

        dispatch(selectedPropertyId(selectedProperty.length > 0 ? selectedProperty.join(',') : ''));
    }, [selectedProperty])

    const handleStartYearChange = (value: string) => {
        const newValue = parseInt(value, 10);
        setLocalStartYear(newValue);
        if (newValue < yearRangeStart && newValue > yearRangeEnd) {
            dispatch(setStartYear(yearRangeStart));
        } else {
            dispatch(setStartYear(newValue));
        }
    }

    const handleEndYearChange = (value: string) => {
        const newValue = parseInt(value, 10);
        setLocalEndYear(newValue);
        if (newValue < yearRangeStart && newValue > yearRangeEnd) {
            dispatch(setEndYear(yearRangeEnd));
        } else {
            dispatch(setEndYear(newValue));
        }
    }
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
                    <img src="/static/images/propertyIcon.png" alt='Property image' />
                    <Typography color='#75B37A' fontSize='medium'>Property</Typography>
                </Box>
                <List className='ListItem' component="nav" aria-label="">
                    {loading ? <Loading /> :
                        <Accordion>
                            <AccordionSummary expandIcon={<ArrowDropDownIcon />}>
                                {selectedProperty.length > 0 ? (
                                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                        {selectedProperty.map((id) => {
                                            const property = propertyList.find((item) => item.id === id);
                                            return (
                                                <Chip
                                                    key={id}
                                                    label={property ? property.name : ''}
                                                    onDelete={handleDeleteProperty(id)}
                                                    deleteIcon={<CloseIcon />}
                                                    sx={{ margin: 0.5 }}
                                                />
                                            );
                                        })}
                                    </Box>
                                ) : (
                                    <Typography>Select</Typography>
                                )}
                            </AccordionSummary>
                            <AccordionDetails>
                                <Box className="selectBox">
                                    <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                                        {propertyList.map((property: any) => (
                                            <FormControlLabel
                                                key={property.name}
                                                control={
                                                    <Checkbox
                                                        checked={selectedProperty.includes(property.id)}
                                                        onChange={handleSelectedProperty(property.id)}
                                                    />
                                                }
                                                label={property.name}
                                            />
                                        ))}
                                    </Box>
                                </Box>
                            </AccordionDetails>
                        </Accordion>
                    }
                </List>
                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/species/elephant.png" alt='species image' />
                    <Typography color='#75B37A' fontSize='medium'>Species</Typography>
                </Box>
                <List className='ListItem' component="nav" aria-label="">
                    {loading ? <Loading /> :
                        <Accordion>
                            <AccordionSummary expandIcon={<ArrowDropDownIcon />}>
                                {selectedSpecies.length > 0 ? (
                                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                        {selectedSpecies.map((value) => (
                                            <Chip
                                                key={value}
                                                label={value}
                                                onDelete={() => handleDeleteSpecies(value)}
                                                deleteIcon={<CloseIcon />}
                                                sx={{ margin: 0.5 }}
                                            />
                                        ))}
                                    </Box>
                                ) : (
                                    <Typography>Select</Typography>
                                )}
                            </AccordionSummary>
                            <AccordionDetails>
                                <Box className="selectBox">
                                    <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                                        {SpeciesFilterList.map((species: any) => (
                                            <FormControlLabel
                                                key={species.common_name_varbatim}
                                                control={
                                                    <Checkbox
                                                        checked={selectedSpecies.includes(species.common_name_varbatim)}
                                                        onChange={handleSelectedSpecies(species.common_name_varbatim)}
                                                    />
                                                }
                                                label={species.common_name_varbatim}
                                            />
                                        ))}
                                    </Box>
                                </Box>
                            </AccordionDetails>
                        </Accordion>
                    }
                </List>
                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/watchIcon.png" alt='watch image' />
                    <Typography color='#75B37A' fontSize='medium'>Year</Typography>
                </Box>
                <Box className='sliderYear'>
                    <Slider
                        value={[startYear, endYear]}
                        onChange={handleChange}
                        valueLabelDisplay="auto"
                        min={yearRangeStart}
                        max={yearRangeEnd}
                        marks={marks}
                    />
                </Box>

                <Box className='formboxInput'>
                    <Box className='form-inputFild'>
                        <TextField type="number" size='small' value={localStartYear} onChange={(e) => handleStartYearChange(e.target.value)} />
                        <Typography className='formtext'>From</Typography>
                    </Box>
                    <Box className='form-inputFild right-flids'>
                        <TextField type="number" size='small' value={localEndYear} onChange={(e) => handleEndYearChange(e.target.value)} />
                        <Typography className='formtext'>To</Typography>
                    </Box>
                </Box>

                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/FilterIcon.png" alt='Filter image' />
                    <Typography color='#75B37A' fontSize='medium'>Spatial filters</Typography>
                </Box>
                <Box>
                    <div className='sidebarArrowsBox'>
                        <ul>
                            {filterlList.map((item: any) => (
                                <li key={item.id} onClick={() => handleArrowClick(item.id)}>
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
                                                                    onClick={(event) => handleSpectialFilterOption(each, event)}
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
        </Box >
    )
}

export default Filter;
