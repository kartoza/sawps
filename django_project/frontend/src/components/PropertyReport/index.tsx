import React, {useCallback, useEffect, useMemo, useState} from "react";
import {Box, Grid, Typography} from "@mui/material";
import Loading from "../Loading";
import {useAppSelector} from "../../app/hooks";
import {RootState} from "../../app/store";
import {DataGrid, GridColDef} from '@mui/x-data-grid';
import Topper from "../../containers/MainPage/Data/Topper";
import axios from "axios";
import {getTitle} from "../../utils/Helpers";
import './index.scss'

const API_URL = '/api/property-report-data/';
const PAGE_SIZE_OPTIONS = [10, 25, 50];


interface PropertyTableInterface {
    title: string
    data: any
    selectedColumns: string[]
}

function generateColumns(chartData: any, selectedColumns: string[]) {
    if (!chartData) {
        return []
    }
    const cellKeys = chartData[0] && Object.keys(chartData[0]);
    const generatedColumns: GridColDef[] = cellKeys.length > 0 && cellKeys.map((key) => ({
        field: key,
        headerName: getTitle(key),
        flex: 1
    }));
    return generatedColumns.filter((column) =>
        selectedColumns.length > 0 ?
            selectedColumns.includes(column.headerName) : []
    );
}

function generateRows(chartData: any) {
    if (!chartData) return [];
    return chartData.map((row: any, rowIndex: any) => ({
        id: rowIndex,
        ...row,
    }));
}


function PropertyTable(props: PropertyTableInterface) {
    const {
        data,
        selectedColumns,
        title
    } = props;
    if (!data) return <></>

    return (
        <Box>
            <Typography>{title}</Typography>
            <DataGrid columns={generateColumns(data, selectedColumns)}
                  rows={generateRows(data)}  initialState={{
                ...data.initialState,
                pagination: { paginationModel: { pageSize: PAGE_SIZE_OPTIONS[0] } },
            }} pageSizeOptions={PAGE_SIZE_OPTIONS}/>
        </Box>
    )
}


export default function PropertyReport() {
    const [reportsData, setReportsData] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [selectedColumns, setSelectedColumns] = useState([]);

    const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)

    const fetchData = useCallback(() => {
        setLoading(true)
        axios.get(API_URL).then((response) => {
            if (response.data) {
                setReportsData(response.data);
            }
        }).catch((e) => console.error(e)).finally(() => {
            setLoading(false);
        })
    }, [])

    useEffect(() => {
        if (propertyId) {
            setLoading(true)
            fetchData();
        }
    }, [propertyId, fetchData]);

    return (loading ? <Loading/> : reportsData ? <Box className='dataContainer buttonsBuffer' id={'dataContainer'}>
                <Topper></Topper>
                <Box>
                    {Object.keys(reportsData).map(((reportData: any) => (
                        <PropertyTable
                            title={reportData}
                            data={reportsData[reportData]}
                            selectedColumns={selectedColumns}/>
                    )))}
                </Box>
            </Box> :
            <Box>
                <Box className='dataContainer' id={'dataContainer'}>
                    <Grid container
                          justifyContent="center" alignItems="center"
                          flexDirection={'column'}>
                        <Grid item className={'explore-message'}>
                            <Typography variant="body1"
                                        color="textPrimary" style={{ fontSize: '20px', fontWeight: 'bold' }}>
                                Ready to explore?
                            </Typography>
                        </Grid>
                        <Grid item className={'explore-message'}>
                            <Typography variant="body1"
                                        color="textPrimary" style={{ fontSize: '16px', fontWeight: 'bold' }}>
                                Choose property to view the data as table.
                            </Typography>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
    )
}
