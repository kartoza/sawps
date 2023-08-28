import React, { useEffect, useState } from "react";
import { Box, Grid } from "@mui/material";
import ActivityDonutChart from "./ActivityDonutChart";
import SpeciesLineChart from "./SpeciesLineChart";
import "./index.scss";
import axios from "axios";
import DensityBarChart from "./DensityBarChart";
import PopulationCategoryChart from "./PopulationCategoryChart";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import PropertyAvailableBarChart from "./PropertyAvailable";
import PropertyTypeBarChart from "./PropertyType";
import AgeGroupBarChart from "./AgeGroupBarChart";
import Card from "@mui/material/Card";

const FETCH_ACTIVITY_PERCENTAGE_URL = '/api/activity-percentage/'
const FETCH_ACTIVITY_TOTAL_COUNT = '/api/total-count-per-activity/'
const FETCH_POPULATION_AGE_GROUP = '/api/population-per-age-group/'

// national metrics and download button
import GenerateChartImages from "../../../components/PdfReport/generateChartImage";

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
    const [userRole, setUserRole] = useState('');

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

    useEffect(() => {
        fetchActivityPercentageData();
        fetchActivityTotalCount();
        fetchPopulationAgeGroupData();
    }, [propertyId, startYear, endYear, selectedSpecies])

    useEffect(() => {
        // Fetch the user role from local storage
        const storedUserRole = localStorage.getItem('user_role');
        setUserRole(storedUserRole.toLocaleLowerCase());
    }, []);

    return (
        <Box className="overflow-auto-chart">
            <Grid container spacing={3} style={{ padding: 20 }}>
                <Grid item xs={12} md={6}>
                    <SpeciesLineChart />
                    <DensityBarChart />
                    <PropertyTypeBarChart />
                </Grid>
                <Grid item xs={12} md={6}>
                    <PopulationCategoryChart />
                    <PropertyAvailableBarChart />
                    { totalCoutData.length > 0 || activityData.length > 0 ?
                    <Card className="card-chart">
                        <ActivityDonutChart activityData={totalCoutData} activityType={activityType} labels={totalCountLabel} loading={loading} chartHeading={"Total Count per Activity"} showPercentage={false} />
                        <ActivityDonutChart activityData={activityData} activityType={activityType} labels={labels} loading={loading} chartHeading={"Activity data, as % of total population"} showPercentage={true} />
                    </Card> : null }
                    {ageGroupData.map((data) =>
                        <AgeGroupBarChart
                            loading={loading}
                            ageGroupData={data?.age_group}
                            icon={data?.graph_icon}
                            colour={data?.colour}
                            name={data?.common_name_varbatim}
                        />)}

                </Grid>
            </Grid>
            {/* for decision makers only */}
             {userRole === 'decision maker' && (
               <GenerateChartImages />
              )}
        </Box>
    );
};

export default Metrics;
