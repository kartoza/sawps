import React, {useState, useEffect} from 'react';
import {Bar} from "react-chartjs-2";
import { capitalize } from '../../../utils/Helpers';

const GROWTH_COLOR_CATEGORY = [
    "#ED4B00",
    "#F6A000",
    "#999999",
    "#00B1E9",
    "#00AB76"
]

const FALLBACK_COLOR_CATEGORY = "#70B276"

export interface GrowthDataItem {
    period: string;
    pop_change_cat: string;
    count: number;
    percentage: number;
    count2: string;
    sort?: number;
    pop_size_cat?: string;
    province?: string;
    pop_size_cat_label?: string;
}

interface GrowthChartInterface {
    data: GrowthDataItem[];
    chartId: string;
}

interface GrowthDataDict {
    [key: string]: GrowthDataItem[];
}

const pop_change_categories = [
    "Decreasing rapidly (>5% pa)",
    "Steady decrease (1-5% pa)",
    "Stable (-1% to 1%)",
    "Steady increase (1-5% pa)",
    "Increasing rapidly (>5% pa)"
]
const period_categories = [
    "Last 10 years",
    "Last 5 years",
    "Last 3 years"
]

const getDefaultList = (cat: string) => {
    let _list:GrowthDataItem[] = []
    for (let i = 0; i < period_categories.length; ++i) {
        let _period = period_categories[i]
        _list.push({
            period: _period,
            pop_change_cat: cat,
            count: 0,
            percentage: 0,
            count2: 'n=0',
            sort: i
        })
    }
    return _list
}

const GrowthChart = (props: GrowthChartInterface) => {
    const [chartData, setChartData] = useState(null)

    useEffect(() => {
        if (!props.data) {
            setChartData(null)
            return;
        }

        let _data: GrowthDataDict = {}
        for (let i=0; i < props.data.length; ++i) {
            let _item = props.data[i];
            let _pop_cat = capitalize(_item.pop_change_cat)
            if (_pop_cat in _data) {
                _data[_pop_cat].push({
                    ..._item,
                    sort: period_categories.findIndex(e => e === _item.period)
                })
            } else {
                _data[_pop_cat] = [{
                    ..._item,
                    sort: period_categories.findIndex(e => e === _item.period)
                }]
            }
        }
        let _datasets = []
        for (let _category of pop_change_categories) {
            let _colorIdx = pop_change_categories.findIndex((a) => a === _category)
            let _color = _colorIdx > -1 && _colorIdx < GROWTH_COLOR_CATEGORY.length ? GROWTH_COLOR_CATEGORY[_colorIdx] : FALLBACK_COLOR_CATEGORY
            let _dataInCategory: GrowthDataItem[] = []
            if (_category in _data) {
                let _items = _data[_category]
                for (let i = 0; i < period_categories.length; ++i) {
                    let _period = period_categories[i]
                    let _itemIdx = _items.findIndex(e => e.period === _period)
                    if (_itemIdx > -1) {
                        _dataInCategory.push(_items[_itemIdx])
                    } else {
                        _dataInCategory.push({
                            period: _period,
                            pop_change_cat: _category,
                            count: 0,
                            percentage: 0,
                            count2: 'n=0',
                            sort: i
                        })
                    }
                }
            } else {
                _dataInCategory = getDefaultList(_category)
            }
            _datasets.push({
                label: _category,
                data: _dataInCategory.map((item) => item.percentage),
                counts: _dataInCategory.map((item) => item.count),
                backgroundColor: _color,
                stack: _category,
                categoryPercentage: 0.9,
                barPercentage: 0.9
            })
        }
        setChartData({
            labels: period_categories,
            datasets: _datasets
        })
    }, [props.data])

    const options:object = {
        indexAxis: 'x',
        responsive: true,
        maintainAspectRatio: false,
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
            },
            x: {
                position: 'top'
            }
        },
        plugins: {
            tooltip: {
                enabled: true
            },
            datalabels: {
                display: true,
                color: '#000',
                anchor: 'end',
                align: 'end',
                font: {
                    size: 12,
                },
                padding: {
                    top: 0,
                    bottom: 0
                },
                formatter: function(value: any, context: any) {
                    if (context.dataset.counts && context.dataset.counts[context.dataIndex])
                        return `n=${context.dataset.counts[context.dataIndex]}`;
                    return '';
                }
            },
            legend: {
                display: true,
                position: 'bottom',
                labels: {
                    boxWidth: 20,
                    boxHeight: 13,
                    padding: 12,
                    font: {
                        size: 10,
                    }
                },
            }
        },
    }

    if (chartData === null) {
        return <div></div>
    }

    return (
        <Bar
            key={props.chartId}
            data={chartData}
            options={options}
            className={'bar-chart'}
        />
    )
}

export default GrowthChart
