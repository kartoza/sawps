import React, {useCallback, useEffect, useState} from "react";
import {Box, Button, Checkbox, Grid, ListItemText, Modal, Typography} from "@mui/material";
import InputLabel from '@mui/material/InputLabel';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, {SelectChangeEvent} from '@mui/material/Select';
import {DataGrid, GridColDef, GridRowParams, GridActionsCellItem} from '@mui/x-data-grid';
import EditIcon from '@mui/icons-material/Edit';
import Loading from '../../../components/Loading';
import axios from "axios";
import {useAppSelector} from "../../../app/hooks";
import {RootState} from "../../../app/store";
import {getTitle} from "../../../utils/Helpers";
import {Activity, useGetActivityAsObjQuery, useGetUserInfoQuery, UserInfo} from "../../../services/api";
import Topper from "./Topper";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import './index.scss';

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
const EXCLUDED_COLUMNS = ['upload_id', 'property_id', 'is_editable']

const DataList = () => {
    const selectedSpeciesList = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpeciesList)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const selectedInfo = useAppSelector((state: RootState) => state.SpeciesFilter.selectedInfoList)
    const spatialFilterValues = useAppSelector((state: RootState) => state.SpeciesFilter.spatialFilterValues);
    const [selectedColumns, setSelectedColumns] = useState([]);
    const [loading, setLoading] = useState(false)
    const [data, setData] = useState([])
    const [columns, setColumns] = useState([])
    const [tableData, setTableData] = useState<any>()
    const [modalOpen, setModalOpen] = useState(false)
    const [activityTableGrid, setActivityTable] = useState<any>()
    const activityDataSet = data ? data.filter(item => item?.Activity_report).flatMap((each) => Object.keys(each)) : [];
    const dataTableList = data ? data.map((data, index) => ({ ...data, id: index })) : [];
    const activity = dataTableList ? dataTableList.filter(item => item.Activity_report).map((item) => item.Activity_report) : [];
    const activityReportList = activity.length > 0 ? activity.flatMap((each) => Object.keys(each)) : [];
    const activityReportdataList = activity.map((data, index) => ({ ...data, id: index }));
    const propertyId = useAppSelector((state: RootState) => state.SpeciesFilter.propertyId)
    const organisationId = useAppSelector((state: RootState) => state.SpeciesFilter.organisationId)
    const activityId = useAppSelector((state: RootState) => state.SpeciesFilter.activityId)
    const [showReports, setShowReports] = useState(false);
    const { data: userInfoData, isLoading, isSuccess } = useGetUserInfoQuery()
    const {
        data: activityList,
        isLoading: isActivityLoading,
        isSuccess: isActivitySuccess
    } = useGetActivityAsObjQuery()

    let dataset: any[] = []
    let reportList: any[] = []
    let defaultColorWidth = {
        "Species_report": {color:"#F9A95D",width:107},
        "Property_report": {color:'#9F89BF',width:131},
        "Sampling_report": {color:"#FF5252",width:168},
        "Province_report": {color:"#FF5252",width:100},
        "Species_population_report": "#9F89BF",
        "Activity_report": checkUserRole(userInfoData) ? {color:"#696969",width:100} : {color:"#75B37A",width:100},
        "Unplanned/natural deaths": {color:"#75B37A",width:106.5},
        "Planned translocation": {color:"#F9A95D",width:106.5},
        "Planned hunt/cull": {color:"#FF5252",width:130.2},
        "Planned euthanasia": {color:"#9F89BF",width:130.2},
        "Unplanned/illegal hunting": {color:"#696969",width:147}
    }

    function isDataConsumer(userInfo: UserInfo) {
        if (!userInfo?.user_roles) return false;
        const dataConsumers = new Set([
          "National data consumer",
            "Provincial data consumer"
        ])
        return userInfo.user_roles.some(userRole => dataConsumers.has(userRole))
    }

    if (isSuccess) {
        if (isDataConsumer(userInfoData)) {
            dataset = data.flatMap((each) => Object.keys(each));
        } else {
            dataset = data.filter(item => !item?.Activity_report)?.flatMap((each) => Object.keys(each));
        }
        if (isDataConsumer(userInfoData)) {
            reportList = dataTableList;
        } else {
            reportList = dataTableList.filter(item => !item?.Activity_report);
        }
    }
    const [customColorWidth, setCustomColorWidth] = useState<any>(defaultColorWidth)

    function checkUserRole(userInfo: UserInfo) {
        if (!userInfo?.user_roles) return false;
        // TODO : Update this to use permissions instead
        const allowedRoles = new Set([
          "Organisation member",
            "Organisation manager",
            "National data scientist",
            "Provincial data scientist",
            "Super user"
        ]);
        return userInfo.user_roles.some(userRole => allowedRoles.has(userRole))
    }

    useEffect(() => {
        if (activityList) {
            setCustomColorWidth({
                ...customColorWidth,
                ...Object.assign({}, ...activityList.map(
                  (x: Activity) => ({[x.name]: {color: x.colour, width: x.width}})
                )
                )
            })
        }
    }, [activityList]);

    const fetchDataList = () => {
        setLoading(true)
        let _data = {
            'species': selectedSpeciesList,
            'reports': selectedInfo.replace(/ /g, '_'),
            'start_year': startYear,
            'end_year': endYear,
            'property': propertyId,
            'organisation': organisationId,
            'activity': activityId,
            'spatial_filter_values': spatialFilterValues,
        }
        if (isDataConsumer(userInfoData)) {
            delete _data['property']
        }
        axios.post(FETCH_AVAILABLE_DATA, _data).then((response) => {
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
      const getData = setTimeout(() => {
        fetchDataList()
      }, 500)

      return () => clearTimeout(getData)
    }, [startYear, endYear])

    useEffect(() => {
        setColumns([])
        fetchDataList()
        if (selectedSpeciesList) {
            setShowReports(true);
        } else {
            setShowReports(false);
        }
    }, [selectedSpeciesList, selectedInfo, propertyId, organisationId, activityId, spatialFilterValues])

    const handleChange = (event: SelectChangeEvent<typeof selectedColumns>) => {
        const {
            target: { value },
        } = event;
        setSelectedColumns(
            typeof value === 'string' ? value.split(',') : value,
        );
    };

    const handleExportCsv = (): void => {
        let activityParams = activityId;
        if (activityList) {
            activityParams = activityId.split(',').length === activityList.length ? 'all': activityId;
        }
        let _data = {
            'file': 'csv',
            'species': selectedSpeciesList,
            'reports': selectedInfo.replace(/ /g, '_'),
            'start_year': startYear,
            'end_year': endYear,
            'property': propertyId,
            'organisation': organisationId,
            'activity': activityParams,
            'spatial_filter_values': spatialFilterValues,
        }
        axios.post(FETCH_AVAILABLE_DATA, _data).then((response) => {
            if (response.data) {
                window.location.href=`${response.data['file']}`
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
        handleClose()
    };

    const handleExportExcel = (): void => {
        let activityParams = activityId;
        if (activityList) {
            activityParams = activityId.split(',').length === activityList.length ? 'all': activityId;
        }
        let _data = {
            'file': 'xlsx',
            'species': selectedSpeciesList,
            'reports': selectedInfo.replace(/ /g, '_'),
            'start_year': startYear,
            'end_year': endYear,
            'property': propertyId,
            'organisation': organisationId,
            'activity': activityParams,
            'spatial_filter_values': spatialFilterValues,
        }
        axios.post(FETCH_AVAILABLE_DATA, _data).then((response) => {
            if (response.data) {
                window.location.href=`${response.data['file']}`
            }
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
        handleClose()
    };

    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const getUniqueColumn = () => {
        const uniqueColumns = [];
        const seenFields = new Set();
        for (const column of columns) {
            if (!seenFields.has(column.field)) {
                uniqueColumns.push(column);
                seenFields.add(column.field);
            }
        }
        return uniqueColumns
    }

    useEffect(() => {
        if (!isSuccess) return;
        const dataGrid = dataset.length > 0 && dataset.map((each: any) =>
            <Box key={each}>
                <Box className="data-table data-grid"
                     style={{
                         backgroundColor: (customColorWidth as any)[each]?.color,
                         marginTop: '20px'
                    }}
                >
                    {getTitle(each)}
                </Box>
                {
                    reportList.length > 0 && reportList.map((item, index) => {
                        const cellData = item[each];
                        if (cellData !== undefined && cellData.length > 0) {
                            const cellKeys = Object.keys(cellData[0]);
                            const generatedColumns: GridColDef[] = cellKeys.filter((key) => !EXCLUDED_COLUMNS.includes(key)).map((key) => ({
                                field: key,
                                headerName: getTitle(key),
                                flex: 1,
                            }));
                            const filteredColumns = generatedColumns.filter((column) =>
                                selectedColumns.length > 0 ?
                                    selectedColumns.includes(column.headerName) : []
                            );
                            for (const value of generatedColumns) {
                                if (!columns.includes(value)) {
                                    columns.push(value)
                                }
                            }
                            if (each === 'Species_report' && userInfoData?.user_permissions.includes('Can edit species population data')) {
                                filteredColumns.push({
                                    field: '',
                                    headerName: 'Action',
                                    flex: 0.5,
                                    type: 'actions',
                                    getActions: (params: GridRowParams) => [
                                        <GridActionsCellItem key={params.id} icon={<EditIcon />} onClick={() => {
                                            let _speciesReportRow = params.row as any
                                            window.location.replace(window.location.origin + `/upload-data/${_speciesReportRow.property_id}/?upload_id=${_speciesReportRow.upload_id}`)
                                        }} label="Edit Data" title="Edit Data" hidden={!params.row.is_editable} />
                                      ]
                                })
                            }
                            const cellRows = cellData.map((row: any, rowIndex: any) => ({
                                id: rowIndex,
                                ...row,
                            }));
                            return (
                                <DataGrid
                                    key={index}
                                    rows={cellRows}
                                    columns={filteredColumns}
                                    disableRowSelectionOnClick
                                    components={{
                                        Pagination: null,
                                    }}
                                />
                            );
                        }
                    })
                }
            </Box>
        )
        const activityDataGrid = isDataConsumer(userInfoData) && activityDataSet.length > 0 ?
          null : activityDataSet.map((each: any) =>
            <Box key={each}>
                <Box className="data-table"
                     style={{
                         backgroundColor: (customColorWidth as any)[each]?.color,
                         marginTop: '20px',
                    }}
                >
                    {getTitle(each)}
                </Box>
                {activityReportList.map((each: any) =>
                    <Box key={each}>
                        <Box className="data-table" style={{  backgroundColor: (customColorWidth as any)[each]?.color }}>
                            {getTitle(each)}
                        </Box>
                        {activityReportdataList.length > 0 && activityReportdataList.map((item, index) => {
                            const cellData = item[each];
                            if (cellData !== undefined && cellData.length > 0) {
                                const cellKeys = cellData[0] && Object.keys(cellData[0]);
                                const generatedColumns: GridColDef[] = cellKeys.length > 0 && cellKeys.map((key) => ({
                                    field: key,
                                    headerName: getTitle(key),
                                    flex: 1
                                }));
                                const filteredColumns = generatedColumns.filter((column) =>
                                    selectedColumns.length > 0 ?
                                        selectedColumns.includes(column.headerName) : []
                                );
                                for (const value of generatedColumns) {
                                    if (!columns.includes(value)) {
                                        columns.push(value)
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
                                        columns={filteredColumns}
                                        disableRowSelectionOnClick
                                        getRowHeight={() => 'auto'}
                                        components={{
                                            Pagination: null,
                                        }}
                                    />
                                );
                            }
                        })}
                    </Box>
                )}
            </Box>);
        setActivityTable(activityDataGrid)

        const uniqueColumns = getUniqueColumn()
        setColumns(uniqueColumns)
        setTableData(dataGrid)
    }, [data, selectedColumns, isSuccess])

    useEffect(() => {
        const uniqueColumns = getUniqueColumn()
        setSelectedColumns(
          uniqueColumns
            .filter(col => !['Organisation Name', 'Organisation Short Code', 'Property Short Code'].includes(col.headerName))
            .map(col => col.headerName)
        )
    }, [data])

        // downloads all charts rendered on page
    const handleDownloadPdf = async () => {
        setModalOpen(true)
        const data = document.getElementById('dataContainer');
        html2canvas(data, {scale: 2}).then((canvas:any) => {
          const imgWidth = 208;
          const pageHeight = 295;
          const imgHeight = (canvas.height * imgWidth) / canvas.width;
          let heightLeft = imgHeight;
          let position = 0;
          heightLeft -= pageHeight;
          const doc = new jsPDF('p', 'mm');
          doc.setFillColor('245');
          doc.addImage(canvas, 'PNG', 1, position, imgWidth, imgHeight, '', 'FAST');
          while (heightLeft >= 0) {
            position = heightLeft - imgHeight;
            doc.addPage();
            doc.addImage(canvas, 'PNG', 1, position, imgWidth, imgHeight, '', 'FAST');
            heightLeft -= pageHeight;
          }
          setModalOpen(false)
          doc.save(`${selectedSpeciesList} - reports.pdf`);
        });
    }


    return (
        <Box className='main-content-wrap'>
            <Box className='main-content-area'>
            {showReports ? (
                <Box>
                    <Box>
                        <Modal
                        id={'pdf-modal'}
                        open={modalOpen}
                        >
                            <Box>
                                <Typography variant="h6" component="h2">
                                    Generating PDF!
                                </Typography>
                                <Typography id="modal-modal-description" sx={{mt: 2}}>
                                    This might take a while.
                                </Typography>
                                <Loading />
                            </Box>
                        </Modal>
                    </Box>
                    <Box className='dataContainer buttonsBuffer' id={'dataContainer'}>
                        <Topper></Topper>
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
                    </Box>
                    {loading ? <Loading/> : (
                    <Box className="downlodBtn">
                        <Button onClick={handleDownloadPdf} variant="contained" color="primary">
                            Download data Report
                        </Button>
                        <Button id="download-data"
                            aria-controls={open ? 'download-data-menu' : undefined}
                            aria-haspopup="true"
                            aria-expanded={open ? 'true' : undefined}
                            variant="contained"
                            disableElevation
                            onClick={handleClick}
                            endIcon={<KeyboardArrowDownIcon />}
                            color="primary">
                            Download data
                        </Button>
                        <Menu
                            id="download-data-menu"
                            MenuListProps={{
                            'aria-labelledby': 'download-data',
                            }}
                            anchorEl={anchorEl}
                            open={open}
                            onClose={handleClose}
                        >
                            <MenuItem onClick={handleExportCsv} disableRipple>
                            Download data CSV
                            </MenuItem>
                            <MenuItem onClick={handleExportExcel} disableRipple>
                            Download data XLSX
                            </MenuItem>
                        </Menu>
                    </Box>
                    )}
                </Box>
            ) : (
                <Box>
                <Box className='dataContainer' id={'dataContainer'}>
                        <Grid container
                            justifyContent="center" alignItems="center"
                            flexDirection={'column'}>
                            <Grid item className={'explore-message'}>
                                <Typography variant="body1" color="textPrimary" style={{ fontSize: '20px', fontWeight: 'bold' }}>
                                    Ready to explore?
                                </Typography>
                            </Grid>
                            <Grid item className={'explore-message'}>
                                <Typography variant="body1" color="textPrimary" style={{ fontSize: '16px', fontWeight: 'bold' }}>
                                    Choose a species to view the data as table.
                                </Typography>
                            </Grid>
                        </Grid>
                </Box>
                </Box>
            )}
            </Box>
        </Box>
          
    )
}

export default DataList
