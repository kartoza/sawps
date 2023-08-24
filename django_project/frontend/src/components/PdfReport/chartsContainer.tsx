import React from "react";
import { Box } from "@mui/material";
import LineChartForPdf from "./LineChart";
import PyramidChartForPdf from "./PyramidChart";

const ChartsContainer = () => {
  return (
    <Box className="overflow-auto-chart">
      <Box className="main-chart">
        <Box className="chart-left">
          <LineChartForPdf />
          <PyramidChartForPdf />
        </Box>
        <Box className="chart-right">
          {/* placing more charts on the right */}
        </Box>
      </Box>
    </Box>
  );
};

export default ChartsContainer;
