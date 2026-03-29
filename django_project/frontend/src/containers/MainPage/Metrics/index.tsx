import React, {useEffect, useRef, useState} from "react";
import {Box, Button, Grid, Modal, Typography} from "@mui/material";
import {useAppSelector} from "../../../app/hooks";
import {RootState} from "../../../app/store";
import axios from "axios";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import SpeciesCountPerProvinceChart from "./SpeciesCountPerProvinceChart";
import TotalCountPerActivity from "./TotalCountPerActivity";
import PopulationEstimateCategoryCount from "./PopulationEstimateCategory";
import PropertyCountPerCategoryChart from "./PropertyCountPerCategory";
import {useGetActivityAsObjQuery, useGetPropertyTypeQuery, useGetUserInfoQuery} from "../../../services/api";
import Topper from "../Data/Topper";
import Loading from "../../../components/Loading";
import StandardDeviationMeanChart from "./StandardDeviationMeanChart";


const FETCH_ACTIVITY_PERCENTAGE_URL = '/api/activity-percentage/'

const Metrics = () => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const activityId = useAppSelector((state: RootState) => state.SpeciesFilter.activityId)
    const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
    const organisationId = useAppSelector((state: RootState) => state.SpeciesFilter.organisationId)
    const spatialFilterValues = useAppSelector((state: RootState) => state.SpeciesFilter.spatialFilterValues)
    // start year on charts is taken from Filter's endYear.
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [loading, setLoading] = useState(false)
    const [activityData, setActivityData] = useState([])
    const [activityType, setActivityType] = useState({})
    const [open, setOpen] = useState(false)

    const contentRef = useRef(null);

    // Declare errorMessage as a state variable
    const [showCharts, setShowCharts] = useState(false);

    const { data: userInfoData, isLoading, isSuccess } = useGetUserInfoQuery();
    const [userPermissions, setUserPermissions] = useState([]);

    const {
        data: activityList,
        isLoading: isActivityLoading,
        isSuccess: isActivitySuccess
    } = useGetActivityAsObjQuery()

    const {
        data: propertyTypes,
        isLoading: isPropertyTypesLoading,
        isSuccess: isPropertyTypesSuccess
    } = useGetPropertyTypeQuery()

    let activityParams = activityId;
    if (activityList) {
        activityParams = activityId.split(',').length === activityList.length ? 'all': activityId
    }

    useEffect(() => {
        if (isSuccess) {
            // Extract user permissions
            setUserPermissions(userInfoData?.user_permissions.map((permission) => permission.toLowerCase().replace(/\s/g, '')) || []);
        }
    }, [isSuccess, userInfoData]);

    const fetchActivityPercentageData = () => {
        setLoading(true)

        let fullUrl = `${FETCH_ACTIVITY_PERCENTAGE_URL}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&activity=${activityParams}&property=${propertyId}`

        axios.get(fullUrl).then((response) => {
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

    useEffect(() => {
        if(selectedSpecies){
            setShowCharts(true)
            fetchActivityPercentageData();
        }else {
            setShowCharts(false);
        }
    }, [propertyId, startYear, endYear, selectedSpecies])

    // downloads all charts rendered on page
    const handleDownloadPdf = async () => {
        setOpen(true)
        const data = document.getElementById('charts-container');
        html2canvas(data, {scale: 2}).then((canvas:any) => {
          const imgWidth = 208;
          const pageHeight = 295;
          const imgHeight = (canvas.height * imgWidth) / canvas.width;
          let heightLeft = imgHeight;
          let position = 0;
          heightLeft -= pageHeight;
          const doc = new jsPDF('p', 'mm');
          doc.setFillColor('245');
          doc.addImage(canvas, 'PNG', 0, position, imgWidth, imgHeight + 30, '', 'FAST');
          while (heightLeft >= 0) {
            position = heightLeft - imgHeight;
            doc.addPage();
            doc.addImage(canvas, 'PNG', 0, position, imgWidth, imgHeight + 30, '', 'FAST');
            heightLeft -= pageHeight;
          }
          setOpen(false)
          doc.save(`${selectedSpecies} - metrics.pdf`);
        });
    }

    type Constants = {
        [key: string]: boolean;
    };

    // TODO: Improve this, we don't need constants here, we can simply check the permissions directly
    const constants: Constants = {
        canViewPopulationTrend: false,
        canViewPopulationCategory: false,
        canViewPropertyType: false,
        canViewDensityBar: false,
        canViewPropertyAvailable: false,
        canViewAgeGroup: false,
        canViewAreaAvailable: false,
        canViewProvinceSpeciesCount: false,
        canViewProvinceSpeciesCountAsPercentage: false,
        canViewTotalCount: false,
        canViewCountAsPercentage: false,
        canViewPopulationEstimate: false,
        canViewPopulationEstimateAsPercentage: false,
    };


    function updateConstants(userPermissions: string[], constants: Constants) {
        for (const permission of userPermissions) {
            for (const key in constants) {
              if (constants.hasOwnProperty(key) && key.toLowerCase() === permission) {
                constants[key] = true;
              }
            }
        }
    }

    // Example usage:
    // userPermissions is an array of permission strings
    // Example: ['CanViewPopulationCategory', 'CanEditData', ...]

    // Call the function with user permissions
    updateConstants(userPermissions, constants);

    return (
        <Box className='main-content-wrap'>
            <Box className='main-content-area'>
                <Box>
                    <Modal
                    id={'pdf-modal'}
                    open={open}
                    >
                        <Box>
                            <Typography variant="h6" component="h2">
                                Generating PDF!
                            </Typography>
                            <Typography id="modal-modal-description" sx={{mt: 2}}>
                                This might take a while.
                            </Typography>
                            <Loading />
                        </Box>
                    </Modal>
                </Box>
                <Box className="charts-container" id={'charts-container'}>

                    {showCharts ? (
                            <div className="buttonsBuffer">
                            <Topper></Topper>
                            <Grid container spacing={1} ref={contentRef}>

                                {
                                constants.canViewPopulationCategory &&
                                selectedSpecies && (
                                    <Grid item xs={12} md={12} lg={6}>
                                        <PropertyCountPerCategoryChart
                                            selectedSpecies={selectedSpecies}
                                            propertyTypeList={propertyTypes}
                                            propertyId={propertyId}
                                            year={endYear}
                                            activityIds={activityId}
                                            spatialFilterValues={spatialFilterValues}
                                            loading={loading}
                                            setLoading={setLoading}
                                            chartId={'property-count-per-population-category-chart'}
                                            chartTitle={'Number of properties per population category (count) of {species} for {year}'}
                                            xLabel={'Population size category (Count)'}
                                            url={'/api/property-count-per-population-category-size/'}
                                        />
                                    </Grid>
                                )}

                                {
                                userInfoData?.user_permissions.includes('Can view property count per population density category') &&
                                selectedSpecies && (
                                    <Grid item xs={12} md={12} lg={6}>
                                        <PropertyCountPerCategoryChart
                                            selectedSpecies={selectedSpecies}
                                            propertyTypeList={propertyTypes}
                                            propertyId={propertyId}
                                            year={endYear}
                                            activityIds={activityId}
                                            spatialFilterValues={spatialFilterValues}
                                            loading={loading}
                                            setLoading={setLoading}
                                            chartId={'property-count-per-population-density-category'}
                                            chartTitle={'Number of properties per population category (population density) of {species} for {year}'}
                                            xLabel={'Population size categories (population density)'}
                                            url={'/api/property-count-per-population-density-category/'}
                                        />
                                    </Grid>
                                )}

                                {
                                userInfoData?.user_permissions.includes('Can view property count per area category') &&
                                selectedSpecies && (
                                    <Grid item xs={12} md={12} lg={6}>
                                        <PropertyCountPerCategoryChart
                                            selectedSpecies={selectedSpecies}
                                            propertyTypeList={propertyTypes}
                                            propertyId={propertyId}
                                            year={endYear}
                                            activityIds={activityId}
                                            spatialFilterValues={spatialFilterValues}
                                            loading={loading}
                                            setLoading={setLoading}
                                            chartId={'property-count-per-area-category-chart'}
                                            chartTitle={'Number of properties per categories of area (ha) for {species} for {year}'}
                                            xLabel={'Area size category (ha)'}
                                            url={'/api/property-count-per-area-category/'}
                                        />
                                    </Grid>
                                )}

                                {
                                userInfoData?.user_permissions.includes('Can view property count per area available to species category') &&
                                selectedSpecies && (
                                    <Grid item xs={12} md={12} lg={6}>
                                        <PropertyCountPerCategoryChart
                                            selectedSpecies={selectedSpecies}
                                            propertyTypeList={propertyTypes}
                                            propertyId={propertyId}
                                            year={endYear}
                                            activityIds={activityId}
                                            spatialFilterValues={spatialFilterValues}
                                            loading={loading}
                                            setLoading={setLoading}
                                            chartId={'property-count-per-area-available-to-species-category-chart'}
                                            chartTitle={'Number of properties per categories of area (ha) available to {species} for {year}'}
                                            xLabel={'Area size category (ha)'}
                                            url={'/api/property-count-per-area-available-to-species-category/'}
                                        />
                                    </Grid>
                                )}

                                {
                                constants.canViewProvinceSpeciesCount &&
                                selectedSpecies && (
                                    <Grid item xs={12} md={12} lg={6}>
                                        <SpeciesCountPerProvinceChart
                                            selectedSpecies={selectedSpecies}
                                            propertyId={propertyId}
                                            startYear={startYear}
                                            endYear={endYear}
                                            organisationIds={organisationId}
                                            activityIds={activityId}
                                            spatialFilterValues={spatialFilterValues}
                                            loading={loading}
                                            setLoading={setLoading}
                                        />
                                    </Grid>
                                )}


                                {
                                constants.canViewTotalCount &&
                                selectedSpecies && (
                                    <Grid item xs={12} md={12} lg={6}>
                                        <TotalCountPerActivity
                                            selectedSpecies={selectedSpecies}
                                            propertyId={propertyId}
                                            startYear={startYear}
                                            endYear={endYear}
                                            activityTypeList={activityList}
                                            activityIds={activityId}
                                            spatialFilterValues={spatialFilterValues}
                                        />
                                    </Grid>
                                )}


                                {
                                constants.canViewPopulationEstimate &&
                                selectedSpecies && (
                                    <Grid item xs={12} md={12} lg={6}>
                                        <PopulationEstimateCategoryCount
                                            selectedSpecies={selectedSpecies}
                                            propertyId={propertyId}
                                            startYear={startYear}
                                            endYear={endYear}
                                            activityData={activityData}
                                            activityIds={activityId}
                                            spatialFilterValues={spatialFilterValues}
                                        />
                                    </Grid>
                                    )}


                                {
                                    constants.canViewPopulationCategory && (
                                        <Grid item xs={12} md={12} lg={12}>
                                            <StandardDeviationMeanChart
                                                species={selectedSpecies}
                                                propertyIds={propertyId}
                                                activityIds={activityId}
                                                spatialFilterValues={spatialFilterValues}
                                                title={`Mean and standard deviation of age classes of ${selectedSpecies} for ${endYear}`}/>
                                        </Grid>
                                    )}

                        </Grid>
                            </div>
                    ): (
                        // Render message to user
                        <Grid container justifyContent="center" alignItems="center" flexDirection={'column'}>
                            <Grid item className={'explore-message'}>
                                <Typography variant="body1" color="textPrimary" style={{ fontSize: '20px', fontWeight: 'bold' }}>
                                    Ready to explore?
                                </Typography>
                            </Grid>
                            <Grid item className={'explore-message'}>
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
                            Download data visualisations
                        </Button>
                    </Box>
                )}
            </Box>
        </Box>
    );
};

export default Metrics;
