import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import ActivityDonutChart from "./ActivityDonutChart";
import SpeciesLineChart from "./SpeciesLineChart";
import "./index.scss";
import axios from "axios";

const FETCH_ACTIVITY_PERCENTAGE_URL = '/activity-percentage/'
const FETCH_ACTIVITY_TOTAL_COUNT = '/total-count-per-activity/'

const Metrics = () => {
    const [loading, setLoading] = useState(false)
    const [activityData, setActivityData] = useState([])
    const [activityType, setActivityType] = useState({})
    const [totalCoutData, setTotalCountData] = useState([])


    const fetchActivityPercentageData = () => {
        setLoading(true)
        axios.get(FETCH_ACTIVITY_PERCENTAGE_URL).then((response) => {
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
        axios.get(FETCH_ACTIVITY_TOTAL_COUNT).then((response) => {
            setLoading(false)
            if (response.data) {
                setTotalCountData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }


    useEffect(() => {
        fetchActivityPercentageData()
        fetchActivityTotalCount()
    }, [])
    return (
        <Box className="overflow-auto-chart">
            <Box className="main-chart">
                <Box className="chart-left">
                    <SpeciesLineChart />
                    <ActivityDonutChart activityData={totalCoutData} activityType={activityType} loading={loading} chartHeading={"Total Count per Activity"} showPercentage={false} />
                </Box>
                <Box className="chart-right">
                    <ActivityDonutChart activityData={activityData} activityType={activityType} loading={loading} chartHeading={"Activity data, as % of total population"} showPercentage={true} />
                </Box>
            </Box>
        </Box>
    );
};

export default Metrics;
