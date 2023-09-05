import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";
import "./index.scss";
import {ChartCard} from "./ChartCard";



Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

const FETCH_SPECIES_DENSITY = '/api/properties-per-population-category/'

const PopulationCategoryChart = (props:any) => {
    const {selectedSpecies, propertyId, startYear, endYear, loading, setLoading ,populationData, setPopulationData} = props
    const fetchpopulationCategoryData = () => {
        setLoading(true)
        axios.get(`${FETCH_SPECIES_DENSITY}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                setPopulationData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }


    useEffect(() => {
        fetchpopulationCategoryData();
    }, [propertyId, startYear, endYear, selectedSpecies])

    const data = {
        labels: Object.keys(populationData),
        datasets: [
            {
                backgroundColor: '#9F89BF',
                borderColor: '#9F89BF',
                borderWidth: 1,
                data: Object.values(populationData),
            },
        ],
    };

    const options = {
        plugins: {
            datalabels: {
                display: false,
            },
            legend: {
                display: false,
            }
        },
        scales: {
            x: {
                beginAtZero: true,
            },
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 50,
                    max: 200,
                },
            },
        },
    };

    return (
        <ChartCard
            loading={loading}
            chartComponent={
                <Bar data={data} options={options} height={225} width={1000}/>
            }
            title={'Number of properties per population category'}
            xLabel={'Population category'}
        />
    )
};

export default PopulationCategoryChart;
