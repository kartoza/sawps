import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import axios from "axios";
import {
    Box,
    Checkbox,
    Accordion,
    AccordionSummary,
    Typography,
    AccordionDetails,
    Chip,
    FormControlLabel,
    Radio,
    InputBase,
} from '@mui/material';
import List from '@mui/material/List';
import MenuItem from '@mui/material/MenuItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import Autocomplete from '@mui/material/Autocomplete';
import { debounce } from '@mui/material/utils';
import SearchIcon from '@mui/icons-material/Search';
import { RootState } from '../../../app/store';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import Slider from '@mui/material/Slider';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import CloseIcon from '@mui/icons-material/Close';
import Loading from '../../../components/Loading';
import SpeciesLayer from '../../../models/SpeciesLayer';
import { selectedOrganisationId, selectedPropertyId, setEndYear, setSelectedInfoList, setSpeciesFilter, setStartYear, toggleSpecies } from '../../../reducers/SpeciesFilter';
import './index.scss';
import PropertyInterface from '../../../models/Property';
import { MapEvents } from '../../../models/Map';
import { triggerMapEvent } from '../../../reducers/MapState';
import Select, { SelectChangeEvent } from '@mui/material/Select';

const yearRangeStart = 1960;
const yearRangeEnd = new Date().getFullYear();
const FETCH_AVAILABLE_SPECIES = '/species/'
const FETCH_PROPERTY_LIST_URL = '/api/property/list/'
const SEARCH_PROPERTY_URL = '/api/property/search'
const FETCH_ORGANISATION_LIST_URL = '/api/organisation/'

interface SearchPropertyResult {
    name: string;
    bbox: any;
    id: string;
    type: string;
    fclass?: string;
}

// Define geocoding service URL and API key/token to allow searching places
const GEOCODING_API_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places';
const GEOCODING_API_KEY = 'your-geocoding-api-key';

// function to perform geocoding
const geocode = async (query: string | number | boolean) => {
    try {
        const response = await axios.get(`${GEOCODING_API_URL}/${encodeURIComponent(query)}.json`, {
            params: {
                access_token: GEOCODING_API_KEY,
                types: 'place', // Specify the types of results you want (e.g., 'place' for locations/places)
            },
        });

        return response.data.features;
    } catch (error) {
        console.error('Geocoding error:', error);
        return [];
    }
};
  

function Filter() {
    const dispatch = useAppDispatch()
    const SpeciesFilterList = useAppSelector((state: RootState) => state.SpeciesFilter.SpeciesFilterList)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [loading, setLoading] = useState(false)
    const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
    const [selectedSpecies, setSelectedSpecies] = useState<string>('');
    const [propertyList, setPropertyList] = useState<PropertyInterface[]>([])
    const [selectedProperty, setSelectedProperty] = useState([]);
    const [localStartYear, setLocalStartYear] = useState(startYear);
    const [localEndYear, setLocalEndYear] = useState(endYear);
    const [selectedInfo, setSelectedInfo] = useState<string>('');
    const [userRole, setUserRole] = useState<string>('');
    const [searchOpen, setSearchOpen] = useState(false)
    const [searchInputValue, setSearchInputValue] = useState('')
    const [searchResults, setSearchResults] = useState<SearchPropertyResult[]>([])
    const [organisationList, setOrganisationList] = useState([]);
    const [selectedOrganisation, setSelectedOrganisation] = useState([]);
    const [tab, setTab] = useState<string>('')
    const [searchSpeciesList, setSearchSpeciesList] = useState([])
    const [filterlList, setFilterList] = useState([
        {
            "id": 3,
            "name": "Activity",
            "isSelected": false,
            "filterData": ['Hunting', 'Poaching', 'Import', 'Export', 'Translocation', 'Contraseption']
        },
        {
            "id": 5,
            "name": "Biome type",
            "isSelected": false
        },
        {
            "id": 4,
            "name": "Critical biodiversity areas",
            "isSelected": false,
            "filterData": ['Critical biodiversity area ', 'Critical biodiversity area 1', 'Critical biodiversity area 2', 'Ecological support area', 'Ecological support area 1']
        },
        {
            "id": 2,
            "name": "Protected Area",
            "isSelected": false,
            "filterData": ['National Park', 'Heritage sight', 'Nature Reserve']
        },
        {
            "id": 1,
            "name": "Population Category",
            "isSelected": false,
            "filterData": ['0-10', '11-20', '21-50', '50-100', '101-200', '>200']
        }
    ])

    const informationList = [
        "Activity report",
        "Property report",
        userRole === "National data consumer" ? "Province report" : userRole === "Regional data consumer" ? "" : "Sampling Report",
        "Species report",
    ].filter(item => item !== "")

    useEffect(() => {
        const storedUserRole = localStorage.getItem('user_role');
        setUserRole(storedUserRole);
    }, []);

    useEffect(() => {
        const pathname = window.location.pathname.replace(/\//g, '');
        setTab(pathname)
    }, [window.location.pathname])

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
            setLocalStartYear((newValue[0]))
            dispatch(setStartYear(newValue[0]));
            setLocalEndYear((newValue[1]))
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
    const fetchOrganisationList = () => {
        setLoading(true)
        axios.get(FETCH_ORGANISATION_LIST_URL).then((response) => {
            setLoading(false)
            if (response.data) {
                setOrganisationList(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        fetchSpeciesList();
        fetchPropertyList();
        fetchOrganisationList();
    }, [])

    const handleSelectedSpecies = (value: string) => {
        setSelectedSpecies(value);
    };

    useEffect(() => {
        dispatch(toggleSpecies(selectedSpecies));
    }, [selectedSpecies])

    const handleSelectedInfo = (e: SelectChangeEvent) => {
        setSelectedInfo(e.target.value);
    };

    useEffect(() => {
        dispatch(setSelectedInfoList(selectedInfo));
    }, [selectedInfo])


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

    const handleSelectedOrganisation = (id: number) => () => {
        const organisationExists = selectedOrganisation.includes(id);
        if (organisationExists) {
            const updatedSelectedOrganisation = selectedOrganisation.filter((item) => item !== id);
            setSelectedOrganisation(updatedSelectedOrganisation);
        } else {
            const updatedSelectedOrganisation = [...selectedOrganisation, id];
            setSelectedOrganisation(updatedSelectedOrganisation);
        }
    };

    useEffect(() => {
        dispatch(selectedOrganisationId(selectedOrganisation.length > 0 ? selectedOrganisation.join(',') : ''));
    }, [selectedOrganisation])

    const handleStartYearChange = (value: string) => {
        const newValue = parseInt(value, 10);
        setLocalStartYear(newValue);
        if (newValue < yearRangeStart || newValue > yearRangeEnd) {
            setTimeout(() => {
                setLocalStartYear(yearRangeStart)
                dispatch(setStartYear(yearRangeStart));
            }, 3000);
        } else {
            dispatch(setStartYear(newValue));
        }
    }

    const handleEndYearChange = (value: string) => {
        const newValue = parseInt(value, 10);
        setLocalEndYear(newValue);
        if (newValue > yearRangeEnd || newValue < yearRangeStart) {
            setTimeout(() => {
                setLocalEndYear(yearRangeEnd);
                dispatch(setEndYear(yearRangeEnd));
            }, 3000);
        } else {
            dispatch(setEndYear(newValue));
        }
    }

    const searchProperty = React.useMemo(
        () =>
            debounce(
                (
                    request: { input: string },
                    callback: (results?: any) => void,
                ) => {
                    let _queryParam = `search_text=${request.input}`
                    axios.get(`${SEARCH_PROPERTY_URL}?${_queryParam}`).then(
                        response => {
                            callback(response)
                        }
                    ).catch(error => {
                        console.log('Failed search property ', error)
                        callback(null)
                    })
                },
                400,
            ),
        [],
    )

    useEffect(() => {
        let active = true;
        if (searchInputValue.length <= 1) {
            setSearchResults([])
            return undefined;
        }
        searchProperty({ input: searchInputValue }, (results: any) => {
            if (active) {
                if (results) {
                    setSearchResults(results.data as SearchPropertyResult[])
                } else {
                    setSearchResults([])
                }
            }
        })
        return () => {
            active = false
        };
    }, [searchInputValue, searchProperty])

    useEffect(() => {
        setSearchOpen(searchInputValue.length > 1)
        if (searchInputValue.length <= 1) {
            setSearchResults([])
        }
    }, [searchInputValue])

    const handleSelectAllProperty = () => {
        const propeertyId = propertyList.map(property => property.id)
        setSelectedProperty(propeertyId)
        if (selectedProperty.length === propertyList.length) {
            setSelectedProperty([]);
        }
    }

    const handleSelectAllOrganisation = () => {
        const organisationId = organisationList.map(data => data.id)
        setSelectedOrganisation(organisationId)
        if (selectedOrganisation.length === organisationList.length) {
            setSelectedOrganisation([]);
        }
    }


    useEffect(() => {
        const sList: any = []
        SpeciesFilterList.map((item: any) => {
            sList.push(item.scientific_name)
        })
        setSearchSpeciesList(sList)
    }, [SpeciesFilterList])

    // Geocode function for searching properties
    const geocodeProperty = async (query: string | number | boolean) => {
        try {
          const results = await geocode(query);
      
          if (results.length > 0) {
            const firstResult = results[0];
            const bbox = firstResult.bbox;
      
            // Trigger zoom to property
            const payload = bbox.map(String);
            dispatch(triggerMapEvent({
              id: uuidv4(),
              name: MapEvents.ZOOM_INTO_PROPERTY,
              date: Date.now(),
              payload,
            }));
      
            setSearchInputValue('');
          }
        } catch (error) {
          console.error('Geocoding property error:', error);
        }
      };

      const handleAutocompleteChange = (event: React.ChangeEvent<{}>, newValue: SearchPropertyResult | string) => {
        if (typeof newValue === 'string') {
            // Likely a place name, trigger geocoding for place search
            geocode(newValue)
                .then((results) => {
                    if (results.length > 0) {
                        const firstResult = results[0];
                        const bbox = firstResult.bbox;
                        // Trigger zoom to place
                        const payload = bbox.map(String);
                        dispatch(
                            triggerMapEvent({
                                id: uuidv4(),
                                name: MapEvents.ZOOM_INTO_PLACE,
                                date: Date.now(),
                                payload,
                            })
                        );
                    }
                })
                .catch((error) => {
                    console.error('Geocoding place error:', error);
                });
        } else {
            // trigger geocoding for property search
            geocodeProperty(newValue.name);
        }
    };

    const getOptionLabel = (option: SearchPropertyResult | string) => {
        if (typeof option === 'string') {
            // If it's a string, return it as-is (the input value)
            return option;
        } else {
            // If it's a SearchPropertyResult, return the label with fclass (if available)
            return option.fclass ? `${option.name} (${option.fclass})` : option.name;
        }
    };
    
   
    
    
      

    return (
        <Box>
            <Box className='searchBar'>
                {/* Autocomplete for Property Search */}
                <Autocomplete
                id="search-property-autocomplete"
                open={searchOpen}
                onOpen={() => setSearchOpen(searchInputValue.length > 1)}
                onClose={() => setSearchOpen(false)}
                options={searchResults}
                getOptionLabel={getOptionLabel}
                renderInput={(params) => (
                    <TextField
                    variant="outlined"
                    placeholder="Search Properties"
                    {...params}
                    InputProps={{
                        ...params.InputProps,
                        endAdornment: (
                        <InputAdornment position="end">
                            <SearchIcon />
                        </InputAdornment>
                        ),
                    }}
                    />
                )}
                onChange={handleAutocompleteChange}
                onInputChange={(_, newInputValue) => {
                    setSearchInputValue(newInputValue);
                }}
                filterOptions={(x) => x}
                isOptionEqualToValue={(option, value) => {
                    if (typeof option === 'string' || typeof value === 'string') {
                        return option === value;
                    } else {
                        return option.id === value.id;
                    }
                }}
                />
                {/* End Autocomplete for Property Search */}

            </Box>
            <Box className='sidebarBox'>
                {(userRole === "National data scientist" || userRole === "Regional data scientist") && <Box>
                    <Box className='sidebarBoxHeading'>
                        <img src="/static/images/organisation.svg" alt='Organisation image' />
                        <Typography color='#75B37A' fontSize='medium'>Organisation</Typography>
                    </Box>
                    <List className='ListItem' component="nav" aria-label="">
                        {loading ? <Loading /> :
                            <Accordion>
                                <AccordionSummary expandIcon={<ArrowDropDownIcon />}>
                                    {selectedOrganisation.length > 0 ? (
                                        <Box >
                                            {`${selectedOrganisation.length} ${selectedOrganisation.length > 1 ? 'Organisations' : 'Organisation'} Selected`}
                                        </Box>
                                    ) : (
                                        <Typography>Select</Typography>
                                    )}
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Box className="selectBox">
                                        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                                            <FormControlLabel
                                                control={
                                                    <Checkbox
                                                        checked={selectedOrganisation.length === organisationList.length}
                                                        onChange={handleSelectAllOrganisation}
                                                    />
                                                }
                                                label="Select All"
                                            />
                                        </Box>
                                        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                                            {organisationList.map((data: any) => (
                                                <FormControlLabel
                                                    key={data.name}
                                                    control={
                                                        <Checkbox
                                                            checked={selectedOrganisation.includes(data.id)}
                                                            onChange={handleSelectedOrganisation(data.id)}
                                                        />
                                                    }
                                                    label={data.name}
                                                />
                                            ))}
                                        </Box>
                                    </Box>
                                </AccordionDetails>
                            </Accordion>
                        }
                    </List>
                </Box>
                }
                {tab === 'data' &&
                    <Box>
                        <Box className='sidebarBoxHeading'>
                            <img src="/static/images/Information.svg" alt='Info image' />
                            <Typography color='#75B37A' fontSize='medium'>Report Type</Typography>
                        </Box>
                        <List className='ListItem' component="nav" aria-label="">
                            {loading ? <Loading /> :
                                (
                                    <Select
                                        displayEmpty
                                        sx={{ width: '100%', textAlign: 'start' }}
                                        value={selectedInfo}
                                        onChange={handleSelectedInfo}
                                        renderValue={
                                            selectedInfo !== "" ? undefined : () => <div style={{ color: '#282829' }}>Select</div>
                                        }
                                    >
                                        {informationList.map((info: any, index) => (
                                            <MenuItem value={info} key={index}>{info}</MenuItem>
                                        ))}
                                    </Select>)
                            }
                        </List>
                    </Box>
                }
                {userRole != "National data consumer" &&
                    <Box>
                        <Box className='sidebarBoxHeading'>
                            <img src="/static/images/Property.svg" alt='Property image' />
                            <Typography color='#75B37A' fontSize='medium'>Property</Typography>
                        </Box>
                        <List className='ListItem' component="nav" aria-label="">
                            {loading ? <Loading /> :
                                <Accordion>
                                    <AccordionSummary expandIcon={<ArrowDropDownIcon />}>
                                        {selectedProperty.length > 0 ? (
                                            <Box>
                                                {`${selectedProperty.length} ${selectedProperty.length > 1 ? 'Properties' : 'Property'} Selected`}

                                            </Box>
                                        ) : (
                                            <Typography>Select</Typography>
                                        )}
                                    </AccordionSummary>
                                    <AccordionDetails>
                                        <Box className="selectBox">
                                            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                                                <FormControlLabel
                                                    control={
                                                        <Checkbox
                                                            checked={selectedProperty.length === propertyList.length}
                                                            onChange={handleSelectAllProperty}
                                                        />
                                                    }
                                                    label="Select All"
                                                />
                                            </Box>
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
                    </Box>
                }
                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/species/Elephant.svg" alt='species image' />
                    <Typography color='#75B37A' fontSize='medium'>Species</Typography>
                </Box>
                <List className='ListItem' component="nav" aria-label="">
                    {loading ? <Loading /> :
                        (
                            <Autocomplete
                                id="combo-box-demo"
                                disableClearable={true}
                                options={searchSpeciesList}
                                sx={{ width: '100%' }}
                                onChange={(event, value) => handleSelectedSpecies(value)}
                                renderInput={(params) => <TextField {...params} placeholder="Select" />}
                            />
                        )
                    }
                </List>
                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/Clock.svg" alt='watch image' />
                    <Typography color='#75B37A' fontSize='medium'>Year</Typography>
                </Box>
                <Box className='sliderYear'>
                    <Slider
                        value={[startYear, endYear]}
                        onChange={handleChange}
                        valueLabelDisplay="auto"
                        min={yearRangeStart}
                        max={yearRangeEnd}
                        style={{ color: 'black' }}
                    />
                </Box>

                <Box className='formboxInput'>
                    <Box className='form-inputFild'>
                        <TextField type="number" size='small' value={localStartYear} onChange={(e:any) => handleStartYearChange(e.target.value)} />
                        <Typography className='formtext'>From</Typography>
                    </Box>
                    <Box className='form-inputFild right-flids'>
                        <TextField type="number" size='small' value={localEndYear} onChange={(e:any) => handleEndYearChange(e.target.value)} />
                        <Typography className='formtext'>To</Typography>
                    </Box>
                </Box>

                <Box className='sidebarBoxHeading'>
                    <img src="/static/images/Layers.svg" alt='Filter image' />
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
