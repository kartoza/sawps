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
import Tooltip from '@mui/material/Tooltip';
import Topper from "../Data/Topper";

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
    // downloading charts
    const contentRefAllCharts = useRef(null);
    const contentRefPopulationTrend = useRef(null);
    const contentRefPopulationCategory = useRef(null);
    const contentRefPropertyType = useRef(null);
    const contentRefPopulationDensity = useRef(null);
    const contentRefProvinceCount = useRef(null);
    const contentRefProvinceCountPercentage = useRef(null);
    const contentRefTotalCountPerActivity = useRef(null);
    const contentRefTotalCountPerActivityPercentage = useRef(null);
    const contentRefPopulationEstimateCategoryCount = useRef(null);
    const contentRefPopulationEstimateCategoryCountPercentage = useRef(null);
    const contentRefPropertyAvailable = useRef(null);
    const contentRefAgeGroup = useRef(null);
    const contentRefAreaAvailable = useRef(null);
    const topperRef = useRef(null);

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

    const imageUrl = 'http://localhost:8000/static/images/icons/download.svg';

    // Get the current window location (i.e., the full URL)
    let currentLocation = window.location.href;

    // Remove '/charts' from the current URL
    currentLocation = currentLocation.replace('/charts', '');

    // Replace 'localhost:8000' with the current full URL
    const imageUrlWithDomain = imageUrl.replace('http://localhost:8000', currentLocation);

    const informationIconUrl = 'http://localhost:8000/static/images/icons/information.svg';

    // Replace 'localhost:8000' with the current full URL
    const informationIconUrlWithDomain = informationIconUrl.replace('http://localhost:8000', currentLocation);


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

    const handleDownloadPdf = async () => {
        setIconsHidden(true);
        const content = contentRefAllCharts.current;
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
        setIconsHidden(false);
    }


    // Check if the user's roles allow them to view charts
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


    const [iconsHidden, setIconsHidden] = useState(false);

    
    const handleDownload = async (contentRef: any) => {
        setIconsHidden(true);
        const content = contentRef.current;
        const topperContent = topperRef.current;
        
        if (!content || !topperContent) return;
        
        const totalHeight = content.scrollHeight;
        const windowHeight = window.innerHeight;
        const pdf = new jsPDF();
        const pdfWidth = pdf.internal.pageSize.getWidth();
        
        let pdf_name = selectedSpecies + '.pdf';
        
        for (let offsetY = 0; offsetY < totalHeight; offsetY += windowHeight) {
          await new Promise((resolve) => setTimeout(resolve, 50));
          
          const scale = 8; // Adjust the scale as needed (higher values result in higher quality)
          
          // Define html2canvas options for better quality
          const canvas = await html2canvas(content, {
            scale: scale, // Increase the scale for better quality
            windowWidth: window.innerWidth,
            width: content.scrollWidth,
            height: content.scrollHeight,
          });
          
          const topperCanvas = await html2canvas(topperContent, {
            scale: scale, // Increase the scale for better quality
            windowWidth: window.innerWidth,
            width: topperContent.scrollWidth,
            height: topperContent.scrollHeight,
          });
      
          const topperImageDataUrl = topperCanvas.toDataURL('image/jpeg', 1.0);
          const imageDataUrl = canvas.toDataURL('image/jpeg', 1.0); // Adjust the quality (1.0 is maximum)
          const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
          
          // Add a header to the PDF
          pdf.addImage(topperImageDataUrl, 'JPEG', 0, 0, pdfWidth, (topperCanvas.height * pdfWidth) / topperCanvas.width);
      
          // Add the chart to the PDF
          pdf.addImage(imageDataUrl, 'JPEG', 0, (topperCanvas.height * pdfWidth) / topperCanvas.width, pdfWidth, pdfHeight);
        }
        
        pdf.save(pdf_name);
        setIconsHidden(false);
      };
      
    

    

    return (
        <Box>
            <Box className="charts-container">
                

                {showCharts ? (
                    
                        <Grid container spacing={2} ref={contentRefAllCharts}>
                            <div ref={topperRef}>
                                <Topper title="SAWPS CHARTS SUMMARY" on_charts={true}/>
                            </div>

                            {/* {
                            canViewPopulationTrend && 
                            selectedSpecies && 
                            hasEmptyPopulationTrend && 
                            (
                                <Grid item xs={12} md={6} ref={contentRefPopulationTrend}>
                                    <PopulationTrend 
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear} 
                                        loading={loading} 
                                        setLoading={setLoading}
                                        onEmptyDatasets={handleEmptyPopulationTrend}
                                    />
                            {iconsHidden ? null : ( 
                                    <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                        <Tooltip title="Information Tooltip" arrow placement="top">
                                            <img
                                            src={informationIconUrlWithDomain}
                                            alt="Information Icon"
                                            width="24"
                                            height="24"
                                            />
                                        </Tooltip>

                                        <div
                                            onClick={() => {
                                                handleDownload(contentRefPopulationTrend);
                                            }}
                                            style={{ cursor: 'pointer' }}
                                        >
                                            <img
                                            src={imageUrlWithDomain}
                                            alt="Image Icon"
                                            width="24"
                                            height="24"
                                            />
                                        </div>
                                    </div>
                                )}
                                </Grid>
                            )} */}



                            {
                            canViewPopulationCategory && 
                            selectedSpecies && 
                            hasEmptyPopulationCategory && (
                                <Grid item xs={12} md={6} ref={contentRefPopulationCategory}>
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

                            {iconsHidden ? null : ( 
                                    <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                        {/* Information Icon with Tooltip */}
                                        <Tooltip title="Information Tooltip" arrow placement="top">
                                            <img
                                            src={informationIconUrlWithDomain}
                                            alt="Information Icon"
                                            width="24"
                                            height="24"
                                            />
                                        </Tooltip>

                                        {/* Image for Download */}
                                        <div
                                            onClick={() => {
                                                handleDownload(contentRefPopulationCategory);
                                            }}
                                            style={{ cursor: 'pointer' }}
                                        >
                                            <img
                                            src={imageUrlWithDomain}
                                            alt="Image Icon"
                                            width="24"
                                            height="24"
                                            />
                                        </div>
                                    </div>
                                )}
                                </Grid>
                            )}

                             {
                             canViewPropertyType && 
                             hasEmptyPropertyType && (
                                <Grid item xs={12} md={6} ref={contentRefPropertyType}>
                                    <PropertyTypeBarChart 
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear} 
                                        loading={loading} 
                                        setLoading={setLoading}
                                        onEmptyDatasets={handleEmptyPropertyType}
                                    />
                                    {iconsHidden ? null : ( 
                                    <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                        {/* Information Icon with Tooltip */}
                                        <Tooltip title="Information Tooltip" arrow placement="top">
                                            <img
                                            src={informationIconUrlWithDomain}
                                            alt="Information Icon"
                                            width="24"
                                            height="24"
                                            />
                                        </Tooltip>

                                        {/* Image for Download */}
                                        <div
                                            onClick={() => {
                                                handleDownload(contentRefPropertyType);
                                            }}
                                            style={{ cursor: 'pointer' }}
                                        >
                                            <img
                                            src={imageUrlWithDomain}
                                            alt="Image Icon"
                                            width="24"
                                            height="24"
                                            />
                                        </div>
                                    </div>
                                    )}
                                </Grid>
                            )}

                            
                            {
                            canViewDensityBar && 
                            selectedSpecies && 
                            hasEmptyDensity && (
                                <Grid item xs={12} md={6} ref={contentRefPopulationDensity}>
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
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefPopulationDensity);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
                                </Grid>
                            )}


                            
                            {
                            canViewPropertyAvailable && 
                            selectedSpecies && 
                            hasEmptyPropertyAvailable && (
                                <Grid item xs={12} md={6} ref={contentRefPropertyAvailable}>
                                    <PropertyAvailableBarChart 
                                        selectedSpecies={selectedSpecies} 
                                        propertyId={propertyId} 
                                        startYear={startYear} 
                                        endYear={endYear} 
                                        loading={loading} 
                                        setLoading={setLoading}
                                        onEmptyDatasets={handleEmptyPropertyAvailable}
                                    /> 
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefPropertyAvailable);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
                                </Grid>
                            )}


                            
                            {
                            canViewAgeGroup && 
                            ageGroupData.map((data) => (
                                <Grid container key={data.id} item xs={12} md={6} ref={contentRefAgeGroup}>
                                    <AgeGroupBarChart
                                        loading={loading}
                                        ageGroupData={data?.age_group}
                                        icon={data?.graph_icon}
                                        colour={data?.colour}
                                        name={data?.common_name_varbatim}
                                    />
                                    {iconsHidden ? null : ( 
                                    <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end',marginLeft: '400px'}}>
                                        {/* Information Icon with Tooltip */}
                                        <Tooltip title="Information Tooltip" arrow placement="top">
                                            <img
                                            src={informationIconUrlWithDomain}
                                            alt="Information Icon"
                                            width="24"
                                            height="24"
                                            />
                                        </Tooltip>

                                        {/* Image for Download */}
                                        <div
                                            onClick={() => {
                                                handleDownload(contentRefAgeGroup);
                                            }}
                                            style={{ cursor: 'pointer' }}
                                        >
                                            <img
                                            src={imageUrlWithDomain}
                                            alt="Image Icon"
                                            width="24"
                                            height="24"
                                            />
                                        </div>
                                    </div>
                                    )}
                                </Grid>
                            ))}
                           

                            
                            {
                            canViewAreaAvailable && 
                            areaData.map((data, index) => (
                                <Grid container key={index} item xs={12} md={6} ref={contentRefAreaAvailable}>
                                    {data?.area?.owned_species ? (
                                        <AreaAvailableLineChart
                                            loading={loading}
                                            areaData={data?.area?.owned_species}
                                            species_name={data?.common_name_varbatim}
                                        />
                                    ) : null}
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' ,marginLeft: '400px'}}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefAreaAvailable);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
                                </Grid>
                            ))}
                            

                            {
                            canViewProvinceSpeciesCount && 
                            selectedSpecies && 
                            hasEmptyProvinceCount && (
                                <Grid item xs={12} md={6} ref={contentRefProvinceCount}>
                                    <SpeciesCountPerProvinceChart
                                        selectedSpecies={selectedSpecies}
                                        propertyId={propertyId}
                                        startYear={startYear}
                                        endYear={endYear}
                                        loading={loading}
                                        setLoading={setLoading}
                                        onEmptyDatasets={handleEmptyProvinceCount}
                                    />
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefProvinceCount);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
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
                                    ref={contentRefProvinceCountPercentage}
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
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefProvinceCountPercentage);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
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
                                    ref={contentRefTotalCountPerActivity}
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
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefTotalCountPerActivity);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
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
                                    ref={contentRefTotalCountPerActivityPercentage}
                                >
                                    <ActivityCountAsPercentage
                                        selectedSpecies={selectedSpecies}
                                        startYear={startYear} 
                                        endYear={endYear}
                                        loading={loading} 
                                        activityData={totalCoutData}
                                        onEmptyDatasets={handleEmptyTotalCountPerActivityPercentage}
                                    />
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefTotalCountPerActivityPercentage);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
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
                                    ref={contentRefPopulationEstimateCategoryCount}
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
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefPopulationEstimateCategoryCount);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
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
                                    ref={contentRefPopulationEstimateCategoryCountPercentage}
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
                                    {iconsHidden ? null : ( 
                                        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                                            {/* Information Icon with Tooltip */}
                                            <Tooltip title="Information Tooltip" arrow placement="top">
                                                <img
                                                src={informationIconUrlWithDomain}
                                                alt="Information Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </Tooltip>

                                            {/* Image for Download */}
                                            <div
                                                onClick={() => {
                                                    handleDownload(contentRefPopulationEstimateCategoryCountPercentage);
                                                }}
                                                style={{ cursor: 'pointer' }}
                                            >
                                                <img
                                                src={imageUrlWithDomain}
                                                alt="Image Icon"
                                                width="24"
                                                height="24"
                                                />
                                            </div>
                                        </div>
                                    )}
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
