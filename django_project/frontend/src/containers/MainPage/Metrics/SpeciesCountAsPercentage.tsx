import React, { useEffect, useState } from "react";
import axios from "axios";
import Loading from "../../../components/Loading";
import { Doughnut } from "react-chartjs-2";

const FETCH_ACTVITY_COUNT = "/api/species-count-per-province/";

type ProvinceData = {
  total_area: number;
  species_area: number;
  percentage: string;
};

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


type SpeciesData = {
  [speciesName: string]: {
    [provinceName: string]: ProvinceData;
  };
};



interface SpeciesDataItem {
  province: string;
  species: string;
  year: number | null;
  count: number | null;
}



const SpeciesCountAsPercentage = (props: any) => {
  const {
    selectedSpecies,
    propertyId,
    startYear,
    endYear,
    loading,
    setLoading,
    activityData
  } = props;
  const [speciesData, setSpeciesData] = useState<SpeciesDataItem[]>([]);
  const [backgroundImageUrl, setBackgroundImageUrl] = useState<string | undefined>(undefined);


  const fetchActivityCount = () => {
    setLoading(true);
    axios
      .get(
        `${FETCH_ACTVITY_COUNT}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`
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
        fetchActivityCount();
    }, [propertyId, startYear, endYear, selectedSpecies]);

    // Extract graph_icon URL from the first item in activityData
    useEffect(() => {
        if (activityData && activityData.length > 0) {
        const firstItem = activityData[0];
        if (firstItem.graph_icon) {
            setBackgroundImageUrl(firstItem.graph_icon);
        }
        }
    }, [activityData]);

    const legendLabels: number[] = Array.from(new Set(speciesData.map((item) => item.year)))
    .filter((year) => year !== null) as number[];

    // Find the most recent year based on the endYear and legendLabels
    const currentYear = new Date().getFullYear();
    const endYearOrCurrent = endYear === currentYear ? Math.max(...legendLabels) : endYear;
    const mostRecentYear = Math.max(startYear, endYearOrCurrent);

    // Filter out objects with years not equal to the most recent year
    const filteredSpeciesData = speciesData.filter((item) => item.year === mostRecentYear);

    // Sum of all count values
    const total = filteredSpeciesData.reduce((acc, item) => acc + item.count, 0);

    // Calculate percentage values and create a new array
    const calculatedPercentageValues = filteredSpeciesData.map((item) => ({
    ...item,
    percentage: (item.count / total) * 100,
    }));

    // Create an array to store labels (province)
    const labels = calculatedPercentageValues.map((item) => item.province);

    // Create an array to store percentages
    const percentages = calculatedPercentageValues.map((item) => item.percentage);

    // Create an array for background colors
    const uniqueBackgroundColors = Array.from(new Set(labels)).map(
    (_, index) => {
        // Determine the color index considering transparency
        const colorIndex = index % availableColors.length;
        const color = availableColors[colorIndex];
        return color;
    }
    );

    const chartData = {
    labels: labels,
    datasets: [
        {
        data: percentages,
        backgroundColor: uniqueBackgroundColors,
        },
    ],
    };

  // Define the inline style for the background image
  const chartContainerStyle: React.CSSProperties = {
    position: "relative",
    backgroundImage: `url(${backgroundImageUrl})`, // Set the background image dynamically
    backgroundSize: "100% 100%",
    backgroundPosition: "left center",
    backgroundRepeat: "no-repeat",
  };

    const options = {
        cutout: "60%",
        plugins: {
            legend: {
                position: "right" as "right",
                display: true,
                labels: {
                    boxWidth: 30,
                    boxHeight: 30,
                    padding: 12,
                    font: {
                        size: 20,
                    },
                },
            },
            datalabels: {
                color: "#fff",
                formatter: (value: number, ctx: { chart: { data: { datasets: { data: any; }[]; }; }; }) => {
                    let sum = 0;
                    let dataArr = ctx.chart.data.datasets[0].data;
                    dataArr.map((data: number) => {
                        sum += data;
                    });
                    const percentage = ((value * 100) / sum).toFixed(2) + "%";
                    return percentage;
                },
                font: {
                    size: 20,
                },
            },
            title: {
                display: true,
                text: `Total count as % of total population per province for ${selectedSpecies} year of ${mostRecentYear}`,
                align: 'start' as 'start',
                font: {
                    size: 16,
                    weight: 'bold' as 'bold',
                },
            },
        },
    };

    return (
        <>
            {!loading ? (
                <div style={chartContainerStyle}>
                    <Doughnut data={chartData} options={options} />
               </div>
            ) : (
                <Loading />
            )}
        </>
    );
};

export default SpeciesCountAsPercentage;
