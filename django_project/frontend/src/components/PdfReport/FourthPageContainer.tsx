import React from "react";
import PerProvinceDonutChart from "./DonughtChartForPdf1";
import PerPropertyTypeDonutChart from "./DonughtChartForPdf2";

const FourthPageCharts = () => {
  return (
      <div className="">
        <div className="">
          <PerProvinceDonutChart />
          <PerPropertyTypeDonutChart />
        </div>
      </div>
  );
};

export default FourthPageCharts;
