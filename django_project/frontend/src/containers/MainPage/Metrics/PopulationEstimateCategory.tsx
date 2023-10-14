import React, { useEffect, useState } from "react";
import { Doughnut } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import Loading from "../../../components/Loading";
import axios from "axios";
import "./index.scss";

Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_POPULATION_ESTIMATE_CATEGORY_COUNT = "/api/total-count-per-population-estimate/";

const availableColors = [
  'rgba(112, 178, 118, 1)',
  'rgba(250, 167, 85, 1)',
  'rgba(157, 133, 190, 1)',
  '#FF5252',
  '#616161',
  // additional transparency colors for years
  'rgba(112, 178, 118, 0.5)', // 50% transparency
  'rgba(255, 82, 82, 0.5)', // 50% transparency
  'rgba(97, 97, 97, 0.5)', // 50% transparency
  'rgba(157, 133, 190, 0.5)', // 50% transparency
  'rgba(250, 167, 85, 0.5)', // 50% transparency
];

const PopulationEstimateCategoryCount = (props: any) => {
  const {
    selectedSpecies,
    propertyId,
    startYear,
    endYear,
    loading,
    setLoading,
  } = props;
  let year: number | null = null;
  const [speciesData, setSpeciesData] = useState([]);

  const fetchPopulationEstimateCategoryCount = () => {
    setLoading(true);
    axios
      .get(
        `${FETCH_POPULATION_ESTIMATE_CATEGORY_COUNT}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`
      )
      .then((response) => {
        if (response.data) {
          setSpeciesData(response.data);
          setLoading(false);
        }
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchPopulationEstimateCategoryCount();
  }, [propertyId, startYear, endYear, selectedSpecies]);
  const [backgroundImageUrl, setBackgroundImageUrl] = useState<string | undefined>(undefined);

  if (!selectedSpecies) {
    return null; // Return null if the condition fails
  }


  // Initialize variables
  const labels: string[] = [];
  const data: number[] = [];
  const uniqueColors: string[] = [];

  // Iterate through the keys of speciesData
  for (const category in speciesData) {
    if (speciesData.hasOwnProperty(category)) {
      const categoryData = speciesData[category];
      const count = categoryData.count;
      year = categoryData.years[0];

      const paddedLabel = category.padEnd(50, ' '); // Pad with spaces
          
      labels.push(paddedLabel); // Use the padded label

      // labels.push(category);
      data.push(count);
      uniqueColors.push(availableColors[labels.length - 1]);
    }
  }

  // Create the chartData object
  const chartData = {
    labels: labels,
    datasets: [
      {
        data: data,
        backgroundColor: uniqueColors,
      },
    ],
  };

  // Create chart title
  let chartTitle = "Please select a species for the chart to show available data";

  if (selectedSpecies) {
    if (Object.keys(speciesData).length > 0) {
      chartTitle = `Total count per population estimate category for ${selectedSpecies}`;
      if (year) {
        chartTitle += ` year ${year}`;
      }
    } else {
      setBackgroundImageUrl('')
      chartTitle = "No data available for current filter selections";
    }
  }

  const options = {
    cutout: "54%",
    plugins: {
      legend: {
        position: "right" as "right",
        display: true,
        labels: {
          boxWidth: 20,
          boxHeight: 13,
          padding: 12,
          font: {
            size: 12,
          },
        },
      },
      datalabels: {
        color: "#fff",
        font: {
          size: 12,
        },
      },
      title: {
        display: true,
        text: chartTitle,
        align: 'start' as 'start',
        font: {
          size: 16,
          weight: 'bold' as 'bold',
        },
      },
    },
  };

  // custom styling for donut charts
  const chartContainerStyle: React.CSSProperties = {
    position: "relative",
    backgroundImage: `url(${backgroundImageUrl})`,
    backgroundSize: "20% 24%", // width and height of image
    backgroundPosition: "19% 57%", //horizontal and vertical position respectively
    backgroundRepeat: "no-repeat",
    whiteSpace: "pre-wrap", // Allow text to wrap
  };

  return (
    <>
      {!loading ? (
          <Doughnut
            data={chartData}
            options={options}
            style={chartContainerStyle}
          />
      ) : (
        <Loading containerStyle={{ minHeight: 160 }} />
      )}
    </>
  );
};


export default PopulationEstimateCategoryCount;
