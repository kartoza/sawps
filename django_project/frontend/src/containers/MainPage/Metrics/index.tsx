import React from "react";
import { Box } from "@mui/material";
import SpeciesLineChart from "./SpeciesLineChart";
import "./index.scss";

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
