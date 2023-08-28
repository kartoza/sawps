import React from "react";
import { Box } from "@mui/material";
import LineChartForPdf from "./LineChart";
import PyramidChartForPdf from "./PyramidChart";

const SecondPageCharts = () => {
  return (
    <div >
      <div className="main-chart">
        <div className="chart-left">
          <LineChartForPdf />
          <PyramidChartForPdf />
        </div>
      </div> 
    </div>
  );
};

export default SecondPageCharts;
