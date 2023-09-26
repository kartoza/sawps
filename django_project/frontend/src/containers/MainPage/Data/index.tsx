import React, { useEffect, useState } from "react";
import { Box, Button, Checkbox, ListItemText, Typography } from "@mui/material";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { DataGrid } from '@mui/x-data-grid';
import Loading from '../../../components/Loading';
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';
import axios from "axios";
import './index.scss';
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};

const FETCH_AVAILABLE_DATA = '/api/data-table/'

const DataList = () => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const selectedInfo = useAppSelector((state: RootState) => state.SpeciesFilter.selectedInfoList)
    const [selectedColumns, setSelectedColumns] = useState([]);
    const [loading, setLoading] = useState(false)
    const [data, setData] = useState([])
    const [columns, setColumns] = useState([])
    const [rows, setRows] = useState([])
    const [tableData, setTableData] = useState<any>()
    const [activityTableGrid, setActivityTable] = useState<any>()
    const [userRole, setUserRole] = useState<string>('')
    const dataset = checkUserRole(userRole) ?  data.filter(item => !item?.Activity_report)?.flatMap((each) => Object.keys(each)) : data.flatMap((each) => Object.keys(each));
    const activityDataSet = data ? data.filter(item => item?.Activity_report).flatMap((each) => Object.keys(each)) : [];
    const dataTableList = data ? data.map((data, index) => ({ ...data, id: index })) : [];
    const activity = dataTableList ? dataTableList.filter(item => item.Activity_report).map((item) => item.Activity_report) : [];
    const activityReportList = activity.length > 0 ? activity.flatMap((each) => Object.keys(each)) : [];
    const activityReportdataList = activity.map((data, index) => ({ ...data, id: index }));
    const reportList = checkUserRole(userRole) ? dataTableList.filter(item => !item?.Activity_report) : dataTableList;
    const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
    const organisationId = useAppSelector((state: RootState) => state.SpeciesFilter.organisationId)
    const color = {
        "Property_report": '#9F89BF',
        "Sampling_report": "#FF5252",
        "Province_report": "#FF5252",
        "Species_population_report": "#9F89BF",
        "Activity_report": checkUserRole(userRole) ? "#696969": "#75B37A",
        "Unplanned/natural_deaths": "#75B37A",
        "Planned_translocation": "#F9A95D",
        "Planned_hunt/cull": "#FF5252",
        "Planned_euthanasia": "#9F89BF",
        "Unplanned/illegal_hunt": "#696969",
    }

    function checkUserRole(userRole:string) {
        const allowedRoles = ["Organisation member", "Organisation manager", "National data scientist", "Regional data scientist"];
        return allowedRoles.includes(userRole);
    }

    useEffect(() => {
        const storedUserRole = localStorage.getItem('user_role');
        setUserRole(storedUserRole);
    }, []);

    const fetchDataList = () => {
        setLoading(true)
        axios.get(`${FETCH_AVAILABLE_DATA}?reports=${selectedInfo.replace(/ /g, '_')}&start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}&property=${propertyId}&organisation=${organisationId}`).then((response) => {
            setLoading(false)
            if (response.data) {
                setData(response.data)
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    useEffect(() => {
        setColumns([])
        fetchDataList();
    }, [startYear, endYear, selectedSpecies, selectedInfo, propertyId,organisationId])
    const handleChange = (event: SelectChangeEvent<typeof selectedColumns>) => {
        const {
            target: { value },
        } = event;
        setSelectedColumns(
            typeof value === 'string' ? value.split(',') : value,
        );
    };

    const filteredColumns = columns.filter((column) =>
        selectedColumns.length > 0 ?
            selectedColumns.includes(column.headerName) : []
    );

    const handleExportCsv = (): void => {
        const csvData = [
            columns.map((column) => column.headerName).join(','),
            ...rows.map((row: any) => columns.map((column) => row[column.field]).join(',')),
        ].join('\n');
        const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8' });
        saveAs(blob, 'data.csv');
    };

    const handleExportExcel = (): void => {
        const worksheet = XLSX.utils.json_to_sheet(rows);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet 1');
        const excelData = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const blob = new Blob([excelData], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        saveAs(blob, 'data.xlsx');
    };

    useEffect(() => {
        const dataGrid = dataset.length > 0 && dataset.map((each: any) =>
            <>
                <Box className="data-table" style={{ backgroundColor: color[each as keyof typeof color] }}>
                    {each.split('_')
                        .map((part: any) => part.charAt(0).toUpperCase() + part.slice(1))
                        .join(' ')}
                </Box>
                {
                    reportList.length > 0 && reportList.map((item, index) => {
                        const cellData = item[each];
                        if (cellData !== undefined) {
                            const cellKeys = Object.keys(cellData[0]);
                            const generatedColumns = cellKeys.map((key) => ({
                                field: key,
                                headerName: key.split('_')
                                    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
                                    .join(' '),
                                width: 125,
                            }));
                            for (const value of generatedColumns) {
                                if (filteredColumns.length === 0) {
                                    columns.push(value);
                                }
                            }
                            const cellRows = cellData.map((row: any, rowIndex: any) => ({
                                id: rowIndex,
                                ...row,
                            }));
                            return (
                                <DataGrid
                                    key={index}
                                    rows={cellRows}
                                    columns={selectedColumns.length > 0 ? filteredColumns : generatedColumns}
                                    disableRowSelectionOnClick
                                    components={{
                                        Pagination: null,
                                    }}
                                />
                            );
                        }
                    })
                }
            </>
        )
        const activityDataGrid = checkUserRole(userRole) && activityDataSet.length > 0 && activityDataSet.map((each: any) =>
            <>
                <Box className="data-table" style={{ backgroundColor: color[each as keyof typeof color] }}>
                    {each.split('_')
                        .map((part: any) => part.charAt(0).toUpperCase() + part.slice(1))
                        .join(' ')}
                </Box>
                {activityReportList.map((each: any) =>
                    <>
                        <Box className="data-table" style={{ backgroundColor: color[each as keyof typeof color] }}>
                            {each.split('_')
                                .map((part: any) => part.charAt(0).toUpperCase() + part.slice(1))
                                .join(' ')
                            }
                        </Box>
                        {activityReportdataList.length > 0 && activityReportdataList.map((item, index) => {
                            const cellData = item[each];
                            if (cellData !== undefined) {
                                const cellKeys = cellData[0] && Object.keys(cellData[0]);
                                const generatedColumns = cellKeys.length > 0 && cellKeys.map((key) => ({
                                    field: key,
                                    headerName: key.split('_')
                                        .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
                                        .join(' '),
                                    width: 125,
                                }));
                                const cellRows = cellData.map((row: any, rowIndex: any) => ({
                                    id: rowIndex,
                                    ...row,
                                }));
                                return (
                                    <DataGrid
                                        key={index}
                                        rows={cellRows}
                                        columns={generatedColumns}
                                        disableRowSelectionOnClick
                                        components={{
                                            Pagination: null,
                                        }}
                                    />
                                );
                            }
                        })}
                    </>
                )}
            </>)
        setActivityTable(activityDataGrid)
        const uniqueColumns = [];
        const seenFields = new Set();
        for (const column of columns) {
            if (!seenFields.has(column.field)) {
                uniqueColumns.push(column);
                seenFields.add(column.field);
            }
        }
        setColumns(uniqueColumns)
        setTableData(dataGrid)
    }, [data, selectedColumns])

    return (
        <Box style={{ paddingRight: '20px' }}>
            <Box className="bgGreen">
                <Box className="selectBox">
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label" shrink={false}>Filter columns</InputLabel>
                        <Select
                            labelId="demo-multiple-checkbox-label"
                            id="demo-multiple-checkbox"
                            multiple
                            value={selectedColumns}
                            onChange={handleChange}
                            renderValue={(selected: any) => selected.join(', ')}
                            MenuProps={MenuProps}
                        >
                            {columns.map((column) => (
                                <MenuItem key={column.headerName} value={column.headerName}>
                                    <Checkbox checked={selectedColumns.indexOf(column.headerName) > -1} />
                                    <ListItemText primary={column.headerName} />
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>
            </Box>
            {loading ? <Loading /> :
                <Box className="dataTable-auto">
                    <Box className="dataTable">
                        {data.length > 0 ?
                            <Box>{tableData}
                                {activityTableGrid}
                            </Box> :
                            <Typography>
                                No Data To Show
                            </Typography>}
                    </Box>
                </Box>}
            <Box className="downlodBtn">
                <Button onClick={handleExportExcel} variant="contained" color="primary">
                    Download data Report
                </Button>
                <Button onClick={handleExportCsv} variant="contained" color="primary">
                    Download data CSV
                </Button>
            </Box>

        </Box>
    )
}

export default DataList
