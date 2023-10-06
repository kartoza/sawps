import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import { CategoryScale } from "chart.js";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";
import "./index.scss";
import { ChartCard } from "./ChartCard";
import { Grid } from "@mui/material";
import Loading from "../../../components/Loading";

Chart.register(CategoryScale);
Chart.register(ChartDataLabels);

interface DensityData {
  density: {
    property_name: string;
    total: number;
    density: number;
  };
}

interface DensityBarChartProps {
  selectedSpecies: string;
  propertyId: string;
  startYear: number;
  endYear: number;
  loading: boolean;
  setLoading: (loading: boolean) => void;
  densityData: DensityData[];
  setDensityData: (data: DensityData[]) => void;
}

const FETCH_SPECIES_DENSITY = "/api/species-population-total-density/";

const DensityBarChart = (props: DensityBarChartProps) => {
  const {
    selectedSpecies,
    propertyId,
    startYear,
    endYear,
    loading,
    setLoading,
    densityData,
    setDensityData,
  } = props;

  const fetchActivityPercentageData = () => {
    setLoading(true);
    axios
      .get(
        `${FETCH_SPECIES_DENSITY}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}`
      )
      .then((response) => {
        setLoading(false);
        if (response.data) {
          setDensityData(response.data);
        }
      })
      .catch((error) => {
        setLoading(false);
        console.log(error);
      });
  };

  useEffect(() => {
    fetchActivityPercentageData();
  }, [propertyId, startYear, endYear, selectedSpecies]);

  const labels = [];
  const density = [];

  for (const each of densityData) {
    labels.push(each.density.property_name);
    density.push(each.density.density);
  }

  // Customize the data and legend based on the number of properties
  const data = {
    labels: labels,
    datasets: [
      {
        label: labels.length === 1 ? labels[0] : "Properties",
        backgroundColor: "#FAA755",
        borderColor: "#FAA755",
        borderWidth: 1,
        data: density,
      },
    ],
  };

  const options = {
    plugins: {
      datalabels: {
        display: false,
      },
      legend: {
        display: true,
        position: "bottom" as "bottom",
      },
      title: {
        display: true,
        text: "Species population density per property",
        font: {
          size: 16,
          weight: "bold" as "bold",
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Properties", // X-axis label
          font: {
            size: 14,
          },
        },
      },
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 50,
          max: 200,
        },
        title: {
          display: true,
          text: "Density", // Y-axis label
          font: {
            size: 14,
          },
        },
      },
    },
  };

  return (
    <Grid>
      {!loading ? (
        <Bar data={data} options={options} height={400} width={1000} />
      ) : (
        <Loading containerStyle={{ minHeight: 160 }} />
      )}
    </Grid>
  );
};

export default DensityBarChart;
