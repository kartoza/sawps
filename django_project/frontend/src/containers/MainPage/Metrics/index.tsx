import React from "react";
import { Box } from "@mui/material";
import ActivityBarChart from "./ActivityBarChart";
import SpeciesLineChart from "./SpeciesLineChart";
import ActivityDonutChart from "./ActivityDonutChart";
import "./index.scss";
import CategoryBarChart from "./CategoryBarChart";

const Metrics = () => {
    return (
        <Box className="overflow-auto-chart">
            <Box className="main-chart">
                <Box className="chart-left">
                    <SpeciesLineChart />
                </Box>
            </Box>
        </Box>
    );
};

export default Metrics;
