import React from "react";
import { Box } from "@mui/material";
import PopulationCategoryChart from "./PopulationCategoryChart";
import DonutChart from "./DonughtChartForPdf";

const ThirdPageCharts = () => {
  return (
      <div className="main-chart">
        <div className="chart-left">
          <PopulationCategoryChart />
          <DonutChart />
        </div>
      </div>
  );
};

export default ThirdPageCharts;
