import React, {useEffect, useState} from "react";
import {Line} from "react-chartjs-2";
import {CategoryScale} from "chart.js";
import Chart from "chart.js/auto";
import Loading from "../../../components/Loading";
import "./index.scss";
import ChartContainer from "../../../components/ChartContainer";
import axios from "axios";
import {useAppSelector} from "../../../app/hooks";
import {RootState} from "../../../app/store";


Chart.register(CategoryScale);
const FETCH_PROPERTY_POPULATION_SPECIES = '/api/species/population_trend/'


const AreaAvailableLineChart = (props: any) => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const [loading, setLoading] = useState(false)
    const [areaData, setAreaData] = useState([])

    const AreaDataValue = {
        labels: areaData.map((item: any) => item?.year),
        datasets: [
            {
                label: "Area available to species",
                data: areaData.map((item: any) => item?.area_available),
                borderColor: "rgb(249, 169, 93)",
                backgroundColor: "rgba(249, 169, 93, 0.4)",
                fill: {
                    target: "origin",
                    above: "rgba(249, 169, 93, 0.4)"
                }
            },
            {
                label: "Total area of property",
                data: areaData.map((item: any) => item?.area_total),
                borderColor: "rgba(255, 82, 82)",
                backgroundColor: "rgba(255, 82, 82, 0.4)",
                fill: "origin",
                above: "rgb(255, 82, 82, 0.4)"
            }
        ]
    }

    const fetchAreaAvailableLineData = () => {
        setLoading(true)
        let url = `${FETCH_PROPERTY_POPULATION_SPECIES}?species=${selectedSpecies}&level=national&data_type=area_available_growth`

        axios.get(url).then((response) => {
            setLoading(false)
            if (response.data['results']) {
                setAreaData(response.data['results'])
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
        areaDataB.labels = []
      }

    useEffect(() => {
        fetchAreaAvailableLineData()
    }, [selectedSpecies]);

    areaDataB.datasets.forEach(dataset => {
        if (dataset.data.length === 1) {
            dataset.data = [];
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
            <ChartContainer title={`Total area vs area available to ${selectedSpecies}`}>
                <div className="AreaAvailableLineChartContainer">
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
