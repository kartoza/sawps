import React, { useEffect, useState } from "react";
import { Box, Button, Checkbox, ListItemText } from "@mui/material";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
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

const FETCH_AVAILABLE_DATA = '/data-table/'

const DataList = () => {
    const selectedSpecies = useAppSelector((state: RootState) => state.SpeciesFilter.selectedSpecies)
    const selectedMonths = useAppSelector((state: RootState) => state.SpeciesFilter.selectedMonths)
    const startYear = useAppSelector((state: RootState) => state.SpeciesFilter.startYear)
    const endYear = useAppSelector((state: RootState) => state.SpeciesFilter.endYear)
    const [selectedColumns, setSelectedColumns] = useState([]);
    const [loading, setLoading] = useState(false)
    const [data, setData] = useState([])
    const columns: GridColDef[] = [
        { field: 'property_name', headerName: 'Property Name', width: 150 },
        { field: 'property_id', headerName: 'Property ID', width: 150 },
        { field: 'owner', headerName: 'Owner', width: 150 },
        { field: 'owner_email', headerName: 'Owner Email', width: 150 },
        { field: 'property_type', headerName: 'Property Type', width: 150 },
        { field: 'province', headerName: 'Province', width: 150 },
        { field: 'size', headerName: 'Size (ha)', width: 150 },
        { field: 'scientific_name', headerName: 'Scientific Name', width: 150 },
        { field: 'common_name', headerName: 'Common Name', width: 150 },
        { field: 'count_total', headerName: 'Count Total', width: 150 },
        { field: 'count_adult_males', headerName: 'Count Adult Males', width: 150 },
        { field: 'count_adult_females', headerName: 'Count Adult Females', width: 150 },
        { field: 'count_subadult_total', headerName: 'Count Subadult Total', width: 150 },
        { field: 'count_subadult_male', headerName: 'Count Subadult Male', width: 150 },
        { field: 'count_subadult_female', headerName: 'Count Subadult Female', width: 150 },
        { field: 'count_juvenile_total', headerName: 'Count Juvenile Total', width: 150 },
        { field: 'count_juvenile_male', headerName: 'Count Juvenile Male', width: 150 },
        { field: 'count_juvenile_female', headerName: 'Count Juvenile Female', width: 150 },
        { field: 'groups', headerName: 'Groups', width: 150 },
        { field: 'open_closed_system', headerName: 'Open/Closed System', width: 150 },
        { field: 'area_available_ha', headerName: 'Area Available (ha)', width: 150 },
        { field: 'ar_name', headerName: 'Ar Name', width: 150 },
        { field: 'count_method', headerName: 'Count Method', width: 150 },
        { field: 'survey_method', headerName: 'Survey Method', width: 150 },
        { field: 'sampling_effort_coverage', headerName: 'Sampling Effort Coverage', width: 150 },
        { field: 'sampling_notes', headerName: 'Sampling Notes', width: 150 },
        { field: 'count_year', headerName: 'Count Year', width: 150 },
        { field: 'presence_only', headerName: 'Presence Only', width: 150 },
        { field: 'reintroduction_total', headerName: '(Re)Introduction Total', width: 150 },
        { field: 'reintroduction_adult_males', headerName: '(Re)Introduction Adult Males', width: 150 },
        { field: 'reintroduction_adult_females', headerName: '(Re)Introduction Adult Females', width: 150 },
        { field: 'reintroduction_male_juveniles', headerName: '(Re)Introduction Male Juveniles', width: 150 },
        { field: 'reintroduction_female_juveniles', headerName: '(Re)Introduction Female Juveniles', width: 150 },
        { field: 'founder_population', headerName: 'Founder Population', width: 150 },
        { field: 'reintroduction_source', headerName: '(Re)Introduction Source', width: 150 },
        { field: 'intake_permit_number', headerName: 'Intake Permit Number', width: 150 },
        { field: 'offtake_total', headerName: 'Offtake Total', width: 150 },
        { field: 'offtake_adult_males', headerName: 'Offtake Adult Males', width: 150 },
        { field: 'offtake_adult_females', headerName: 'Offtake Adult Females', width: 150 },
        { field: 'offtake_male_juveniles', headerName: 'Offtake Male Juveniles', width: 150 },
        { field: 'offtake_female_juveniles', headerName: 'Offtake Female Juveniles', width: 150 },
        { field: 'offtake_event', headerName: 'Offtake Event', width: 150 },
        { field: 'additional_detail', headerName: 'Additional Detail', width: 150 },
        { field: 'translocation_destination', headerName: 'Translocation Destination', width: 150 },
        { field: 'offtake_permit_number', headerName: 'Offtake Permit Number', width: 150 },
        { field: 'notes', headerName: 'Notes', width: 150 },
    ];

    const rows = data.map((data, index) => {
        const { taxon, property, annualpopulation, annualpopulation_per_activity } = data;
        return {
            id: index + 1,
            property_name: property?.name,
            property_id: property?.id,
            owner: property?.owner,
            owner_email: property?.owner_email,
            property_type: property?.property_type,
            province: property?.province,
            size: property?.size,
            scientific_name: taxon?.scientific_name,
            common_name: taxon?.common_name_varbatim,
            count_total: annualpopulation?.total,
            count_adult_males: annualpopulation?.adult_male,
            count_adult_females: annualpopulation?.adult_female,
            count_subadult_total: annualpopulation?.sub_adult_total,
            count_subadult_male: annualpopulation?.sub_adult_male,
            count_subadult_female: annualpopulation?.sub_adult_female,
            count_juvenile_total: annualpopulation?.juvenile_total,
            count_juvenile_male: annualpopulation?.juvenile_male,
            count_juvenile_female: annualpopulation?.juvenile_female,
            groups: annualpopulation?.group,
            open_closed_system: annualpopulation?.open_close_system_name,
            area_available_ha: property?.area_available,
            ar_name: '',
            count_method: annualpopulation?.count_method?.name,
            survey_method: annualpopulation?.survey_method?.name,
            sampling_effort_coverage: annualpopulation?.sampling_effort,
            sampling_notes: annualpopulation?.note,
            count_year: annualpopulation?.year,
            presence_only: '',
            reintroduction_total: '',
            reintroduction_adult_males: '',
            reintroduction_adult_females: '',
            reintroduction_male_juveniles: '',
            reintroduction_female_juveniles: '',
            founder_population: annualpopulation_per_activity?.founder_population,
            reintroduction_source: annualpopulation_per_activity?.reintroduction_source,
            intake_permit_number: '',
            offtake_total: '',
            offtake_adult_males: '',
            offtake_adult_females: '',
            offtake_male_juveniles: '',
            offtake_female_juveniles: '',
            offtake_event: '',
            additional_detail: '',
            translocation_destination: '',
            offtake_permit_number: '',
            notes: '',
        };
    });

    const fetchDataList = () => {
        setLoading(true)
        axios.get(`${FETCH_AVAILABLE_DATA}?month=${selectedMonths}&start_year=${startYear}&end_year=${endYear}&species=${selectedSpecies}`).then((response) => {
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
        fetchDataList();
    }, [selectedMonths, startYear, endYear, selectedSpecies])
    const handleChange = (event: SelectChangeEvent<typeof selectedColumns>) => {
        const {
            target: { value },
        } = event;
        setSelectedColumns(
            typeof value === 'string' ? value.split(',') : value,
        );
    };

    const filteredColumns = columns.filter((column) =>
        selectedColumns.includes(column.headerName)
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

    return (
        <Box>
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
                <Box className="dataTable">
                    <DataGrid
                        rows={rows}
                        columns={filteredColumns.length > 0 ? filteredColumns : columns}
                        checkboxSelection={true}
                        disableRowSelectionOnClick
                        components={{
                            Pagination: null,
                        }}
                    />
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
