import React, {useEffect, useState} from "react";
import {Line} from "react-chartjs-2";
import {CategoryScale} from "chart.js";
import Chart from "chart.js/auto";
import Loading from "../../../components/Loading";
import "./index.scss";
import ChartContainer from "../../../components/ChartContainer";
import axios from "axios";


Chart.register(CategoryScale);
const FETCH_PROPERTY_POPULATION_SPECIES = '/api/total-area-vs-available-area/'


const AreaAvailableLineChart = (props: any) => {
    const {
        selectedSpecies,
        propertyId,
        startYear,
        endYear,
        species_name
    } = props
    const [loading, setLoading] = useState(false)
    const [areaData, setAreaData] = useState([])

    // Extract the species name
    const speciesName = species_name ? species_name : '';

    const AreaDataValue = {
        labels: areaData.map((item: any) => item?.year),
        datasets: [
            {
                label: "Area available to species",
                data: areaData.map((item: any) => item?.area_available),
                borderColor: "#F9A95D",
                backgroundColor: "#F9A95D",
                fill: {
                    target: "origin",
                    above: "#F9A95D"
                }
            },
            {
                label: "Total area of property",
                data: areaData.map((item: any) => item?.area_total),
                borderColor: "#FF5252",
                backgroundColor: "#FF5252",
                fill: "origin",
                above: "#FF5252"
            }
        ]
    }

    const fetchAreaAvailableLineData = () => {
        setLoading(true)
        axios.get(`${FETCH_PROPERTY_POPULATION_SPECIES}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                if (response.data.length > 0) {
                    setAreaData(response.data[0]?.area)
                }
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    // incase there is a single label and single value
    interface AreaDataValueB {
        labels: number[];
        datasets: any[];
      }

    const areaDataB: AreaDataValueB = AreaDataValue

      if (areaDataB.labels.length === 1) {
        const year = areaDataB.labels[0];
        if (!isNaN(year)) {
          // Modify the data in place by adding the previous year to labels
          areaDataB.labels = [year - 1, year];
        }
      }

      useEffect(() => {
        fetchAreaAvailableLineData()
      }, [propertyId, startYear, endYear, selectedSpecies]);

      areaDataB.datasets.forEach(dataset => {
        if (dataset.data.length === 1) {
          dataset.data.unshift(0);
        }
      });

    const AreaOptions = {
        tension: 0.5,
        maintainAspectRatio: false,
        responsive: true,
        elements: {
            point: {
                radius: 0,
            },
        },
        plugins: {
            tooltip: {
                enabled: true,
            },
            datalabels: {
                display: false,
            },
            legend: {
                display: true,
                position: 'bottom' as 'bottom',
                labels: {
                    boxWidth: 20,
                    boxHeight: 13,
                    padding: 12,
                    font : {
                      size: 12,
                    }
                },
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                grid: {
                    display: false,
                },
                title: {
                    display: true,
                    text: 'Year', // X-axis label
                    font: {
                        size: 14,
                    },
                },
            },
            y: {
                beginAtZero: true,
                grid: {
                    display: false,
                },
                ticks: {
                    stepSize: 65,
                    max: 260,
                },
                title: {
                    display: true,
                    text: 'Area (Ha)', // Y-axis label
                    font: {
                        size: 14,
                    },
                },
            },
        },
    };

    return (
        <>
            {!loading ? (
            <ChartContainer title={`Total area vs area available to ${speciesName}`}>
                <div style={{ width: '100%', height: 260}}>
                    <Line
                        data={AreaDataValue}
                        options={AreaOptions}
                    />
                </div>
            </ChartContainer>
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </>
    );
};

export default AreaAvailableLineChart;
