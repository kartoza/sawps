import React from "react";
import { Box } from "@mui/material";
import ActivityDonutChart from "./ActivityDonutChart";
import SpeciesLineChart from "./SpeciesLineChart";
import "./index.scss";

const Metrics = () => {
  return (
    <Box className="overflow-auto-chart">
      <Box className="main-chart">
        <Box className="chart-left">
          <SpeciesLineChart />
          <ActivityDonutChart />
        </Box>
      </Box>
    </Box>
  );
};

export default Metrics;
