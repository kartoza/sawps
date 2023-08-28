import React from "react";
import { Box } from "@mui/material";
import PerProvinceDonutChart from "./DonughtChartForPdf1";
import PerPropertyTypeDonutChart from "./DonughtChartForPdf2";

const FourthPageCharts = () => {
  return (
      <div className="main-chart">
        <div className="chart-left">
          <PerProvinceDonutChart />
          <PerPropertyTypeDonutChart />
        </div>
      </div>
  );
};

export default FourthPageCharts;
