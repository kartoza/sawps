import React, {useEffect, useState} from 'react';
import "./index.scss";
import Loading from '../../../components/Loading';
import BarChart from "../../../components/BarChart";
import axios from "axios";

type AvailableColors = {
  [key: string]: string;
};

const availableColors: AvailableColors = {
  'Community': 'rgba(112, 178, 118, 1)', // Solid color for male
  'Provincial': 'rgba(112, 178, 118, 0.5)', // 50% transparency for female
  'National': 'rgba(250, 167, 85, 1)', // Solid color for male
  'State': 'rgba(250, 167, 85, 0.5)', // 50% transparency for female
  'Private': 'rgba(157, 133, 190, 1)', // Solid color for male
  'State and Private': 'rgba(157, 133, 190, 0.5)', // 50% transparency for female
};

const FETCH_PROPERTY_COUNT = "/api/property-count-per-population-category-size/";

const PropertyCountPerCategoryChart = (props: any) => {
  const {propertyId, year, selectedSpecies, chartId, chartTitle, xLabel} = props;
  const [loading, setLoading] = useState<boolean>(false);
  const [propertyData, setPropertyData] = useState([]);

  // Extract the species name
  const species = propertyData.length > 0 ? propertyData[0].common_name_varbatim : '';

  // Define the labels (category) dynamically from propertyData and sort them from highest to lowest
  const labels = propertyData.map((data: any) => data.category).sort();
  
  const fetchPopulationEstimateCategoryCount = () => {
    setLoading(true);
    axios
      .get(
        `${FETCH_PROPERTY_COUNT}?year=${year}&species=${selectedSpecies}&property=${propertyId}`
      )
      .then((response) => {
        setLoading(false);
        if (response.data) {
          setPropertyData(response.data);
        } else {
          setPropertyData([])
        }
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchPopulationEstimateCategoryCount();
  }, [propertyId, year, selectedSpecies]);

  // Define age groups and their corresponding data properties
  let propertyTypes = [
    'Community',
    'Provincial',
    'National',
    'State',
    'Private',
    'State and private'
  ]
  const propertyTypesObj = propertyTypes.map(propertyType => {
    return {
      label: propertyType, 
      dataProperty: propertyType.toLowerCase().replace(' ', '-')
    }
  })

  // Create an array to hold datasets
  const datasets = [];

  // Loop through age groups
  for (const propertyType of propertyTypesObj) {
    // Map the data for the current age group
    const data = propertyData.map((dataItem: any) => dataItem[propertyType.dataProperty] || 0);

    // Rearrange the data to match the sorted labels
    const sortedData = labels.map((year: any) => {
      const index = propertyData.findIndex((item: { category: any }) => item.category === year);
      return data[index];
    });

    // Create the dataset object
    const dataset = {
      label: propertyType.label,
      data: sortedData,
      backgroundColor: availableColors[propertyType.label],
      stack: `Stack ${propertyTypes.indexOf(propertyType.label)}`,
    };

    datasets.push(dataset);
  }

  let data = null;

  if (labels.length > 0 && datasets.length > 0) {
    data = {
      labels: labels,
      datasets: datasets,
    };
  } else return null;

  return (
    <>
      {!loading ? (
        <BarChart
            chartData={data}
            chartId={chartId}
            chartTitle={chartTitle.replace('{species}', species).replace('{year}', year)}
            yLabel={'Count'}
            xLabel={xLabel}
            indexAxis={'x'}
        />
      ) : (
        <Loading containerStyle={{minHeight: 160}}/>
      )}
    </>
  );
};

export default PropertyCountPerCategoryChart;
