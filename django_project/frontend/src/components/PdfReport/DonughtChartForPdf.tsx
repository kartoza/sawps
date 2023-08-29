import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import Chart from "chart.js/auto";
import axios from "axios";
import Loading from "../Loading";
import { Doughnut } from "react-chartjs-2"; 

const FETCH_ACTVITY_COUNT = '/api/activity_count_percentage/'

type AvailableColors = {
    [key: string]: string;
};

type SpeciesData = {
    [speciesName: string]: {
        [activityType: string]: string;
    };
};

const availableColors: AvailableColors = {
    'Unplanned/Illegal Hunting': "#FF5252",
    'Planned Euthanasia/DCA': "rgb(83 83 84)",
    'Unplanned/natural deaths': "#75B37A",
    'Planned Hunt/Cull': "#282829",
    'Translocation (Intake)': "#F9A95D", //need colors for these
    'Translocation (Offtake)': "#F9A95D", //need colors for these
    'Other': "#F9A95D", //need colors for these
}

const DonutChart = () => {
    const [loading, setLoading] = useState(false);
    const [speciesData, setSpeciesData] = useState<SpeciesData>({}); // Initialize with an empty object

    const fetchActivityCount = () => {
        axios.get(FETCH_ACTVITY_COUNT)
            .then((response) => {
                if (response.data) {
                    setSpeciesData(response.data);
                }
            })
            .catch((error) => {
                console.log(error);
            });
    }

    useEffect(() => {
        fetchActivityCount();
    }, []);

    const generatedCharts = Object.keys(speciesData).map((speciesName, index) => {
        const species = speciesData[speciesName];

        const labels = Object.keys(species).filter(key => key !== "species_name");
        const data = labels.map(label => {
            const value = species[label];
            if (value && typeof value === "string") {
                const floatValue = parseFloat(value.replace("%", ""));
                return isNaN(floatValue) ? 0 : floatValue;
            } else {
                return 0;
            }
        });

        const backgroundColors = labels.map(label => availableColors[label]);


        if (data.every(value => value === 0)) {
            return null; // Skip this chart
        }

        const filteredData = data.filter(value => value !== 0);
        const filteredLabels = labels.filter((_, idx) => data[idx] !== 0);
        const filteredBackgroundColors = backgroundColors.filter((_, idx) => data[idx] !== 0);

        const chartData = {
            labels: filteredLabels,
            datasets: [
                {
                    data: filteredData,
                    backgroundColor: filteredBackgroundColors,
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
                  boxWidth: 30,
                  boxHeight: 30,
                  padding: 12,
                  font : {
                    size: 20
                  }
                },
              },
              datalabels: {
                color: "#fff",
                formatter: (value: number) => {
                  return `${value.toFixed(2)}%`;
                },
                font : {
                  size: 20
                }
              },
              font: {
                size: 20,
                weight: "bold" as "bold",
              },
            },
          };

        return (
            <div className="chart-container-donught" key={index}>
                <div className="donut-chart" 
                // style={{ 
                //     backgroundImage: 'url("http://localhost:9000/static/201859c0c5a44a3b690ae8035d3fa696.png")',
                //     backgroundRepeat: "no-repeat"}}
                    >
                    <div className="chart-title" style={{ fontSize: '20px', marginLeft: '0px'  }}>{species.species_name}</div>
                    <Doughnut data={chartData} options={options} 
                    // height={300} 
                    width={500} 
                    />
                </div>
            </div>
        );
    });

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
                            Activity count as % of the total population
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


export default DonutChart;
