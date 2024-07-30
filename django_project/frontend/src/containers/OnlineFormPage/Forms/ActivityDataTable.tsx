import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import VisibilityIcon from '@mui/icons-material/Visibility';
import {
    DataGrid,
    GridColDef,
    GridActionsCellItem,
    GridRowId 
} from '@mui/x-data-grid';
import {
    AnnualPopulationPerActivityInterface
} from '../../../models/Upload';
import { EventType } from './EventDetailForm';


interface ActivityDataTableInterface {
    data: AnnualPopulationPerActivityInterface[];
    eventType: EventType;
    isReadOnly: boolean;
    handleEditRow?: (id: GridRowId, eventType: EventType) => void;
    handleDeleteRow?: (id: GridRowId, eventType: EventType) => void;
    handlePreviewRow?: (id: GridRowId, eventType: EventType) => void;
}


export default function ActivityDataTable(props: ActivityDataTableInterface) {
    const {
        data, eventType, isReadOnly, handleEditRow, handleDeleteRow, handlePreviewRow
    } = props
    const [columns, setColumns] = useState<GridColDef[]>([])

    useEffect(() => {
        let _columns:GridColDef[] = []
        if (eventType === EventType.intake) {
            _columns = [
                {
                    field: 'activity_type_name',
                    headerName: 'Event',
                    flex: 1,
                },
                {
                    field: 'total',
                    headerName: 'Total',
                    flex: 1,
                },
                {
                    field: 'reintroduction_source',
                    headerName: 'Source',
                    flex: 1,
                },
                {
                    field: 'permit',
                    headerName: 'Permit',
                    flex: 1,
                }
            ]
        } else {
            _columns = [
                {
                    field: 'activity_type_name',
                    headerName: 'Event',
                    flex: 1,
                },
                {
                    field: 'total',
                    headerName: 'Total',
                    flex: 1,
                    valueGetter: (value) => {
                        if (value.value === null) return 'NA'
                        return value.value
                    },
                },
                {
                    field: 'translocation_destination',
                    headerName: 'Destination',
                    flex: 1,
                },
                {
                    field: 'permit',
                    headerName: 'Permit',
                    flex: 1,
                }
            ]
        }
        _columns.push({
            field: 'actions',
            type: 'actions',
            getActions: ({ id }) => {
                if (isReadOnly) {
                    return [
                        <GridActionsCellItem
                            icon={<VisibilityIcon />}
                            label="Preview"
                            onClick={() => {
                                if (handlePreviewRow) {
                                    handlePreviewRow(id, eventType)
                                }
                            }}
                        />
                    ]
                }
                return [
                    <GridActionsCellItem
                        icon={<EditIcon />}
                        label="Edit"
                        onClick={() => {
                            if (handleEditRow) {
                                handleEditRow(id, eventType)
                            }
                        }}
                    />,
                    <GridActionsCellItem
                        icon={<DeleteIcon />}
                        label="Delete"
                        onClick={() => {
                            if (handleDeleteRow) {
                                handleDeleteRow(id, eventType)
                            }
                        }}
                    />,
                ]
            }
        })
        setColumns(_columns)
    }, [eventType, isReadOnly, handleEditRow, handleDeleteRow, handlePreviewRow])

    return (
        <Grid container className={'ActivityTable' + (data.length === 0 ? ' EmptyRows' : '')}>
            {columns && <DataGrid columns={columns} rows={data} autoHeight />}
        </Grid>
    )
}
