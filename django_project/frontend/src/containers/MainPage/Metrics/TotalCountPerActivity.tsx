import React, {useEffect, useState} from 'react';
import Loading from '../../../components/Loading';
import BarChart from "../../../components/BarChart";
import axios from "axios";
import "./index.scss";

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
    activityTypeList,
    activityIds,
    spatialFilterValues
  } = props;
  const [loading, setLoading] = useState<boolean>(false);
  const [totalPopulation, setTotalPopulation] = useState(0);
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

  const fetchActivityTotalCount = () => {
    setLoading(true);
    axios
      .get(
          `${FETCH_ACTIVITY_TOTAL_COUNT}?start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&activity=${activityIds}&property=${propertyId}&spatial_filter_values=${spatialFilterValues}`
      )
      .then((response) => {
        setLoading(false);
        if (response.data) {
          setTotalPopulation(response.data.length > 0 ? response.data[0].total : 0);
          setActivityData(response.data.length > 0 ? response.data[0].activities : []);
        } else {
          setTotalPopulation(0)
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
  }, [propertyId, startYear, endYear, selectedSpecies, activityIds, spatialFilterValues]);

  useEffect(() => {
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

  for (const activityType of activityTypesObj) {
    const count = activityData.filter((dataItem: any) => dataItem.activity_type === activityType.label)
      .map((dataItem: any) => dataItem.total);

    if (count.every(d => d === 0)) continue;

    const percentage = activityData.filter((dataItem: any) => dataItem.activity_type === activityType.label)
      .map((dataItem: any) => parseFloat(((dataItem.total / totalPopulation) * 100).toFixed(2)));

    // Create the dataset object
    const dataset = {
      label: activityType.label,
      data: percentage,
      counts: count,
      backgroundColor: availableColors[activityType.label]
    };

    datasets.push(dataset);
  }

  const data = {
    labels: [''],
    datasets: datasets,
  };

  const options = {
        scales: {
            y: {
              grace: '20%',
              display: true,
              stacked: false,
              title: {
                  display: true,
                  text: 'Percentage',
                  font: {
                      size: 14,
                  },
              },
              grid: {
                  display: false,
              },
              ticks: {
                  color: "black",
              },
            }
        },
        plugins: {
            datalabels: {
                display: true,
                color: '#000',
                anchor: 'end',
                align: 'end',
                font: {
                    size: 12,
                },
                formatter: function(value: any, context: any) {
                    return `n=${context.dataset.counts ? context.dataset.counts[context.dataIndex] : null}`;
                }
            }
        },
    }

  return (
    <>
      {!loading ? (
        <BarChart
            chartData={data}
            chartId={'TotalCountPerActivity'}
            chartTitle={`Activity count as % of total population of ${selectedSpecies} for ${endYear}`}
            yLabel={'Percentage'}
            xLabel={'Activities'}
            indexAxis={'x'}
            xStacked={false}
            yStacked={false}
            options={options}
        />
      ) : (
        <Loading containerStyle={{minHeight: 160}}/>
      )}
    </>
  );
};

export default TotalCountPerActivity;