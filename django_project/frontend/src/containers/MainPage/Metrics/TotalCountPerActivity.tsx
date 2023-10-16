import React, { useState } from "react";
import { Doughnut } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import Loading from "../../../components/Loading";
import "./index.scss";



Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

interface SpeciesDataItem {
    province: string;
    species: string;
    year: number | null;
    count: number | null;
}

  const availableColors = [
    'rgba(112, 178, 118, 1)', 
    'rgba(250, 167, 85, 1)', 
    'rgba(157, 133, 190, 1)', 
    '#FF5252', 
    '#616161',
    // additional transparency colors for years
    'rgba(112, 178, 118, 0.5)',  // 50% transparency
    'rgba(255, 82, 82, 0.5)',  // 50% transparency
    'rgba(97, 97, 97, 0.5)',  // 50% transparency
    'rgba(157, 133, 190, 0.5)',  // 50% transparency
    'rgba(250, 167, 85, 0.5)',  // 50% transparency
  ];
  

  const TotalCountPerActivity = (props: any) => {
    const {
      selectedSpecies,
      loading,
      activityData
    } = props;
    const [backgroundImageUrl, setBackgroundImageUrl] = useState<string | undefined>(undefined);

    // Add a condition to check if the selectedSpecies and activityData meet your criteria
    if (!selectedSpecies || !activityData || activityData.length === 0) {
        return null; // Return null if the condition fails
    }
  
    // Initialize variables
    const labels: string[] = [];
    const data: number[] = [];
    const uniqueColors: string[] = [];
    let year: number = 0;
  
    if (activityData && activityData.length > 0) {
      // Iterate through activityData
      activityData.forEach((speciesData: any) => {
        const speciesActivities = speciesData.activities;
        const latestActivity = speciesActivities.reduce(
          (maxActivity: any, currentActivity: any) =>
            currentActivity.year > maxActivity.year ? currentActivity : maxActivity,
          speciesActivities[0]
        );
  
        const activityType = latestActivity.activity_type;
        const total = latestActivity.total;
        year = latestActivity.year;
  
        // Check if the activityType is not in the labels list
        if (!labels.includes(activityType)) {
            // Ensure the label is exactly 23 characters long with padding
            const paddedLabel = activityType.padEnd(50, ' '); // Pad with spaces
          
            labels.push(paddedLabel); // Use the padded label
            data.push(total);
            uniqueColors.push(availableColors[labels.length - 1]);
          }          
      });
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
  
    // Define chart title based on conditions
    let chartTitle = 'No data available for current filter selections';
  
    if (selectedSpecies && activityData && activityData.length > 0) {
      chartTitle = `Total count per activity for ${selectedSpecies} year ${year}`;
    }
    
    if (!selectedSpecies){
        chartTitle = "Please select a species for the chart to show available data";
    }
  
    const options = {
      cutout: '54%',
      plugins: {
        legend: {
          position: 'right' as 'right',
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
          color: '#fff',
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
  
  export default TotalCountPerActivity;
