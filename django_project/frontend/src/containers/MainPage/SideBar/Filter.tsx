import React, {useEffect, useState} from 'react';
import {v4 as uuidv4} from 'uuid';
import axios from "axios";
import Grid from "@mui/material/Grid";
import {Autocomplete, Box, TextField, Typography,} from '@mui/material';
import Tooltip from '@mui/material/Tooltip';
import List from '@mui/material/List';
import CircularProgress from '@mui/material/CircularProgress';
import SearchIcon from '@mui/icons-material/Search';
import {RootState} from '../../../app/store';
import {useAppDispatch, useAppSelector} from '../../../app/hooks';
import Slider from '@mui/material/Slider';
import Loading from '../../../components/Loading';
import {
    selectedActivityId,
    selectedActivityName,
    selectedOrganisationId,
    selectedOrganisationName,
    selectedPropertyId,
    selectedPropertyName,
    setActivityCount,
    setEndYear,
    setOrganisationCount,
    setPropertyCount,
    setSelectedInfoList,
    setSpatialFilterValues,
    setStartYear,
    toggleSpecies,
    toggleSpeciesList,
    setSelectedProvinceName,
    DEFAULT_START_YEAR_FILTER,
    DEFAULT_END_YEAR_FILTER
} from '../../../reducers/SpeciesFilter';
import './index.scss';
import {MapEvents} from '../../../models/Map';
import {triggerMapEvent} from '../../../reducers/MapState';
import SpatialFilter from "./SpatialFilter";
import {
    Activity,
    Organisation,
    Property,
    Province,
    useGetActivityQuery,
    useGetOrganisationQuery,
    useGetPropertyQuery,
    useGetSpeciesQuery,
    useGetUserInfoQuery,
    useGetProvinceQuery, UserInfo
} from "../../../services/api";
import {isMapDisplayed} from "../../../utils/Helpers";
import Button from "@mui/material/Button";
import {AutoCompleteCheckbox} from "../../../components/SideBar/index";
import {SeachPlaceResult} from '../../../utils/SearchPlaces';
import SearchPlace from '../../../components/SearchPlace';

const yearRangeStart = DEFAULT_START_YEAR_FILTER;
const yearRangeEnd = DEFAULT_END_YEAR_FILTER;
const FETCH_PROPERTY_DETAIL_URL = '/api/property/detail/'

function Filter(props: any) {
    const dispatch = useAppDispatch()
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [loading, setLoading] = useState(false)
    const [selectedSpecies, setSelectedSpecies] = useState<string>('');
    const [selectedProperty, setSelectedProperty] = useState([]);
    const [selectedProvince, setSelectedProvince] = useState([]);
    const [selectedActivity, setSelectedActivity] = useState<number[]>([]);
    const [localStartYear, setLocalStartYear] = useState(startYear);
    const [localEndYear, setLocalEndYear] = useState(endYear);
    const [selectedInfo, setSelectedInfo] = useState<string[]>(['Species report']);
    const [selectedOrganisation, setSelectedOrganisation] = useState([]);
    const [tab, setTab] = useState<string>('')
    const startYearDisabled = ['map', 'charts'].includes(tab);
    const [searchSpeciesList, setSearchSpeciesList] = useState([])
    const [selectedSpeciesList, setSelectedSpeciesList] = useState<string[]>([]);
    const [allowPropertiesSelection, setPropertiesSelection] = useState(false)
    const [allowOrganisationSelection, setOrganisationSelection] = useState(false)
    const [shownPropertyOptions, setShownPropertyOptions] = useState([])
    const [provinceOptions, setProvinceOptions] = useState([])
    const isStartYearValid = localStartYear >= yearRangeStart && localStartYear <= yearRangeEnd
    const isEndYearValid = localEndYear >= yearRangeStart && localEndYear <= yearRangeEnd
    const { data: userInfoData, isLoading, isSuccess } = useGetUserInfoQuery()
    const {
        data: organisationList,
        isLoading: isOrganisationLoading,
        isSuccess: isOrganisationSuccess
    } = useGetOrganisationQuery()
    const {
        data: activityList,
        isLoading: isActivityLoading,
        isSuccess: isActivitySuccess
    } = useGetActivityQuery()
    const {
        data: propertyList,
        isLoading: isPropertyLoading,
        isSuccess: isPropertySuccess
    } = useGetPropertyQuery(selectedOrganisation.join(','))
    const {
        data: SpeciesFilterList,
        isLoading: isSpeciesLoading,
        isSuccess: isSpeciesSuccess
    } = useGetSpeciesQuery(selectedOrganisation.join(','))
    const {
        data: provinceList,
        isLoading: isProvinceListLoading,
        isSuccess: isProvinceListSuccess
    } = useGetProvinceQuery()

    type Information = {
        id?: string,
        name?: string
    }
    let informationList: Information[] = []

    const roleExists = (role: string) => {
        if (!userInfoData || !userInfoData.user_roles) return false;
        return userInfoData.user_roles.includes(role);
    }

    if (userInfoData) {
        informationList = [
            {
                id: "Activity report",
                name: "Activity report",
            },
            {
                id: "Property report",
                name: "Property report"
            },
            {
                id: "Species report",
                name: "Species report"
            }
        ]

        if (userInfoData.user_permissions.includes("Can view province report")
          && !roleExists('Provincial data consumer')) {
            informationList.push({
                id: "Province report",
                name: "Province report"
            })
        }

        if (userInfoData.user_permissions.includes("Can view sampling report")) {
            informationList.push({
                id: "Sampling report",
                name: "Sampling report"
            })
        }
        informationList = informationList.sort((a, b) => a.id > b.id ? 1 : -1)
    }

    // Select all organisations by default
    useEffect(() => {
        if (organisationList) {
            setSelectedOrganisation(organisationList.map((organisation: Organisation) => organisation.id))
        }
    }, [organisationList]);

    // Select all province by default
    useEffect(() => {
        if (provinceList) {
            setProvinceOptions(provinceList.map((province: Province) => {
                return {
                    id: province.name,
                    name: province.name
                }
            }))
            setSelectedProvince(provinceList.map((province: Province) => province.name))
        }
    }, [provinceList]);

    useEffect(() => {
        if (propertyList) {
            if (selectedOrganisation.length === 0 && selectedProvince.length === 0) {
                setShownPropertyOptions([])
                setSelectedProperty([])
            } else {
                setShownPropertyOptions(propertyList.map(property => {
                    return {
                        id: property.id,
                        name: `${property.name} (${property.short_code})`
                    }
                }))
                setSelectedProperty(propertyList.map(property => property.id))
            }
        }
    }, [propertyList])

    // Select all activities by default
    useEffect(() => {
        if (activityList) {
            setSelectedActivity([])
        }
    }, [activityList]);

    // intial map state vars for zoom out
    const center = [25.86, -28.52]; // Center point in backend
    const width = 10;
    const height = 10;

     // Calculate the bounding box
    const halfWidth = width / 2;
    const halfHeight = height / 2;
    const boundingBox = [
        center[0] - halfWidth,
        center[1] - halfHeight,
        center[0] + halfWidth,
        center[1] + halfHeight,
    ];

    useEffect(() => {
        const pathname = window.location.pathname.replace(/\//g, '');
        if (pathname !== 'trends') {
            setSelectedProvince([])
        } else {
            setSelectedProvince(provinceOptions.map((province: Province) => province.name))
        }
        setTab(pathname)
    }, [window.location.pathname])

    const handleChange = (event: any, newValue: number | number[]) => {
        if (Array.isArray(newValue)) {
            setLocalStartYear((startYearDisabled? localStartYear : newValue[0]))
            dispatch(setStartYear(startYearDisabled? localStartYear : newValue[0]));
            setLocalEndYear((newValue[1]))
            dispatch(setEndYear(newValue[1]));
        }
    };

    const handleSelectedSpecies = (value: string) => {
        setSelectedSpecies(value);
    };

    useEffect(() => {
        setLocalStartYear(startYear)
    }, [startYear])

    useEffect(() => {
        if (selectedSpeciesList.length === 0 && selectedSpecies !== "") {
            setSelectedSpeciesList([selectedSpecies])
        }
        dispatch(toggleSpecies(selectedSpecies));
    }, [selectedSpecies])

    useEffect(() => {
        dispatch(toggleSpeciesList(selectedSpeciesList.join(',')));
    }, [selectedSpeciesList])

    useEffect(() => {
        const values = selectedInfo.join(',')
        dispatch(setSelectedInfoList(values));
    }, [selectedInfo])

    const mergeBoundingBoxes = (boundingBoxes: number[][]): number[] => {
        let minLeft: number = 180;
        let minBottom: number = 90;
        let maxRight: number = -180;
        let maxTop: number = -90;

        boundingBoxes.forEach(([left, bottom, right, top]) => {
          if (left < minLeft) minLeft = left;
          if (bottom < minBottom) minBottom = bottom;
          if (right > maxRight) maxRight = right;
          if (top > maxTop) maxTop = top;
        });

        return [minLeft, minBottom, maxRight, maxTop];
      };


    const zoomToCombinedBoundingBox = async (propertyIds: number[]) => {

        try {
          const propertyBoundingBoxes: number[][] = [];

          // Fetch and collect bounding boxes for each property
          await Promise.all(
            propertyIds.map(async (propertyId) => {
              const response = await axios.get(`${FETCH_PROPERTY_DETAIL_URL}${propertyId}/`);
              if (response.data && response.data.bbox && response.data.bbox.length === 4) {
                propertyBoundingBoxes.push(response.data.bbox);
              }
            })
          );

          if (propertyBoundingBoxes.length > 0) {
            // Merge the collected bounding boxes
            const combinedBoundingBox = mergeBoundingBoxes(propertyBoundingBoxes);


            adjustMapToBoundingBox(combinedBoundingBox)
          } else {
            console.error('No valid bounding boxes found for selected properties.');
          }

          setLoading(false);
        } catch (error) {
          setLoading(false);
          console.error(error);
        }
      };

      const adjustMapToBoundingBox = (boundingBox: any[]) => {
        dispatch(
            triggerMapEvent({
                id: uuidv4(),
                name: MapEvents.PROPERTY_SELECTED,
                date: Date.now(),
                payload: boundingBox.map(String),
            })
        );
      };

    useEffect(() => {
        if (propertyList) {
            dispatch(selectedPropertyId(selectedProperty.join(',')));
            const selectedPropertyNames = propertyList.filter(
              propertyObj => selectedProperty.includes(propertyObj.id)
            ).map(propertyObj => propertyObj.name)
            dispatch(selectedPropertyName(selectedPropertyNames.length > 0 ? selectedPropertyNames.join(', ') : ''));
            dispatch(setPropertyCount(selectedProperty.length));
        }
    }, [selectedProperty])

    useEffect(() => {
       setSelectedProperty(shownPropertyOptions.map(property => property.id))
    }, [shownPropertyOptions]);

    useEffect(() => {
        if (provinceList) {
            dispatch(setSelectedProvinceName(selectedProvince.join(',')));

            if (propertyList) {
                if (selectedOrganisation.length === 0 && selectedProvince.length === 0) {
                    setShownPropertyOptions([])
                } else {
                    console.debug(shownPropertyOptions.length)
                    let newPropertyOptions = propertyList;
                    if (tab === 'trends') {
                        newPropertyOptions = newPropertyOptions.filter(property =>
                            selectedProvince.includes(property.province)
                        )
                    }
                    // @ts-ignore
                    newPropertyOptions = newPropertyOptions.map(property => {
                        return {
                            id: property.id,
                            name: `${property.name} (${property.short_code})`
                        }
                    })

                    setShownPropertyOptions(newPropertyOptions)
                }
            }
        }
    }, [selectedProvince])

    useEffect(() => {
        if (organisationList) {
            dispatch(selectedOrganisationId(selectedOrganisation.join(',')))
            const selectedOrganisationNames = organisationList.filter(
              organisationObj => selectedOrganisation.includes(organisationObj.id)
            ).map(organisationObj => organisationObj.name)
            dispatch(selectedOrganisationName(selectedOrganisationNames.length > 0 ? selectedOrganisationNames.join(', ') : ''));
            dispatch(setOrganisationCount(selectedOrganisation.length));
        }
    }, [selectedOrganisation])

    useEffect(() => {
        if (activityList) {
            dispatch(selectedActivityId(selectedActivity.join(',')));
            const selectedActivityNames = activityList.filter(
              activityObj => selectedActivity.includes(activityObj.id)
            ).map(activityObj => activityObj.name)
            dispatch(selectedActivityName(selectedActivityNames.length > 0 ? selectedActivityNames.join(',') : ''));
            dispatch(setActivityCount(selectedActivity.length));
        }
    }, [selectedActivity])

    const handleStartYearChange = (value: string) => {
        const newValue = parseInt(value, 10);
        setLocalStartYear(newValue);
        if (newValue >= yearRangeStart && newValue <= yearRangeEnd) {
            dispatch(setStartYear(newValue));
        }
    }

    const handleEndYearChange = (value: string) => {
        const newValue = parseInt(value, 10);
        setLocalEndYear(newValue);
        if (newValue >= yearRangeStart && newValue <= yearRangeEnd) {
            dispatch(setEndYear(newValue));
        }
    }

    const clearFilter = () => {
        if (allowOrganisationSelection) {
            setSelectedOrganisation([]);
            setShownPropertyOptions([]);
        }
        setSelectedProperty([])
        setSelectedSpecies('')
        setSelectedSpeciesList([])
        setSelectedActivity([])
        setSelectedInfo([])
        setLocalStartYear(yearRangeStart)
        setLocalEndYear(yearRangeEnd)
        dispatch(setStartYear(yearRangeStart));
        dispatch(setEndYear(yearRangeEnd));
    }

    const organisationInputField = () => {
        return (
          <Box>
            <Box className='sidebarBoxHeading'>
                <img src="/static/images/organisation.svg" alt='Organisation image' />
                <Typography color='#75B37A' fontSize='medium'>Organisation</Typography>
            </Box>
            <List className='ListItem' component="nav" aria-label="">
                {loading || isLoading || isOrganisationLoading? <Loading /> :
                    <AutoCompleteCheckbox
                        options={organisationList}
                        selectedOption={selectedOrganisation}
                        singleTerm={'Organisation'}
                        pluralTerms={'Organisations'}
                        setSelectedOption={setSelectedOrganisation}
                      />
                }
            </List>
        </Box>)
    }

    const propertyInputField = () => {
        return (
            <Tooltip
                title={selectedOrganisation.length === 0 ? "Select Organisation to show Property options!" : ""}
                placement="top-start"
            >
                <Box>
                    <Box className='sidebarBoxHeading'>
                        <img src="/static/images/Property.svg" alt='Property image' />
                        <Typography color='#75B37A' fontSize='medium'>Property</Typography>
                    </Box>
                    <List className='ListItem' component="nav" aria-label="">
                        {loading || isPropertyLoading ? (
                            <Loading />
                        ) : (
                            <AutoCompleteCheckbox
                                options={shownPropertyOptions}
                                selectedOption={selectedOrganisation.length > 0 ? selectedProperty : []}
                                singleTerm={'Property'}
                                pluralTerms={'Properties'}
                                setSelectedOption={(newValues) => {
                                    setSelectedProperty(newValues)
                                    if (newValues.length === 0) {
                                        adjustMapToBoundingBox(boundingBox)
                                    } else {
                                        // Call zoomToCombinedBoundingBox with the updated list of selected properties
                                        zoomToCombinedBoundingBox(newValues);
                                    }
                                }}
                            />
                        )}
                    </List>
                </Box>
            </Tooltip>
        )
    }

    useEffect(() => {
        if (SpeciesFilterList) {
            const sList: any = []
            SpeciesFilterList.map((item: any) => {
                sList.push(item.scientific_name)
            })
            if (selectedOrganisation.length === 0) {
                setSearchSpeciesList([])
            } else {
                setSearchSpeciesList(sList)
            }
        }
    }, [SpeciesFilterList])

    useEffect(() => {
        if (!isSuccess) return;

        if (userInfoData.user_permissions.includes("Can view organisation filter")) {
            setOrganisationSelection(true);
        }

        if (userInfoData.user_permissions.includes("Can view property filter")) {
            setPropertiesSelection(true);
        }
    }, [isSuccess, userInfoData]);

    return (
        <Box sx={{position: 'relative'}}>
            {isLoading ?
                <div
                    className='sidepanel-loading-container'
                >
                    <CircularProgress color="inherit" />
                </div> : null }
            <Grid container>
                <Grid item xs={12} md={12} lg={12}>
                    <Box className='sidebarBox' style={{ marginTop: 10 }}>
                <Box className='clear-button-container'>
                    <Button onClick={clearFilter}>Clear All</Button>
                </Box>
                {isMapDisplayed() && (
                <Box style={{marginTop: '5%', marginBottom: '10%'}} >
                    <Box className="sidebarBoxHeading" style={{ display: 'flex', alignItems: 'center', marginBottom: '15px'}}>
                        <SearchIcon
                            style={{
                                color: '#70B276',
                            }}
                        />
                        <Typography color='#75B37A' fontSize='medium'>Search place</Typography>
                    </Box>
                    <SearchPlace onPlaceSelected={(place: SeachPlaceResult) => {
                        if (place && place.bbox && place.bbox.length === 4) {
                            // trigger zoom to property
                            let _bbox = place.bbox.map(String)
                            dispatch(triggerMapEvent({
                                'id': uuidv4(),
                                'name': MapEvents.ZOOM_INTO_PROPERTY,
                                'date': Date.now(),
                                'payload': _bbox
                            }))
                        }
                    }} />
                </Box>
                )}

                <Tooltip
                  title={selectedOrganisation.length === 0 ? "Select Organisation to show Species options!" : ""}
                  placement="top-start"
                >
                    <Box>
                        <Box className='sidebarBoxHeading'>
                            <img src="/static/images/species/Elephant.svg" alt='species image' />
                            <Typography color='#75B37A' fontSize='medium'>Species</Typography>
                        </Box>
                        <List className='ListItem' component="nav" aria-label="">
                            {loading || isSpeciesLoading ? <Loading /> :
                                tab !== 'reports' ? (
                                    <Autocomplete
                                        id="combo-box-demo"
                                        disableClearable={true}
                                        value={selectedSpecies}
                                        options={searchSpeciesList}
                                        sx={{ width: '100%' }}
                                        onChange={(event, value) => handleSelectedSpecies(value)}
                                        renderInput={(params) => <TextField {...params} placeholder="Select" />}
                                    />
                                ) : (
                                    <AutoCompleteCheckbox
                                        options={searchSpeciesList.map((species) => {
                                            return {
                                                'id': species,
                                                'name': species
                                            }
                                        })}
                                        selectedOption={selectedSpeciesList}
                                        singleTerm={'Species'}
                                        pluralTerms={'Species'}
                                        setSelectedOption={setSelectedSpeciesList}
                                    />
                                )
                            }
                        </List>
                    </Box>
                </Tooltip>

                {tab === 'reports' &&
                    <Box>
                        <Box className='sidebarBoxHeading'>
                            <img src="/static/images/Information.svg" alt='Info image' />
                            <Typography color='#75B37A' fontSize='medium'>Report Type</Typography>
                        </Box>
                        <List className='ListItem' component="nav" aria-label="">
                            {loading ? <Loading /> :
                              (
                                <AutoCompleteCheckbox
                                    options={informationList}
                                    selectedOption={selectedInfo}
                                    singleTerm={'Report'}
                                    pluralTerms={'Reports'}
                                    setSelectedOption={setSelectedInfo}
                                  />
                              )
                            }
                        </List>
                    </Box>
                }

                {
                    allowOrganisationSelection && organisationInputField()
                }

                {
                    tab === 'trends' &&
                  <Tooltip
                    title={""}
                    placement="top-start"
                  >
                    <Box>
                        <Box className='sidebarBoxHeading'>
                            <img src="/static/images/Property.svg" alt='Property image' />
                            <Typography color='#75B37A' fontSize='medium'>Province</Typography>
                        </Box>
                        <List className='ListItem' component="nav" aria-label="">
                            {loading || isProvinceListLoading ? (
                                <Loading />
                            ) : (
                              <AutoCompleteCheckbox
                                options={provinceOptions}
                                selectedOption={selectedProvince}
                                singleTerm={'Province'}
                                pluralTerms={'Provinces'}
                                setSelectedOption={(newValues) => {
                                    setSelectedProvince(newValues)
                                }}
                              />
                            )}
                        </List>
                    </Box>
                  </Tooltip>
                }

                {
                    allowPropertiesSelection && propertyInputField()
                }

                {tab !== 'trends' &&
                    <Box>
                      <Box className='sidebarBoxHeading'>
                          <img src="/static/images/Clock.svg" alt='watch image'/>
                          <Typography color='#75B37A' fontSize='medium'>Year</Typography>
                      </Box>
                      <Box className='sliderYear'>
                          <Slider
                            value={[startYear, endYear]}
                            onChange={handleChange}
                            valueLabelDisplay="auto"
                            min={yearRangeStart}
                            max={yearRangeEnd}
                            style={{color: 'black'}}
                          />
                      </Box>

                      <Box className='formboxInput'>
                          <Box className='form-inputFild'>
                            <Tooltip
                                title={isStartYearValid ? '' : `Year should range from ${yearRangeStart} to ${yearRangeEnd}`}
                                placement="top-start"
                              >
                                  <TextField
                                    type="number" size='small' value={localStartYear}
                                    onChange={(e: any) => handleStartYearChange(e.target.value)}
                                    className={isStartYearValid ? '': 'yearFilter-red'}
                                    disabled={startYearDisabled}
                                  />
                            </Tooltip>
                            <Typography className='formtext'>From</Typography>
                          </Box>
                          <Box className='form-inputFild right-flids'>
                              <Tooltip
                                title={isEndYearValid ? '' : `Year should range from ${yearRangeStart} to ${yearRangeEnd}`}
                                placement="top-start"
                              >
                                  <TextField type="number" size='small' value={localEndYear}
                                             onChange={(e: any) => handleEndYearChange(e.target.value)}
                                             className={isEndYearValid ? '': 'yearFilter-red'}
                                  />
                              </Tooltip>
                              <Typography className='formtext'>To</Typography>
                          </Box>
                      </Box>
                </Box>
                }

                {tab !== 'trends' &&
                   <Box>
                        <Box className='sidebarBoxHeading'>
                            <img src="/static/images/Activity.svg" alt='Property image' />
                            <Typography color='#75B37A' fontSize='medium'>Activity</Typography>
                        </Box>
                        <List className='ListItem' component="nav" aria-label="">
                            {loading || isActivityLoading ? <Loading /> :
                                (
                                    <AutoCompleteCheckbox
                                        options={activityList}
                                        selectedOption={selectedActivity}
                                        singleTerm={'Activity'}
                                        pluralTerms={'Activities'}
                                        setSelectedOption={setSelectedActivity}
                                      />
                                )
                            }
                        </List>
                    </Box>
                }

                {tab !== 'trends' &&
                  <Box>
                      <Box className='sidebarBoxHeading'>
                          <img src="/static/images/Layers.svg" alt='Filter image'/>
                          <Typography color='#75B37A' fontSize='medium'>Spatial filters</Typography>
                      </Box>
                      <Box>
                          <SpatialFilter loading={loading}
                                         onSpatialFilterValuesUpdate={(spatialFilterValues: string[]) =>
                                           dispatch(setSpatialFilterValues(spatialFilterValues))}/>
                      </Box>
                  </Box>
                }
            </Box>
                </Grid>
            </Grid>
        </Box >
    )
}


export default Filter;
