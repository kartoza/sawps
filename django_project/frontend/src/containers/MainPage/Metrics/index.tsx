import React, { useEffect, useRef, useState } from "react";
import { Box, Button, Grid, Typography } from "@mui/material";
import DensityBarChart from "./DensityBarChart";
import PopulationCategoryChart from "./PopulationCategoryChart";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import PropertyAvailableBarChart from "./PropertyAvailable";
import PropertyTypeBarChart from "./PropertyType";
import AgeGroupBarChart from "./AgeGroupBarChart";
import AreaAvailableLineChart from "./AreaAvailableLineChart";
import axios from "axios";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import SpeciesCountPerProvinceChart from "./SpeciesCountPerProvinceChart";
import SpeciesCountAsPercentage from "./SpeciesCountAsPercentage";
import TotalCountPerActivity from "./TotalCountPerActivity";
import ActivityCountAsPercentage from "./ActivityCountAsPercentage";
import PopulationEstimateCategoryCount from "./PopulationEstimateCategory";
import PopulationEstimateAsPercentage from "./PopulationEstimateCategoryAsPercentage";
import PopulationTrend from "./PopulationTrend";
import {
    useGetUserInfoQuery,
} from "../../../services/api";


const FETCH_POPULATION_AGE_GROUP = '/api/population-per-age-group/'
const FETCH_ACTIVITY_PERCENTAGE_URL = '/api/activity-percentage/'
const FETCH_ACTIVITY_TOTAL_COUNT = '/api/total-count-per-activity/'
const FETCH_PROPERTY_POPULATION_SPECIES = '/api/total-area-vs-available-area/'

const Metrics = () => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [loading, setLoading] = useState(false)
    const [activityData, setActivityData] = useState([])
    const [activityType, setActivityType] = useState({})
    const [totalCoutData, setTotalCountData] = useState([])
    const [ageGroupData, setAgeGroupData] = useState([])
    const labels = Object.keys(activityType);
    const totalCountLabel = labels.filter(item => item !== "Base population");
    const [areaData, setAreaData] = useState([])

    const [densityData, setDensityData] = useState([])
    const [populationData, setPopulationData] = useState([])
    const [speciesData, setSpeciesData] = useState([])
    const contentRef = useRef(null);

    // Declare errorMessage as a state variable
    const [showCharts, setShowCharts] = useState(false);

    const [hasEmptyPopulationTrend, setHasEmptyPopulationTrend] = useState(true);
    const [hasEmptyPopulationCategory, setHasEmptyPopulationCategory] = useState(true);
    const [hasEmptyPropertyType, setHasEmptyPropertyType] = useState(true);
    const [hasEmptyDensity, setHasEmptyDensity] = useState(true);
    const [hasEmptyProvinceCount, setHasEmptyProvinceCount] = useState(true);
    const [hasEmptyProvinceCountPercentage, setHasEmptyProvinceCountPercentage] = useState(true);
    const [hasEmptyTotalCountPerActivity, setHasEmptyTotalCountPerActivity] = useState(true);
    const [hasEmptyTotalCountPerActivityPercentage, setHasEmptyTotalCountPerActivityPercentage] = useState(true);
    const [hasEmptyPopulationEstimateCategoryCount, setHasEmptyPopulationEstimateCategoryCount] = useState(true);
    const [hasEmptyPopulationEstimateCategoryCountPercentage, setHasEmptyhasEmptyPopulationEstimateCategoryCountPercentage] = useState(true);
    const [hasEmptyPropertyAvailable, setHasEmptyPropertyAvailable] = useState(true);

    const { data: userInfoData, isLoading, isSuccess } = useGetUserInfoQuery();
    const [userRoles, setUserRoles] = useState([]);

    useEffect(() => {
        if (isSuccess) {
            // Preprocess user roles to make them lowercase and remove spaces
            setUserRoles(userInfoData?.user_roles.map((role) => role.toLowerCase().replace(/\s/g, '')) || []);
        }
    }, [isSuccess, userInfoData]);

    // Pass callback functions to each child component for the specific type
    const handleEmptyPopulationTrend = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyPopulationTrend(isEmpty);
    };
    const handleEmptyPopulationCategory = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyPopulationCategory(isEmpty);
    };
    const handleEmptyPropertyType = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyPropertyType(isEmpty);
    };
    const handleEmptyDensity = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyDensity(isEmpty);
    };
    const handleEmptyPropertyAvailable = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyPropertyAvailable(isEmpty);
    };
    const handleEmptyProvinceCount = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyProvinceCount(isEmpty);
    };
    const handleEmptyProvinceCountPercentage = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyProvinceCountPercentage(isEmpty);
    };
    const handleEmptyTotalCountPerActivity = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyTotalCountPerActivity(isEmpty);
    };
    const handleEmptyTotalCountPerActivityPercentage = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyTotalCountPerActivityPercentage(isEmpty);
    };
    const handleEmptyTopulationEstimateCategoryCount = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyPopulationEstimateCategoryCount(isEmpty);
    };
    const handleEmptyPopulationEstimateCategoryCountPercentage = (isEmpty: boolean | ((prevState: boolean) => boolean)) => {
        setHasEmptyhasEmptyPopulationEstimateCategoryCountPercentage(isEmpty);
    };

    const fetchActivityPercentageData = () => {
        setLoading(true)
        axios.get(`${FETCH_ACTIVITY_PERCENTAGE_URL}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                setActivityData(response.data.data)
                setActivityType(response.data.activity_colours)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    const fetchActivityTotalCount = () => {
        setLoading(true)
        axios.get(`${FETCH_ACTIVITY_TOTAL_COUNT}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                setTotalCountData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    const fetchPopulationAgeGroupData = () => {
        setLoading(true)
        axios.get(`${FETCH_POPULATION_AGE_GROUP}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                console.log('fetched data: ',response.data)
                setAgeGroupData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }


    const fetchAreaAvailableLineData = () => {
        setLoading(true)
        axios.get(`${FETCH_PROPERTY_POPULATION_SPECIES}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                setAreaData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        if(selectedSpecies){
            setShowCharts(true)
            fetchActivityPercentageData();
            fetchActivityTotalCount();
            fetchPopulationAgeGroupData();
            fetchAreaAvailableLineData();
        }else {
            setShowCharts(false);
        }
        // allow rerender
        setHasEmptyPopulationTrend(true)
        setHasEmptyPopulationCategory(true)
        setHasEmptyPropertyType(true)
        setHasEmptyDensity(true)
        setHasEmptyPropertyAvailable(true)
        setHasEmptyProvinceCountPercentage(true)
        setHasEmptyTotalCountPerActivity(true)
        setHasEmptyTotalCountPerActivityPercentage(true)
        setHasEmptyPopulationEstimateCategoryCount(true)
        setHasEmptyhasEmptyPopulationEstimateCategoryCountPercentage(true)
    }, [propertyId, startYear, endYear, selectedSpecies])

    // downloads all charts rendered on page
    const handleDownloadPdf = async () => {
        const content = contentRef.current;
        if (!content) return;
        const totalHeight = content.scrollHeight;
        const windowHeight = window.innerHeight;
        const pdf = new jsPDF();
        for (let offsetY = 0; offsetY < totalHeight; offsetY += windowHeight) {
            await new Promise((resolve) => setTimeout(resolve, 50));
            const canvas = await html2canvas(content);
            const imageDataUrl = canvas.toDataURL('image/png');
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
            pdf.addImage(imageDataUrl, 'PNG', 0, 0, pdfWidth, pdfHeight);
        }
        pdf.save('metrics.pdf');
    }

    // determines which role can see which charts on page
    const canViewPopulationTrend = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser', 'sanbiplatformadministrator'].includes(role)
    );
    const canViewPopulationCategory = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewPropertyType = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewDensityBar = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewPropertyAvailable = userRoles.some((role) =>
        ['datacontributor', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewAgeGroup = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewAreaAvailable = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewProvinceSpeciesCount = userRoles.some((role) =>
        ['nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewProvinceSpeciesCountAsPercentage = userRoles.some((role) =>
        ['nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewTotalCount = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewCountAsPercentage = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewPopulationEstimate= userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );
    const canViewPopulationEstimateAsPercentage = userRoles.some((role) =>
        ['datacontributor', 'nationaldatascientist', 'superuser','sanbiplatformadministrator'].includes(role)
    );

    return (
        <Box>
            <Box className="charts-container">

                {showCharts ? (
                        <Grid container spacing={2} ref={contentRef}>
                            {
                            canViewPopulationTrend && 
                            selectedSpecies && 
                            hasEmptyPopulationTrend && (
                                <Grid item xs={12} md={6}>
                                    <PopulationTrend 
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear} 
                                        loading={loading} 
                                        setLoading={setLoading}
                                        onEmptyDatasets={handleEmptyPopulationTrend}
                                    />
                                </Grid>
                            )}


                            {
                            canViewPopulationCategory && 
                            selectedSpecies && 
                            hasEmptyPopulationCategory && (
                                <Grid item xs={12} md={6}>
                                    <PopulationCategoryChart 
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear} 
                                        loading={loading} 
                                        setLoading={setLoading} 
                                        populationData={populationData} 
                                        setPopulationData={setPopulationData}
                                        onEmptyDatasets={handleEmptyPopulationCategory}
                                    />
                                </Grid>
                            )}

                             {
                             canViewPropertyType && 
                             hasEmptyPropertyType && (
                                <Grid item xs={12} md={6}>
                                    <PropertyTypeBarChart 
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear} 
                                        loading={loading} 
                                        setLoading={setLoading}
                                        onEmptyDatasets={handleEmptyPropertyType}
                                    />
                                </Grid>
                            )}

                            
                            {
                            canViewDensityBar && 
                            selectedSpecies && 
                            hasEmptyDensity && (
                                <Grid item xs={12} md={6}>
                                    <DensityBarChart 
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear} 
                                        loading={loading} 
                                        setLoading={setLoading} 
                                        densityData={densityData} 
                                        setDensityData={setDensityData}
                                        onEmptyDatasets={handleEmptyDensity}
                                    /> 
                                </Grid>
                            )}


                            
                            {
                            canViewPropertyAvailable && 
                            selectedSpecies && 
                            hasEmptyPropertyAvailable && (
                                <Grid item xs={12} md={6}>
                                    <PropertyAvailableBarChart 
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear} 
                                        loading={loading} 
                                        setLoading={setLoading}
                                        onEmptyDatasets={handleEmptyPropertyAvailable}
                                    /> 
                                </Grid>
                            )}


                            
                            {
                            canViewAgeGroup && 
                            ageGroupData.map((data) => (
                                <Grid container key={data.id} item xs={12} md={6}>
                                    <AgeGroupBarChart
                                        loading={loading}
                                        ageGroupData={data?.age_group}
                                        icon={data?.graph_icon}
                                        colour={data?.colour}
                                        name={data?.common_name_varbatim}
                                    />
                                </Grid>
                            ))}
                           

                            
                            {
                            canViewAreaAvailable && 
                            areaData.map((data, index) => (
                                <Grid container key={index} item xs={12} md={6}>
                                    {data?.area?.owned_species ? (
                                        <AreaAvailableLineChart
                                            loading={loading}
                                            areaData={data?.area?.owned_species}
                                            species_name={data?.common_name_varbatim}
                                        />
                                    ) : null}
                                </Grid>
                            ))}
                            

                            {
                            canViewProvinceSpeciesCount && 
                            selectedSpecies && 
                            hasEmptyProvinceCount && (
                                <Grid item xs={12} md={6}>
                                    <SpeciesCountPerProvinceChart
                                        selectedSpecies={selectedSpecies}
                                        propertyId={propertyId}
                                        startYear={startYear}
                                        endYear={endYear}
                                        loading={loading}
                                        setLoading={setLoading}
                                        onEmptyDatasets={handleEmptyProvinceCount}
                                    />
                                </Grid>
                            )}

                               
                            
                            {
                            canViewProvinceSpeciesCountAsPercentage && 
                            selectedSpecies && 
                            hasEmptyProvinceCountPercentage && (
                                <Grid item xs={12} md={6} 
                                    style={{ 
                                        textAlign: 'center', 
                                        display: 'flex', 
                                        alignItems: 'center', 
                                        justifyContent: 'center',
                                        maxHeight: '370px'
                                    }}
                                >
                                    <SpeciesCountAsPercentage
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear}
                                        loading={loading} 
                                        setLoading={setLoading}
                                        activityData={activityData}
                                        onEmptyDatasets={handleEmptyProvinceCountPercentage}
                                    />
                                </Grid>
                            )}

                                    
                            {
                            canViewTotalCount && 
                            selectedSpecies && 
                            hasEmptyTotalCountPerActivity && (
                                <Grid item xs={12} md={6}
                                    style={{ 
                                        textAlign: 'center', 
                                        display: 'flex', 
                                        alignItems: 'center', 
                                        justifyContent: 'center',
                                        maxHeight: '370px'
                                    }}
                                >
                                    <TotalCountPerActivity
                                        selectedSpecies={selectedSpecies}
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear}
                                        loading={loading} 
                                        activityData={totalCoutData}
                                        onEmptyDatasets={handleEmptyTotalCountPerActivity}
                                    />
                                </Grid>
                            )}

                            
                            {
                            canViewCountAsPercentage && 
                            selectedSpecies &&
                            hasEmptyTotalCountPerActivityPercentage && (
                                <Grid item xs={12} md={6}
                                    style={{ 
                                        textAlign: 'center', 
                                        display: 'flex', 
                                        alignItems: 'center', 
                                        justifyContent: 'center',
                                        maxHeight: '370px'
                                    }}
                                >
                                    <ActivityCountAsPercentage
                                        selectedSpecies={selectedSpecies}
                                        startYear={startYear} 
                                        endYear={endYear}
                                        loading={loading} 
                                        activityData={totalCoutData}
                                        onEmptyDatasets={handleEmptyTotalCountPerActivityPercentage}
                                    />
                                </Grid>
                                )}

                                
                            {
                            canViewPopulationEstimate && 
                            selectedSpecies && 
                            hasEmptyPopulationEstimateCategoryCount && (
                                <Grid item xs={12} md={6}
                                    style={{ 
                                        textAlign: 'center', 
                                        display: 'flex', 
                                        alignItems: 'center', 
                                        justifyContent: 'center',
                                        maxHeight: '370px'
                                    }}
                                >
                                    <PopulationEstimateCategoryCount
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear}
                                        loading={loading} 
                                        setLoading={setLoading}
                                        activityData={activityData}
                                        onEmptyDatasets={handleEmptyTopulationEstimateCategoryCount}
                                    />
                                </Grid>
                                )}
                           
                           
                            {
                            canViewPopulationEstimateAsPercentage && 
                            selectedSpecies && 
                            hasEmptyPopulationEstimateCategoryCountPercentage && (
                                <Grid item xs={12} md={6}
                                    style={{ 
                                        textAlign: 'center', 
                                        display: 'flex', 
                                        alignItems: 'center', 
                                        justifyContent: 'center',
                                        maxHeight: '370px'
                                    }}
                                >
                                    <PopulationEstimateAsPercentage
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear}
                                        loading={loading} 
                                        setLoading={setLoading}
                                        activityData={activityData}
                                        onEmptyDatasets={handleEmptyPopulationEstimateCategoryCountPercentage}
                                    />
                                </Grid>
                            )}

                    </Grid>
                ): (
                    // Render message to user
                    <Grid container justifyContent="center" alignItems="center" flexDirection={'column'}>
                        <Grid item>
                            <Typography variant="body1" color="textPrimary" style={{ fontSize: '20px', fontWeight: 'bold' }}>
                                Ready to explore?
                            </Typography>
                        </Grid>
                        <Grid>
                            <Typography variant="body1" color="textPrimary" style={{ fontSize: '16px', fontWeight: 'bold' }}>
                                Choose a species to view the data as charts.
                            </Typography>
                        </Grid>
                    </Grid>
                )}


        </Box>
            {/* for decision makers only */}
            {/* {userRole === 'decision maker' && (
                <GenerateChartImages />
            )} */}
            {showCharts && (
                <Box className="download-btn-box" style={{ position: 'fixed', bottom: '20px', right: '20px' }}>
                    <Button onClick={handleDownloadPdf} variant="contained" color="primary">
                        Download data visualizations
                    </Button>
                </Box>
            )}

        </Box>
    );
};

export default Metrics;
