import React, {useEffect, useState} from 'react';
import "./index.scss";
import Loading from '../../../components/Loading';
import BarChart from "../../../components/BarChart";
import axios from "axios";

type AvailableColors = {
  [key: string]: string;
};


const PropertyCountPerCategoryChart = (props: any) => {
  const {
    propertyId,
    year,
    activityIds,
    spatialFilterValues,
    selectedSpecies,
    propertyTypeList,
    chartId,
    chartTitle,
    xLabel,
    url
  } = props;
  const [loading, setLoading] = useState<boolean>(false);
  const [propertyData, setPropertyData] = useState([]);

  const [availableColors, setAvailableColors] = useState<AvailableColors>({});
  // Define age groups and their corresponding data properties
  const [propertyTypes, setPropertyTypes] = useState([])
  const propertyTypesObj = propertyTypes.map(propertyType => {
    return {
      label: propertyType,
      dataProperty: propertyType.toLowerCase().replace(' ', '-')
    }
  })

  // Extract the species name
  const species = propertyData.length > 0 ? propertyData[0].common_name_verbatim : '';

  // Define the labels (category) dynamically from propertyData and sort them from highest to lowest
  const labels = propertyData.map((data: any) => data.category);
  
  const fetchPopulationEstimateCategoryCount = () => {
    setLoading(true);
    let fullUrl = `${url}?year=${year}&species=${selectedSpecies}&property=${propertyId}&activity=${activityIds}&spatial_filter_values=${spatialFilterValues}`

    axios.get(fullUrl).then((response) => {
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
  }, [propertyId, year, selectedSpecies, activityIds, spatialFilterValues]);

  useEffect(() => {
    if (propertyTypeList) {
      let avColors = {}
      let propertyTypeNames = []
      for (const propertyType of propertyTypeList) {
        const propertyTypeName: string = propertyType.name
        // @ts-ignore
        avColors[propertyTypeName] = propertyType.colour
        propertyTypeNames.push(propertyTypeName)
      }
      setAvailableColors(avColors)
      setPropertyTypes(propertyTypeNames)
    }
  }, [propertyTypeList]);

  // Create an array to hold datasets
  const datasets = [];

  // Loop through age groups
  for (const propertyType of propertyTypesObj) {
    // Map the data for the current age group
    const data = propertyData.map((dataItem: any) => dataItem[propertyType.dataProperty] || 0);

    if (data.every(d => d === 0)) continue;

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

  const options = {
        scales: {
            y: {
              ticks: {
                  precision: 0
              },
            }
        }
    }

  return (
    <>
      {!loading ? (
        <BarChart
            chartData={data}
            chartId={chartId}
            chartTitle={chartTitle.replace('{species}', selectedSpecies).replace('{year}', year)}
            yLabel={'Count'}
            xLabel={xLabel}
            indexAxis={'x'}
            options={options}
        />
      ) : (
        <Loading containerStyle={{minHeight: 160}}/>
      )}
    </>
  );
};

export default PropertyCountPerCategoryChart;
