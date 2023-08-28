import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import axios from "axios";
import Loading from "../Loading";
import { Doughnut } from "react-chartjs-2";

const FETCH_ACTVITY_COUNT = "/api/activity_count_per_province/";

type ProvinceData = {
  total_area: number;
  species_area: number;
  percentage: string;
};

const availableColors: { [key: string]: string } = {
    'Western Cape': "#FF5252",
    'Mpumalanga': "rgb(83 83 84)",
    'KwaZulu-Natal': "#75B37A",
    'Free State': "#282829",
    'Limpopo': "#F9A95D",
    'Gauteng': "#000000",
    'Northern Cape': "#70B276",
    'North West': "#9F89BF",
    'Eastern Cape': "#FF5252"
  }

type SpeciesData = {
  [speciesName: string]: {
    [provinceName: string]: ProvinceData;
  };
};

const PerProvinceDonutChart = () => {
  const [loading, setLoading] = useState(false);
  const [speciesData, setSpeciesData] = useState<SpeciesData>({});

  const fetchActivityCount = () => {
    axios
      .get(FETCH_ACTVITY_COUNT)
      .then((response) => {
        if (response.data) {
          console.log(response.data);
          setSpeciesData(response.data);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    fetchActivityCount();
  }, []);

  const generatedCharts = Object.keys(speciesData).map(
    (speciesName, index) => {
      const provinceData = speciesData[speciesName];
      const provinceNames = Object.keys(provinceData);

      const chartData = {
        labels: provinceNames,
        datasets: [
          {
            data: provinceNames.map((provinceName) => {
              const percentage = parseFloat(
                provinceData[provinceName].percentage.replace("%", "")
              );
              return isNaN(percentage) ? 0 : percentage;
            }),
            backgroundColor: provinceNames.map(
              (provinceName) => availableColors[provinceName] || "#000000"
            ),
            hoverOffset: 2,
            borderWidth: 0,
          },
        ],
      };

      const options = {
        cutout: "50%",
        plugins: {
          legend: {
            position: "right" as "right",
            display: true,
            labels: {
              boxWidth: 12,
              padding: 10,
            },
          },
          datalabels: {
            color: "#fff",
            formatter: (value: number) => {
              return `${value.toFixed(2)}%`;
            },
          },
          font: {
            size: 8,
            weight: "bold" as "bold",
          },
        },
      };

      return (
        <div className="chart-container-donught" key={index}>
          <div className="donut-chart">
            <div className="chart-title">{speciesName}</div>
            <Doughnut data={chartData} options={options} width={400} />
          </div>
        </div>
      );
    }
  );

  const pairs = [];
  for (let i = 0; i < generatedCharts.length; i += 2) {
    pairs.push(
      <Box key={i} className="chart-row-donut">
        {generatedCharts[i]}
        {generatedCharts[i + 1]}
      </Box>
    );
  }

  return (
    <div>
      {!loading ? (
        pairs.length > 0 ? (
          <Box className="chart-wrapper">
            <Typography variant="h6" gutterBottom style={{ textAlign: "left" }}>
              Total count as % of the total population per province
            </Typography>
            {pairs}
          </Box>
        ) : null
      ) : (
        <Loading />
      )}
    </div>
  );
};

export default PerProvinceDonutChart;
