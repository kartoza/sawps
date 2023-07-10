import React, { useState } from "react";
import { Box, Button, Checkbox, ListItemButton, ListItemIcon, ListItemText, Typography } from "@mui/material";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';
import './index.scss';

interface RowData {
    id: number;
    firstName: string | null;
    lastName: string | null;
    age: number | null;
}

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


const DataList = () => {
    const [selectedColumns, setSelectedColumns] = useState([]);
    const columns: GridColDef[] = [
        { field: 'id', headerName: 'ID', width: 90 },
        {
            field: 'firstName',
            headerName: 'First name',
            width: 150,
            editable: true,
        },
        {
            field: 'lastName',
            headerName: 'Last name',
            width: 150,
            editable: true,
        },
        {
            field: 'age',
            headerName: 'Age',
            type: 'number',
            width: 110,
            editable: true,
        },
        {
            field: 'fullName',
            headerName: 'Full name',
            description: 'This column has a value getter and is not sortable.',
            sortable: false,
            width: 160,
            valueGetter: (params: GridValueGetterParams) =>
                `${params.row.firstName || ''} ${params.row.lastName || ''}`,
        },
    ];

    const rows: RowData[] = [
        { id: 1, lastName: 'Snow', firstName: 'Jon', age: 35 },
        { id: 2, lastName: 'Lannister', firstName: 'Cersei', age: 42 },
        { id: 3, lastName: 'Lannister', firstName: 'Jaime', age: 45 },
        { id: 4, lastName: 'Stark', firstName: 'Arya', age: 16 },
        { id: 5, lastName: 'Targaryen', firstName: 'Daenerys', age: null },
        { id: 6, lastName: 'Melisandre', firstName: null, age: 150 },
        { id: 7, lastName: 'Clifford', firstName: 'Ferrara', age: 44 },
        { id: 8, lastName: 'Frances', firstName: 'Rossini', age: 36 },
        { id: 9, lastName: 'Roxie', firstName: 'Harvey', age: 65 },
    ];

    const handleChange = (event: SelectChangeEvent<typeof selectedColumns>) => {
        const {
            target: { value },
        } = event;
        setSelectedColumns(
            // On autofill we get a stringified value.
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
                            // input={<OutlinedInput label="Tag" />}
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
            <Box className="dataTable">
                <DataGrid
                    rows={rows}
                    columns={filteredColumns.length>0 ? filteredColumns : columns}
                    checkboxSelection={true}
                    disableRowSelectionOnClick
                    components={{
                        Pagination: null,
                    }}
                />
            </Box>

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