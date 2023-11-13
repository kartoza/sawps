import React, {useEffect, useState} from 'react';
import "./index.scss";
import Loading from '../../../components/Loading';
import BarChart from "../../../components/BarChart";
import axios from "axios";

type AvailableColors = {
  [key: string]: string;
};

const FETCH_ACTIVITY_TOTAL_COUNT = '/api/total-count-per-activity/'

const TotalCountPerActivity = (props: any) => {
  const {
    propertyId,
    startYear,
    endYear,
    selectedSpecies,
    activityTypeList
  } = props;
  const [loading, setLoading] = useState<boolean>(false);
  const [allData, setAllData] = useState([]);
  const [activityData, setActivityData] = useState([]);

  const [availableColors, setAvailableColors] = useState<AvailableColors>({});
  // Define age groups and their corresponding data properties
  const [activityTypes, setActivityTypes] = useState([])
  const activityTypesObj = activityTypes.map(activityType => {
    return {
      label: activityType,
      dataProperty: activityType.toLowerCase().replace(' ', '-')
    }
  })

  // Define the labels (category) dynamically from propertyData and sort them from highest to lowest
  const labels = activityData.map((data: any) => data.category).sort();

  const fetchActivityTotalCount = () => {
    setLoading(true);
    axios
      .get(
          `${FETCH_ACTIVITY_TOTAL_COUNT}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&activity=all&property=${propertyId}`
      )
      .then((response) => {
        setLoading(false);
        if (response.data) {
          setAllData(response.data);
          setActivityData(response.data.length > 0 ? response.data[0].activities : []);
        } else {
          setAllData([])
          setActivityData([])
        }
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchActivityTotalCount();
  }, [propertyId, startYear, endYear, selectedSpecies]);

  useEffect(() => {
    console.debug('activityTypeList', activityTypeList);
    if (activityTypeList) {
      let avColors = {}
      let activityTypeNames = []
      for (const activityType of activityTypeList) {
        const activityTypeName: string = activityType.name
        // @ts-ignore
        avColors[activityTypeName] = activityType.colour
        activityTypeNames.push(activityTypeName)
      }
      setAvailableColors(avColors)
      setActivityTypes(activityTypeNames)
    }
  }, [activityTypeList]);

  // Create an array to hold datasets
  const datasets = [];

  // Loop through age groups
  for (const activityType of activityTypesObj) {
    // Map the data for the current age group
    const data = activityData.filter((dataItem: any) => dataItem.activity_type === activityType.label)
      .map((dataItem: any) => dataItem.total);

    if (data.every((d: number) => d === 0)) continue;
    //
    // // Rearrange the data to match the sorted labels
    // const sortedData = labels.map((year: any) => {
    //   const index = activityData.findIndex((item: { category: any }) => item.category === year);
    //   return data[index];
    // });

    // Create the dataset object
    const dataset = {
      label: activityType.label,
      data: data,
      backgroundColor: availableColors[activityType.label],
      // stack: `Stack ${activityTypes.indexOf(activityType.label)}`,
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
            chartId={'TotalCountPerActivity'}
            chartTitle={'Activity count as % of total population'}
            yLabel={'Percentage'}
            xLabel={'Activities'}
            indexAxis={'x'}
            // xStacked={false}
        />
      ) : (
        <Loading containerStyle={{minHeight: 160}}/>
      )}
    </>
  );
};

export default TotalCountPerActivity;