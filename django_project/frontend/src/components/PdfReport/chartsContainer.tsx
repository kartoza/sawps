import React from "react";
import { Box } from "@mui/material";
import LineChartForPdf from "./LineChart";
import PyramidChartForPdf from "./PyramidChart";

const ChartsContainer = () => {
  // return (
  //   <Box className="overflow-auto-chart">
  //     <Box className="main-chart">
  //       <Box className="chart-left">
          
  //         <PyramidChartForPdf />
  //         <LineChartForPdf />
  //         <PyramidChartForPdf />
  //       </Box>
  //       <Box className="chart-right">
  //         {/* placing more charts on the right */}
  //       </Box>
  //     </Box>
  //   </Box>
  // );
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

export default ChartsContainer;
